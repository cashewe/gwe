use serde::{Serialize, Deserialize};
use std::fmt;
use uuid::Uuid;

/// used to create shallow uuid wrappers - doesnt need anything too thicccc imo
macro_rules! id_type {
    ($name:ident) => {
        #[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
        #[repr(transparent)]
        pub struct $name(Uuid);

        /// litterally just a uuid m8
        impl $name {
            pub fn new() -> Self {
                Self(Uuid::new_v4())
            }
        }

        /// lets us actually just display the uuid if we want
        impl fmt::Display for $name {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                self.0.fmt(f)
            }
        }

        /// convert from Uuid types into custom type
        impl From<Uuid> for $name {
            fn from(id: Uuid) -> Self { 
                Self(id)
            }
        }

        /// convert into raw Uuid if required by external crates
        impl From<$name> for Uuid {
            fn from(id: $name) -> Self {
                id.0
            }
        }

        /// pass into 'uuid-like' type requirements
        impl AsRef<Uuid> for $name {
            fn as_ref(&self) -> &Uuid {
                &self.0
            }
        }
    }
}

/// unique ref for a given entity
id_type!(EntityId);

/// unique ref for a relationship between two entities
id_type!(RelationshipId);

/// unqiue ref for an obect in an ontology? do i need one for relationships too?
id_type!(OntologyId);