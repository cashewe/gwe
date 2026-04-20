use std::fmt;
use serde::{Serialize, Deserialize};
use crate::graph::{ReferenceId, RelationshipId, EntityId};


/// Relationships form the edges of the graph.
/// for ease of modelling, all relationships will be one directional
/// we will simply have two for two directional relationships
/// do not question this, trust me its chill i asked around
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Relationship {
    pub id: RelationshipId,
    pub subject: EntityId,
    pub object: EntityId,
    pub ontological_type: str,
    pub references: Vec<ReferenceId>,
}

/// allow users to easily view relationship
impl fmt::Display for Relationship {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Relationship(type={}, subject={}, object={})", self.ontological_type, self.subject, self.object)
    }
}

/// this is shallow as a summer fling
impl Relationship {
    /// constructor baybee
    pub fn new(
        name: str,
        ontological_type: str,
        subject: EntityId,
        object: EntityId,
        references: Vec<ReferenceId>,
    ) -> Self {
        return Self {
            id: RelationshipId::new(), // default this
            ontological_type,
            subject,
            object,
            references,
        }
    }
}
