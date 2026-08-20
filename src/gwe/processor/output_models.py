import uuid

from pydantic import (
    BaseModel,
    Field,
)

from ._types import Certainty


class EvidenceModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier.")
    start_idx: int = Field(
        description="The starting index of the evidence in the source text."
    )
    end_idx: int = Field(
        description="The ending index of the evidence in the source text."
    )


class EntityModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier.")
    type: str = Field(description="The type of the entity.")
    name: str = Field(description="The name of the entity.")


class RelationshipModel(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Unique identifier.")
    type: str = Field(description="The type of the relationship.")
    subject_id: uuid.UUID = Field(
        description="The unique identifier of the subject entity."
    )
    object_id: uuid.UUID = Field(
        description="The unique identifier of the object entity."
    )
    certainty: Certainty = Field(description="Confidence in the relationship.")
    evidence_ids: list[uuid.UUID] = Field(
        description="A list of unique identifiers for the evidence supporting the relationship."
    )
