from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.dtos.users import UserDTO
from api.models.users import GitHubUserModel, UserModel
from api.models.users.email_model import EmailModel
from api.repositories.defaults import BaseDatabaseRepository


class UserRepository(BaseDatabaseRepository[UserModel, UserDTO]):
    ##
    # private methods
    ##
    @staticmethod
    def _find_email(
        emails: list[EmailModel],
        candidate_id: UUID,
        candidate_email: str,
    ) -> EmailModel | None:
        return next(
            (email for email in emails if email.id == candidate_id or email.email == candidate_email),
            None,
        )

    async def _load_user(self, user_id: UUID) -> UserModel | None:
        statement = (
            select(UserModel)
            .options(
                selectinload(UserModel.emails),
                selectinload(UserModel.primary_email),
                selectinload(UserModel.github),
            )
            .where(UserModel.id == user_id)
        )
        result = await self._database.execute(statement)

        return result.scalar_one_or_none()

    @property
    def _model_type(self) -> type[UserModel]:
        return UserModel

    def _sync_emails(self, model: UserModel, emails: list) -> None:
        existing_emails = {email.id: email for email in model.emails}
        synced_emails: list[EmailModel] = []

        for email_dto in emails:
            existing_email = existing_emails.get(email_dto.id) or next(
                (item for item in model.emails if item.email == email_dto.email),
                None,
            )

            if existing_email is None:
                synced_emails.append(email_dto.to_model())
                continue

            existing_email.created_at = email_dto.created_at
            existing_email.email = email_dto.email
            existing_email.verified = email_dto.verified
            synced_emails.append(existing_email)

        model.emails = synced_emails

    async def _to_dto(self, model: UserModel) -> UserDTO:
        _model = await self._load_user(model.id)

        if _model is None:
            raise ValueError(f'user "{model.id}" could not be loaded')

        return UserDTO.from_model(_model)

    def _to_model(self, dto: UserDTO) -> UserModel:
        return dto.to_model()

    ##
    # public methods
    ##
    async def add(self, dto: UserDTO) -> UserDTO:
        model = UserModel(
            active=dto.active,
            created_at=dto.created_at,
            display_name=dto.display_name,
            id=dto.id,
            updated_at=dto.updated_at,
        )
        model.github = dto.github.to_model() if dto.github else None
        model.emails = [email.to_model() for email in dto.emails]

        try:
            self._database.add(model)
            await self._database.flush()

            if dto.primary_email is not None:
                primary_email = self._find_email(
                    emails=model.emails, candidate_id=dto.primary_email.id, candidate_email=dto.primary_email.email
                )

                if primary_email is None:
                    raise ValueError("primary email must be included in the email collection")

                model.primary_email_id = primary_email.id

            await self._database.commit()
            await self._database.refresh(model)
        except Exception:
            await self._database.rollback()
            raise

        result = await self._to_dto(model)

        self._logger.debug('added "%s" entry: "%s"', UserModel.__tablename__, result.id)

        return result

    async def bulk_add(self, dtos: list[UserDTO]) -> list[UserDTO]:
        if not dtos:
            return []

        results = [await self.add(dto) for dto in dtos]

        self._logger.debug(
            'added multiple "%s": %s',
            UserModel.__tablename__,
            "[" + ", ".join(f'"{result.id}"' for result in results) + "]",
        )

        return results

    async def delete_by_id(self, _id: UUID) -> bool:
        result = await super().delete_by_id(_id)

        if result:
            self._logger.debug('deleted "%s" entry: "%s"', UserModel, _id)

        return result

    async def get_by_email(self, email: str) -> UserDTO | None:
        result = await self._database.execute(
            select(UserModel)
            .join(UserModel.emails)
            .options(
                selectinload(UserModel.emails),
                selectinload(UserModel.primary_email),
                selectinload(UserModel.github),
            )
            .where(EmailModel.email == email)
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserDTO.from_model(model)

    async def get_by_github_id(self, github_id: int) -> UserDTO | None:
        result = await self._database.execute(
            select(UserModel)
            .options(
                selectinload(UserModel.emails),
                selectinload(UserModel.primary_email),
                selectinload(UserModel.github),
            )
            .where(UserModel.github.has(GitHubUserModel.id == github_id))
        )
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return UserDTO.from_model(model)

    async def set_primary_email(self, user_id: UUID, email_id: UUID | None) -> UserDTO | None:
        model = await self._load_user(user_id)

        if model is None:
            return None

        if email_id is None:
            model.primary_email_id = None
        else:
            email = next((item for item in model.emails if item.id == email_id), None)

            if email is None:
                raise ValueError("email does not belong to user")

            model.primary_email_id = email.id

        try:
            await self._database.commit()
            await self._database.refresh(model)
        except Exception:
            await self._database.rollback()
            raise

        return await self._to_dto(model)

    async def update(self, dto: UserDTO) -> UserDTO | None:
        model = await self._load_user(dto.id)

        if model is None:
            return None

        model.active = dto.active
        model.display_name = dto.display_name
        model.github = dto.github.to_model() if dto.github else None
        self._sync_emails(model, dto.emails)

        try:
            await self._database.flush()

            if dto.primary_email is None:
                model.primary_email_id = None
            else:
                primary_email = self._find_email(
                    emails=model.emails, candidate_id=dto.primary_email.id, candidate_email=dto.primary_email.email
                )

                if primary_email is None:
                    raise ValueError("primary email must be included in the email collection")

                model.primary_email_id = primary_email.id

            await self._database.commit()
            await self._database.refresh(model)
        except Exception:
            await self._database.rollback()
            raise

        self._logger.debug('updated "%s" entry: "%s"', UserModel, model.id)

        return await self._to_dto(model)
