use std::fmt;
use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use crate::graph::{Reference, Relationship, Entity, EntityId, EntityCollectionId};

/// big fatty papa oh man
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Graph {
    // --- entities ---
    entities: Vec<EntityCollectionId>, // public facing entities
    raw_entities: Vec<Entity>, // all underlying entities, premerge
    entity_lookup: HashMap<EntityId, EntityCollectionId>, // can this be invertible?

    relationships: Vec<Relationship>,
    references: Vec<Reference>,
    // does it own an ontology or did the onotology simply get used to create it?
    // what about the underlying corpus does that live here? is that constructive??
}

/// allow users to easily view the graph
impl fmt::Display for Graph {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Graph({} entities, {} relationships)", self.entities.len(), self.relationships.len())
    }
}

/// this might get fat tbh?
impl Graph {
    /// create a graph - recommended via the creation object or via loading from json?
    pub fn new(
        raw_entities: Vec<Entity>,
        relationships: Vec<Relationship>,
        references: Vec<Reference>
    ) -> Self {
        let mut entities = Vec::with_capacity(raw_entities.len());
        let mut entity_index = HashMap::with_capacity(raw_entities.len());

        for (i, e) in raw_entities.iter().enumerate() {
            entities.push(vec![e.id]);
            entity_index.insert(e.id, i);
        }

        Self {
            entities,
            entity_index,
            raw_entities,
            relationships,
            references,
        }
    }

    /// merge two or more underlying entities into a single entity
    /// works by:
    /// mapping all entities in the list into the left most entities ID
    /// removing any newly empty entitycollectionids from the hashmap.
    pub fn merge_entities(&mut self, ids: &[EntityId]) {
        if ids.is_empty() {
            return;
        }

        let mut group_indices: Vec<usize> = ids
            .iter()
            .filter_map(|id| self.entity_index.get(id).copied())
            .collect();

        group_indices.sort_unstable();
        group_indices.dedup();

        if group_indices.len() <= 1 {
            return; // already in same group
        }

        let target_idx = group_indices[0];
        let mut merged = Vec::new();

        for &idx in group_indices.iter().rev() {
            let group = self.entities.swap_remove(idx);
            merged.extend(group);

            if idx < self.entities.len() {
                for id in &self.entities[idx] {
                    self.entity_index.insert(*id, idx);
                }
            }
        }

        let new_idx = self.entities.len();
        self.entities.push(merged);

        for id in &self.entities[new_idx] {
            self.entity_index.insert(*id, new_idx);
        }
    }

    /// remove an entity from its current grouping
    /// handled by changing the id we map the entity to to a brand new one
    /// i dont think there are any edge cases here...
    pub fn separate_entity(&mut self, id: EntityId) {
        let new_id = EntityCollectionId::new();
        
        self.entities.push(new_id);

        // add the lookup
        if let Some(entry) = self.entity_lookup.get_mut(&id) {
            *entry = new_id;
        } else {
            self.entity_lookup.insert(id, new_id);
        }
    }
}