import json

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
from api.schemas.builds import TemplateIntentSchema, TemplateResolutionSchema
from api.services.agents import AbstractAgentService


class TemplateResolverService:
    def __init__(self, agent_service: AbstractAgentService, root_config: RootConfigDTO) -> None:
        self._agent_service = agent_service
        self._root_config = root_config

    ##
    # public methods
    ##
    async def intent_from_prompt(self, prompt: str) -> TemplateIntentSchema:
        messages = [
            ChatCompletionSystemMessageParam(
                content=f"""
Extract software project intent from the user request.

Return JSON only. Use canonical internal values.
Rules:
- app_kind: {",".join(APP_KINDS)}
- auth_preference: {",".join(AUTH_PREFERENCES)}
- backend_framework: {",".join(BACKEND_FRAMEWORKS)}
- frontend_framework: {",".join(FRONTEND_FRAMEWORKS)}
- database: {",".join(DATABASES)}
- deployment_target: {",".join(DEPLOYMENT_TARGETS)}
- missing_fields: include only genuinely unresolved decisions
- requested_features: short stable identifiers only
""".strip(),
                role="system",
            ),
            ChatCompletionUserMessageParam(
                content=prompt,
                role="user",
            ),
        ]
        response = await self._agent_service.chat(messages=messages, temperature=0.0)
        data = json.loads(response.content)

        return TemplateIntentSchema.model_validate(data)

    async def resolve_from_intent(self, intent: TemplateIntentSchema) -> TemplateResolutionSchema:
        candidates = []

        for manifest_path in self._root_config.registry.glob("templates/*/template.yaml"):
            manifest = yaml.safe_load(manifest_path.read_text())

            score = 0.0
            reasons: list[str] = []

            if manifest.get("classification", {}).get("app_kind") == intent.app_kind:
                score += 5
                reasons.append("Matched app_kind")

            frontend = manifest.get("stack", {}).get("frontend", {}).get("framework")

            if frontend == intent.frontend_framework:
                score += 4
                reasons.append("Matched frontend framework")

            backend = manifest.get("stack", {}).get("backend", {}).get("framework")

            if backend == intent.backend_framework:
                score += 4
                reasons.append("Matched backend framework")

            supported_dbs = manifest.get("stack", {}).get("database", {}).get("supported", [])
            default_db = manifest.get("stack", {}).get("database", {}).get("default")

            if intent.database and (intent.database in supported_dbs or intent.database == default_db):
                score += 2
                reasons.append("Matched database")

            supported_auth = manifest.get("stack", {}).get("auth", {}).get("supported", [])

            if intent.auth_preference and intent.auth_preference in supported_auth:
                score += 2
                reasons.append("Matched auth preference")

            deployment_targets = manifest.get("stack", {}).get("deployment", {}).get("targets", [])

            if intent.deployment_target and intent.deployment_target in deployment_targets:
                score += 2
                reasons.append("Matched deployment target")

            candidates.append(
                {
                    "template_id": manifest["id"],
                    "score": score,
                    "reasons": reasons,
                    "manifest": manifest,
                }
            )

        candidates.sort(key=lambda item: item["score"], reverse=True)
        best = candidates[0]

        manifest = best["manifest"]
        derived_variables = {
            "auth_mode": intent.auth_preference or "jwt",
            "include_billing": "billing" in intent.requested_features,
        }

        unresolved_questions = list(intent.missing_fields)

        return TemplateResolutionSchema(
            derived_variables=derived_variables,
            reasons=best["reasons"],
            score=best["score"],
            template_id=best["template_id"],
            unresolved_questions=unresolved_questions,
        )
