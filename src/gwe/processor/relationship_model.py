from pydantic import BaseModel, Field

from ._types import Certainty


class Entity(BaseModel):
    name: str = Field(
        description="the name of the specific entity instance i.e. 'Paul'"
    )
    type: str = Field(description="the Onotological type of the entity i.e. 'person'")


class Triplet(BaseModel):
    """Extracted triplet from the source text."""

    subject: Entity = Field(description="the subject of the triplet.")
    predicate: str = Field(description="the relationship being described.")
    object: Entity = Field(description="the object on which the subject predicates.")


class RelationshipModel(BaseModel):
    """The full extracted information per relationship."""

    triplet: Triplet = Field(description="the extracted triplet.")
    certainty: Certainty = Field(description="confidence in the relationship.")
    evidence: list[str] = Field(
        description="exact text of sentence/s that sourced the relationship."
    )


class ExtractionModel(BaseModel):
    """The full extracted information."""

    relationships: list[RelationshipModel] = Field(
        description="the extracted relationships."
    )
