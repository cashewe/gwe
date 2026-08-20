# gwe

`gwe` meaning 'web' (as in spider) is a package for extracting relationship structures from linear text - originally intended to be used to provide targetted context to surfaced chunks in RAG systems.

its goal is to slot into a toolkit for context management alonside `darn` and `adran`, but this time focusing not on text but on relationships. a theoretical user might surface a chunk made by `darn` which mentions a bloke, expand it to the whole section using `adran` to discover hes associated with a given organisation and then find out about who else works for that organisation via `gwe`

at its core, we want the following principles:
- BYOM
- user editable graph, requires human legible output formats
- relationship first approach, entities exist only in relation to one another
- self healing ontology using novel embedding approach to propose merges between similar objects in a reversable way
- super easy to use interface, dont make the users learn an entire query language just for this tool
- any learned information could theoretically be used by a different tool if the user wanted to migrate off (i.e. simple json data)

## possible follow ons

1. mcp server option in which we allow an agent to ask gwe questions directly - might help with agentic rag
2. simple ui tool in which user uploads a document and is able to read it via relationship graph rather than from top to bottom
3. an end to end rag that uses both `adran` and `gwe` to manage the context of the chunks its surfaces, created via `darn`