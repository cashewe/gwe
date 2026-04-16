use std::fmt;
use serde::{Serialize, Deserialize};
use crate::graph::{DocumentId, ReferenceId};

/// The location of a reference quote
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Reference {
    pub id: ReferenceId,
    pub source_id: DocumentId,
    pub start_idx: u32, // is this cheaper than raw string storage?
    pub end_idx: u32,
}

/// allow users to easily view the reference
impl fmt::Display for Reference {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Reference(document={}, start={}, end={})", self.source_id, self.start_idx, self.end_idx)
    }
}

/// are any of these not crap?
impl Reference {
    /// constructor baybee
    pub fn new(
        source_id: DocumentId,
        start_idx: u32,
        end_idx: u32,
    ) -> Self {
        return Self {
            id: ReferenceId::new(), // default this
            source_id,
            start_idx,
            end_idx,
        }
    }

    /// get the string for the reference based on the input 
    pub fn resolve<'a>(&self, corpus: &'a [String]) -> &'a str {
        let doc = &corpus[self.source_id as usize]; // dont love passing the whole corpus round ngl

        return &doc[self.start_idx as usize..self.end_idx as usize]
    }
}