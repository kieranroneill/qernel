import yaml
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from api.constants import (
    APP_KINDS,
    AUTH_PREFERENCES,
    BACKEND_FRAMEWORKS,
    DATABASES,
    DEPLOYMENT_TARGETS,
    FRONTEND_FRAMEWORKS,
)
from api.dtos.system import RootConfigDTO
from api.errors.templates import TemplateNotFoundError
from api.schemas.builds import (
    TemplateIntentSchema,
    TemplateManifestSchema,
    TemplateResolutionCandidateSchema,
    TemplateResolutionSchema,
)
from api.services.agents import AbstractAgentService
from api.utilities.agents import json_from_agent_response
from api.utilities.logging import get_logger


class TemplateResolverService:
    def __init__(self, agent_service: AbstractAgentService, root_config: RootConfigDTO) -> None:
        self._agent_service = agent_service
        self._logger = get_logger()
        self._root_config = root_config

    ##
    # private methods
    ##
    def _build_unresolved_questions(self, intent: TemplateIntentSchema) -> list[str]:
        questions: list[str] = []

        for field_name in intent.missing_fields:
            if field_name == "database":
                questions.append("Which database do you want to use?")
            elif field_name == "auth_preference":
                questions.append("Which authentication strategy do you want to use?")
            elif field_name == "deployment_target":
                questions.append("Where should this project be deployed?")
            else:
                questions.append(f"Please clarify: {field_name}")

        return questions

    def _derive_variables(
        self,
        *,
        intent: TemplateIntentSchema,
        manifest: TemplateManifestSchema,
    ) -> dict[str, object]:
        defaults = {variable.name: variable.default for variable in manifest.variables if variable.default is not None}

        if intent.auth_preference is not None and intent.auth_preference != "none":
            defaults["auth_mode"] = intent.auth_preference

        defaults["include_billing"] = "billing" in intent.requested_features
        defaults["requested_features"] = intent.requested_features

        return defaults

    def _load_template_manifests(self) -> list[TemplateManifestSchema]:
        manifests: list[TemplateManifestSchema] = []

        template_root = self._root_config.registry / "templates"

        for manifest_path in template_root.glob("*/template.yaml"):
            payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

            manifests.append(TemplateManifestSchema.model_validate(payload))

        return manifests

    def _score_manifest(
        self,
        *,
        intent: TemplateIntentSchema,
        manifest: TemplateManifestSchema,
    ) -> tuple[float, list[str]]:
        score = 0.0
        reasons: list[str] = []

        if (
            intent.app_kind is not None
            and manifest.classification is not None
            and manifest.classification.app_kind == intent.app_kind
        ):
            score += 5.0
            reasons.append("Matched app kind.")

        manifest_frontend = manifest.stack.frontend.framework if manifest.stack.frontend else None

        if intent.frontend_framework is not None and manifest_frontend == intent.frontend_framework:
            score += 4.0
            reasons.append("Matched frontend framework.")

        manifest_backend = manifest.stack.backend.framework if manifest.stack.backend else None

        if intent.backend_framework is not None and manifest_backend == intent.backend_framework:
            score += 4.0
            reasons.append("Matched backend framework.")

        manifest_database = manifest.stack.database

        if intent.database is not None and intent.database != "none" and manifest_database is not None:
            supported_databases = set(manifest_database.supported)

            if intent.database == manifest_database.default or intent.database in supported_databases:
                score += 2.0

                reasons.append("Matched database.")

        manifest_auth = manifest.stack.auth

        if intent.auth_preference is not None and intent.auth_preference != "none" and manifest_auth is not None:
            if intent.auth_preference in set(manifest_auth.supported):
                score += 2.0

                reasons.append("Matched auth preference.")

        manifest_deployment = manifest.stack.deployment

        if (
            intent.deployment_target is not None
            and manifest_deployment is not None
            and intent.deployment_target in set(manifest_deployment.targets)
        ):
            score += 2.0

            reasons.append("Matched deployment target.")

        feature_packs = set(manifest.supports.feature_packs) if manifest.supports is not None else set()

        if "billing" in intent.requested_features:
            if "stripe-billing" in feature_packs:
                score += 1.5

                reasons.append("Supports billing feature pack.")

        if "redis" in intent.requested_features:
            if "redis-cache" in feature_packs:
                score += 1.5

                reasons.append("Supports redis cache feature pack.")

        return score, reasons

    ##
    # public methods
    ##
    async def intent_from_prompt(self, prompt: str) -> TemplateIntentSchema:
        messages = [
            ChatCompletionSystemMessageParam(
                content=f"""
Extract software project intent from the user request.

Return JSON only.
Use canonical internal values only.

Allowed values:
- app_kind: {",".join(APP_KINDS)}
- auth_preference: {",".join(AUTH_PREFERENCES)}
- backend_framework: {",".join(BACKEND_FRAMEWORKS)}
- frontend_framework: {",".join(FRONTEND_FRAMEWORKS)}
- database: {",".join(DATABASES)}
- deployment_target: {",".join(DEPLOYMENT_TARGETS)}

Rules:
- requested_features must contain short stable identifiers only.
- missing_fields must contain only unresolved decision fields.
- If a field is not specified and cannot be safely inferred, use null.
- Do not invent unsupported frameworks or providers.
""".strip(),
                role="system",
            ),
            ChatCompletionUserMessageParam(
                content=prompt,
                role="user",
            ),
        ]

        self._logger.debug(f'prompt "{prompt}"')

        response = await self._agent_service.chat(messages=messages, temperature=0.0)
        data = json_from_agent_response(response)

        if data is None:
            self._logger.debug(f'no template intent found for prompt "{prompt}"')

            raise TemplateNotFoundError()

        self._logger.debug(f"found template intent '{data}'")

        return TemplateIntentSchema.model_validate(data)

    async def resolve_from_intent(self, intent: TemplateIntentSchema) -> TemplateResolutionSchema:
        manifests = self._load_template_manifests()
        candidates: list[tuple[TemplateManifestSchema, float, list[str]]] = []

        for manifest in manifests:
            score, reasons = self._score_manifest(intent=intent, manifest=manifest)

            if score <= 0:
                continue

            candidates.append((manifest, score, reasons))

        if not candidates:
            self._logger.debug(f'no template candidates were found for for the intent "{intent}"')

            raise TemplateNotFoundError()

        candidates.sort(key=lambda item: item[1], reverse=True)
        best_manifest, best_score, best_reasons = candidates[0]

        candidate_summaries = [
            TemplateResolutionCandidateSchema(
                template_id=manifest.id,
                score=score,
                reasons=reasons,
            )
            for manifest, score, reasons in candidates[:5]
        ]

        derived_variables = self._derive_variables(
            intent=intent,
            manifest=best_manifest,
        )

        return TemplateResolutionSchema(
            template_id=best_manifest.id,
            score=best_score,
            reasons=best_reasons,
            derived_variables=derived_variables,
            unresolved_questions=self._build_unresolved_questions(intent),
            candidates=candidate_summaries,
        )
