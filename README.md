# gwe

`gwe` meaning 'web' (as in spider) is a package for extracting relationship structures from linear text - and in particular from chunked text.

the solution uses a structured ontology to ensure cross compatibility for all outcomes, and makes liberal use of ml / ai models to extract, label and construct the knowledge graph.

built in rust because its fun, delivered in python because otherwise itll never get used :(

The eventual goal of `gwe` is to provide the building blocks for a knoweldge graph for graphRAG - but im thinking ti may have some additional benefit jsut for extracting information from documents - so maybe one feature might be a UI this time?

I really dont want to learn REACT or whatever though so if we do want a UI, maybe ill try for a claude code one-bang there...

the goal with the design is to appreciate that any fully automatic means of constructing a graph is likely to have issues, and therefore to construct in a way that allows users to edit the underlying structure as ergonomically as possible. given users may get it wrong, we ideally want to keep these edits reversible.
