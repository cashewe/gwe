sooooo

the package is effectiveyl split in half:

1. the graph creation
2. the graph manipulation

counter-intuitively, step 2 should be built first so the structure can feed the creation. step 2 also happens to be purely programmatic so no slop here baybee...
lets try to map out the objects i likely need to pull this off and see where we get - I'd guess itll basically end up like a bunch of nested modules with a 'graph' as a papa struct
this is the bit that will also need to be exposed in python

goal i think is probably an entity first graph tbh, although thats me getting stuck in a NER first world... 
we want a super ergonomic manipulation method which can easily be parsed by both human and bot - as the structure here will likely be part of prompts ssent to the models
to that end, lets try to make sure its fairly simple to read too.
we also need to bare in mind most users will be interacting with the graph object, not the entities - even if it is designed to be entity first
to that end, what is a minimal interface to provide the graph with? its basically been the last of my worries up till now...

generally plan then:

```
EntityId: uuid4   // reference this to avoid circles 
RelationshipId: uuid4 // reference this because i think its cute might delete later
OntologyId: uuid4 // unique ref for the onotology elements

Reference:
    start: int    // start character within the document
    end: int      // end character within the document
    index: int    // which source document? 

Entity:
    id: EntityId  // unique id for the entity, neccessary for aliases
    name: str     // canonical name for the entity
    ontological_mapping: str // what kind of entity is this??
    relationships: list[RelationshipId] // how does it relate to other entities?
    references: list[Reference] // list of locations the entity is referenced

Relationship:
    id: RelationshipId // unqiue ref for the relationship
    subject: EntityId // the left side of the relationship
    pbject: EntityId // entity the relationship points at
    type: str      // what in the ontology does this entity map to?
    references: list[Reference] // list of locations the relationship is referenced

WrappedEntity:
    id: EntityId   // used for aliases
    name: str      // canonical name for the collective entity
    ontological_mapping: str // resolved position in the ontology
    relationships: list[Relationship] // collective set of all relationships from members
    references: list[Reference] // list of locations all entities are referenced
    aliases: list[EntityId] // ids of all entities mapped into this one

EntityOntologicalElement:
    id: OntologyId // unqiue ref for this layer of ontology
    type: str      // label of ontological category
    children: list[OnotologyId] // everything that fits into this category
    parent: OntologyId // for reverse lookups

RelationshipOntologicalElement:
    id: OntologyId // unqiue ref for this map in the ontology
    label: str     // what is the relationship describing
    valid_sources: list[OntologyId] // what types are valid left hand sides? need only be parents?
    valid_targets: list[OntologyId] // what types are valid right hand sides? as with source

Ontology:
    entities: list[EntityOntologicalElement] // possibly just use the ids here as a map?
    relationships: list[RelationshipOntologicalELement] // as with entities

Graph:
    entities: list[WrappedEntity] // all entities in the KG
    corpus: list[str] // indexed list of text data to form the graph
    ontology: Ontology // either provided or infered?
```


will need to build this out over the course of several modules and attach relevant methods to map between the various levels. 
- add aliasing
- add... splitting? like the opposite to aliasing
- have means to deal with aliasing objects that have relationships to one another
- how to pick canonical names etc... for each wrapped entity. maybe the name of the entity in the wrapping with most refs?
- dont *think* i need aliases for relationships since ostensibly they are purely described by the ontology vs entities which have unique realisations
- Ontology feels pretty loosely thought through compared to the rest
- aliasing a wrapped element inside another wrapped element... will this knacker anything in terms of surfacing the relationshipps etc...?
