use std::fmt;
use serde::{Serialize, Deserialize};
use crate::graph::{ReferenceId, RelationshipId, EntityId};


/// Enities form the nodes of the graph.
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Entity {
    pub id: EntityId,
    pub name: str,
    pub ontological_type: str,
    pub relationships: Vec<RelationshipId>, // do we do this? or relationship first...
    pub references: Vec<ReferenceId>,
}

/// allow users to easily view entity
impl fmt::Display for Entity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Entity(name={}, type={})", self.name, self.ontological_type)
    }
}

/// this is shallow as a pond in summer heat
impl Entity {
    /// constructor baybee
    pub fn new(
        name: str,
        ontological_type: str,
        relationships: Vec<RelationshipId>,
        references: Vec<ReferenceId>
    ) -> Self {
        return Self {
            id: EntityId::new(), // default this
            name,
            ontological_type,
            relationships,
            references,
        }
    }
}
