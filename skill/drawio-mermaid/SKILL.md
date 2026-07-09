---
name: drawio-mermaid
description: 如何用最小依赖处理 draw.io / diagrams.net 与 Mermaid、PNG、SVG、PDF 之间的转换。Use when Codex needs Mermaid -> draw.io, draw.io XML/.drawio -> PNG/SVG/PDF, or draw.io XML/.drawio -> semantic Mermaid.
---

# drawio-mermaid

Use this skill when the user asks for any of these draw.io / diagrams.net conversion tasks:

- Mermaid -> draw.io / diagrams.net editable diagram.
- draw.io XML / `.drawio` / `.drawio.svg` -> PNG, SVG, or PDF.
- draw.io XML / `.drawio` / bare `<mxGraphModel>` -> semantic Mermaid.

This skill is prompt-first for official draw.io capabilities: do not copy external scripts for Mermaid insertion or PNG/SVG/PDF export. Use the official draw.io Desktop CLI or draw.io UI behavior directly.

## Official Capability Map

| Direction | Status | Use This Path |
| --- | --- | --- |
| Mermaid -> draw.io | Officially supported | Prefer draw.io Desktop CLI for files; otherwise use the draw.io Mermaid insert dialog. |
| draw.io XML -> PNG/SVG/PDF | Officially supported | Prefer draw.io Desktop CLI export; otherwise use File > Export as in the UI. |
| draw.io XML -> Mermaid | Not a first-party draw.io export | Use this repository's `drawio-mermaid` converter. |

Official references used for this prompt:

- draw.io Mermaid manual: `https://www.drawio.com/docs/manual/mermaid/`
- draw.io insert Mermaid manual: `https://www.drawio.com/docs/manual/insert/insert-mermaid/`
- draw.io export diagram manual: `https://www.drawio.com/docs/manual/export/export-diagram/`
- draw.io Desktop CLI implementation: `https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js`
- draw.io Desktop releases: `https://github.com/jgraph/drawio-desktop/releases`

## Mermaid -> draw.io

Use this workflow when the input is `.mmd`, `.mermaid`, or raw Mermaid text and the requested output is draw.io / diagrams.net.

1. Save raw Mermaid text to a `.mmd` file if the user provided inline Mermaid.
2. Prefer draw.io Desktop CLI export/import behavior when the local `draw.io` binary exists. The official CLI accepts Mermaid inputs for export and can open `.mmd` / `.mermaid` as editable diagrams by default.
3. Generate a draw.io XML file with:

   ```bash
   draw.io --export --format xml --output output.drawio input.mmd
   ```

4. If the user wants Mermaid preserved as a static rendered image instead of an editable diagram, add:

   ```bash
   draw.io --export --format xml --mermaid-image true --output output.drawio input.mmd
   ```

5. If the CLI is unavailable, tell the user to use the official UI path: open draw.io / diagrams.net, choose `Insert > Advanced > Mermaid`, paste the Mermaid definition, then insert it. For editing later, select the inserted Mermaid diagram and use the Mermaid edit action from the UI.
6. Validate by opening the generated `.drawio` file or exporting a quick PNG preview.

Notes:

- Mermaid syntax support follows draw.io's bundled Mermaid renderer, not this repository.
- For best editability, keep node IDs and labels Mermaid-compatible and avoid unsupported Mermaid beta syntax unless draw.io accepts it.
- If CLI conversion fails on complex Mermaid, retry through the UI insert dialog; if both fail, simplify unsupported Mermaid constructs and report the changed constructs.

## draw.io XML -> PNG/SVG/PDF

Use this workflow when the input is `.drawio`, `.xml`, `.drawio.svg`, a folder of diagrams, or another draw.io-supported file and the requested output is a rendered asset.

### Preferred CLI

Use draw.io Desktop from the command line:

```bash
draw.io --export --format png --output output.png input.drawio
draw.io --export --format svg --output output.svg input.drawio
draw.io --export --format pdf --output output.pdf input.drawio
```

If the output filename has an extension, draw.io determines the output type from that extension and ignores `--format`.

### Common Export Options

- `--output <file|folder>`: write to an explicit output path.
- `--format <pdf|svg|png|jpeg|jpg|xml|html>`: choose output format when the output extension is not enough.
- `--page-index <n>` / `-p <n>`: export a specific 1-based page; image formats default to the first page when omitted.
- `--all-pages` / `-a`: export all pages for PDF and HTML.
- `--page-range <from>..<to>` / `-g <from>..<to>`: export a 1-based page range for PDF.
- `--transparent` / `-t`: transparent background for PNG and SVG.
- `--embed-diagram` / `-e`: embed a copy of the diagram in PNG, SVG, or PDF.
- `--embed-svg-images`: embed images in SVG output.
- `--embed-svg-fonts true|false`: control SVG font embedding; default is true.
- `--border <px>` / `-b <px>`: add border around the diagram.
- `--scale <number>` / `-s <number>`: scale diagram size.
- `--width <px>` or `--height <px>`: fit output into a target dimension while preserving aspect ratio.
- `--crop`: crop PDF to diagram size.
- `--layers <comma separated indexes>`: export selected layers.
- `--recursive` / `-r`: recursively export folder inputs.
- `--layout <name|json>`: run a layout before export; official preset names include `verticalFlow`, `horizontalFlow`, `verticalTree`, `horizontalTree`, `radialTree`, and `organic`.

### Recipes

```bash
# Transparent SVG, preserving the source diagram for future editing.
draw.io -x -f svg -t -e -o output.svg input.drawio

# Cropped PDF for docs.
draw.io -x -f pdf --crop -o output.pdf input.drawio

# Export page 2 as a high-resolution PNG.
draw.io -x -f png -p 2 -s 2 -b 8 -o page2.png input.drawio

# Export all pages to PDF.
draw.io -x -f pdf -a -o all-pages.pdf input.drawio

# Recursively export a folder to SVG files.
draw.io -x -r -f svg -o exported-svg diagrams/
```

### UI Fallback

If draw.io Desktop CLI is unavailable, open the file in draw.io / diagrams.net and use `File > Export as > PNG/SVG/PDF`. Match the user's requested page, transparency, embedding, crop, border, and scale settings in the export dialog.

## draw.io XML -> Mermaid

Use this repository's converter only for semantic Mermaid extraction from draw.io XML. This is not an official draw.io export.

1. Locate the source `.drawio` or `.xml` file. Accept standard `<mxfile><diagram>...` files and bare `<mxGraphModel>...` files.
2. Prefer the bundled wrapper script when the skill is installed from the skill repo:

   ```bash
   node skill/drawio-mermaid/scripts/convert.mjs input.drawio -o output.mmd
   ```

3. If running from the `drawio-mermaid` project root, call the CLI directly:

   ```bash
   node src/cli.mjs input.drawio -o output.mmd
   ```

4. Use `--diagram auto` by default. Override only when the user knows the intended diagram type:

   ```bash
   node src/cli.mjs input.xml --diagram architecture -o architecture.mmd
   node src/cli.mjs input.drawio --diagram class -o class.mmd
   node src/cli.mjs input.drawio --diagram sequence -o sequence.mmd
   node src/cli.mjs input.drawio --diagram er -o er.mmd
   ```

5. Use `--mode flowchart` only when the user explicitly wants all diagrams represented as Mermaid `flowchart` / `subgraph` instead of Mermaid native UML/ER syntax.
6. For multi-page draw.io files, use `--page <name|index>`; page indexes are 1-based for users.
7. Inspect stderr warnings. Missing `source` / `target` edges are skipped intentionally and should be mentioned if they affect the result.

Supported semantic outputs:

- Flowchart and swimlane/container process diagrams: Mermaid `flowchart TD` with `subgraph` hierarchy.
- Architecture and component dependency diagrams: Mermaid `flowchart TD` with nested `subgraph` containers.
- UML class diagrams: Mermaid `classDiagram`.
- UML sequence diagrams: Mermaid `sequenceDiagram`.
- Simple ER diagrams: Mermaid `erDiagram`.

## Quality Bar

- Preserve semantic structure over pixels: containers, groups, labels, edges, UML/ER relationships, and service/component dependencies matter most.
- Do not promise pixel-perfect round-tripping between Mermaid and draw.io XML.
- For official draw.io export work, use draw.io Desktop/UI behavior rather than adding conversion scripts to this skill.
- If a requested conversion depends on local draw.io Desktop, first check whether `draw.io` or the platform binary is installed, then provide the exact command used or the fallback UI steps.
