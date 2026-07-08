---
name: drawio-mermaid
description: Convert draw.io / diagrams.net XML, .drawio files, and bare mxGraphModel files into semantic Mermaid, and explain draw.io's official conversion boundaries. Use when Codex needs to convert draw.io XML to Mermaid while preserving flowchart, swimlane, architecture/container, component dependency, UML class, UML sequence, or simple ER semantics; or when Codex needs to route supported draw.io work such as Mermaid-to-draw.io insertion and draw.io XML export to PNG/SVG/PDF.
---

# drawio-mermaid

Use this skill to convert draw.io / diagrams.net XML into maintainable Mermaid text, and to choose the right path for adjacent draw.io conversion tasks.

## draw.io Capability Boundary

Treat draw.io's current conversion support this way:

| Direction | Status | Recommended path |
| --- | --- | --- |
| Mermaid -> draw.io | Officially supported | Use draw.io's Mermaid insertion flow. Mermaid can be converted into native draw.io shapes or inserted as an image/SVG depending on supported syntax and app behavior. |
| draw.io XML -> PNG/SVG/PDF | Officially supported | Use draw.io export / desktop CLI workflows when the user wants rendered assets. |
| draw.io XML -> Mermaid | Not officially provided as a first-party export | Use this `drawio-mermaid` project for semantic conversion. |

Official references to consult when the user asks about supported draw.io-native behavior:

- draw.io Mermaid manual: https://www.drawio.com/docs/manual/mermaid/
- draw.io insert Mermaid manual: https://www.drawio.com/docs/manual/insert/insert-mermaid/
- draw.io export formats manual: https://www.drawio.com/docs/manual/export/export-diagram/
- draw.io GitHub organization/repo: https://github.com/jgraph/drawio
- draw.io Desktop GitHub repo: https://github.com/jgraph/drawio-desktop

## Workflow

1. Locate the source `.drawio` or `.xml` file. Accept both standard `<mxfile><diagram>...` files and bare `<mxGraphModel>...` files.
2. Prefer the bundled wrapper script:

   ```bash
   node skill/drawio-mermaid/scripts/convert.mjs input.drawio -o output.mmd
   ```

3. If running from the `drawio-mermaid` project root, call the CLI directly:

   ```bash
   node src/cli.mjs input.drawio -o output.mmd
   ```

4. Use `--diagram auto` by default. Override only when the user knows the intended type:

   ```bash
   node src/cli.mjs input.xml --diagram architecture -o architecture.mmd
   node src/cli.mjs input.drawio --diagram class -o class.mmd
   node src/cli.mjs input.drawio --diagram sequence -o sequence.mmd
   node src/cli.mjs input.drawio --diagram er -o er.mmd
   ```

5. Use `--mode flowchart` only when the user explicitly wants all diagrams represented as Mermaid `flowchart`/`subgraph` instead of Mermaid native UML/ER syntax.
6. For multi-page draw.io files, use `--page <name|index>`; page indexes are 1-based for users.
7. Inspect stderr warnings. Missing `source`/`target` edges are skipped intentionally and should be mentioned if they affect the result.

## Supported Outputs

- Flowchart and swimlane/container process diagrams: Mermaid `flowchart TD` with `subgraph` hierarchy.
- Architecture and component dependency diagrams: Mermaid `flowchart TD` with nested `subgraph` containers.
- UML class diagrams: Mermaid `classDiagram`.
- UML sequence diagrams: Mermaid `sequenceDiagram`.
- Simple ER diagrams: Mermaid `erDiagram`.

## Expectations

- Preserve semantic structure: containers, nested groups, node labels, edge labels, UML/ER relationships, and service/component dependencies.
- Do not attempt pixel-perfect reproduction. Coordinates, sizes, colors, exact line routing, and most draw.io styling are intentionally not preserved.
- If the output looks semantically wrong, retry with an explicit `--diagram` value before changing code.
- Validate important conversions by checking the generated `.mmd` contains expected `subgraph`, class, participant, or entity names.
