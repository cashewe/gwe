from importlib.resources import files

from ..ai import (
    AiConfig,
    AiGateway,
)
from .output_models import (
    EntityModel,
    EvidenceModel,
    RelationshipModel,
)
from .relationship_model import (
    ExtractionModel,
)
from .relationship_model import (
    RelationshipModel as ExtractedRelationshipModel,
)


class Processor:
    def __init__(
        self,
        config: AiConfig,
    ) -> None:
        self.ai_gateway = AiGateway(config)
        self.system_prompt = (
            files("gwe.processor")
            .joinpath("prompts", "triplet_extraction_system_prompt.txt")
            .read_text(encoding="utf-8")
        )
        self.user_prompt = (
            files("gwe.processor")
            .joinpath("prompts", "triplet_extraction_user_prompt.txt")
            .read_text(encoding="utf-8")
        )

    def process_text(
        self,
        text: str,
        identifier: str,
    ) -> None:
        prompt = self.user_prompt + text
        relationships = self.ai_gateway.chat(
            prompt=prompt,
            system_prompt=self.system_prompt,
            response_type=ExtractionModel,
        )

        return self._convert_to_output_model(text, relationships)

    def _convert_to_output_model(
        self,
        source_text: str,
        extraction: ExtractionModel,
    ) -> list[EntityModel | RelationshipModel | EvidenceModel]:
        output = []

        for relationship in extraction.relationships:
            evidence = self._create_evidence_models(
                source_text,
                relationship,
            )
            entities = self._create_entity_models(relationship)
            relationship = self._create_relationship_model(
                relationship,
                entities,
                evidence,
            )

            output.extend(evidence)
            output.extend(entities)
            output.append(relationship)

        return output

    def _create_evidence_models(
        self,
        source_text: str,
        relationship_model: ExtractedRelationshipModel,
    ) -> list[EvidenceModel]:
        evidence_models = []

        for evidence_text in relationship_model.evidence:
            start_idx = source_text.find(evidence_text)

            if start_idx == -1:
                raise ValueError(
                    f"Evidence text was not found in the source text: {evidence_text!r}"
                )

            evidence_models.append(
                EvidenceModel(
                    start_idx=start_idx,
                    end_idx=start_idx + len(evidence_text),
                )
            )

        return evidence_models

    def _create_entity_models(
        self,
        relationship_model: ExtractedRelationshipModel,
    ) -> list[EntityModel]:
        triplet = relationship_model.triplet

        entities = []

        for entity in (triplet.subject, triplet.object):
            if (entity.name, entity.type) not in [
                (existing.name, existing.type) for existing in entities
            ]:
                entities.append(
                    EntityModel(
                        type=entity.type,
                        name=entity.name,
                    )
                )

        return entities

    def _create_relationship_model(
        self,
        relationship_model: ExtractedRelationshipModel,
        entities: list[EntityModel],
        evidence: list[EvidenceModel],
    ) -> RelationshipModel:
        triplet = relationship_model.triplet

        subject = next(
            entity
            for entity in entities
            if entity.name == triplet.subject.name
            and entity.type == triplet.subject.type
        )
        object_ = next(
            entity
            for entity in entities
            if entity.name == triplet.object.name and entity.type == triplet.object.type
        )

        return RelationshipModel(
            type=triplet.predicate,
            subject_id=subject.id,
            object_id=object_.id,
            certainty=relationship_model.certainty,
            evidence_ids=[model.id for model in evidence],
        )
