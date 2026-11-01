---
name: fashion-design-studio
description: Create or revise original garment concepts with matching front/back previews and colourways. Use for fashion ideas or reference-led redesigns; exclude cutting patterns, sizing and sewing instructions.
---

# Fashion Design Studio

Create garment concepts and actual visual previews from text, sketches or reference
photos. Work in the user's language; accept Roman Urdu naturally. Deliver designs,
not a website, app, pattern-making program or text-only list of ideas.

## 1. Read the brief

- Extract garment type, wearer category, style, colours, fabric appearance,
  requested views, and details to keep or change. Treat an age range as design
  context, not a validated size range.
- Use details already supplied. For a vague new request, ask at most two short
  questions: which garment/wearer, and which style/colour direction. If the user
  says to choose, choose and state the assumptions briefly; proceed.
- Default to one wearable concept, front on the left and back on the right, with
  a neutral background. Include detail views only when requested or necessary
  to explain the concept. Respect an explicit count or requested view layout.
- Inspect supplied reference images before interpreting them. Distinguish visible
  details from proposed details. Mark an unseen back as a proposed back view in
  the brief. Request a missing attachment only when it is necessary to edit that
  exact image. Use broad style cues without importing unrelated logos/artwork.
- Keep new concepts separate from unrelated garments in previous messages.

## 2. Choose a visual route from actual host capabilities

Follow the host's tool instructions and the user's requested medium. Do not assume
that installing a skill adds an image model, API access or an external account.

| Available capability / request | Action |
| --- | --- |
| Image generation is available; a realistic preview is requested or suitable | Generate a paired front/back image with the available image tool. Read [visual-directions.md](references/visual-directions.md). |
| A fashion flat, vector drawing or editable SVG is requested | Create an SVG design sheet. Use the bundled renderer for supported options, or draw a custom SVG for other garment details. |
| No image tool, but code execution or SVG artifacts are available | Explain in one sentence that the preview will be an illustrated fashion flat. Produce an actual SVG; do not stop at a prompt. |
| No visual/file/artifact capability is available | Provide a concept brief and a reusable image prompt; clearly state that the visual has not been generated. |

For template-based SVGs, read [svg-options.md](references/svg-options.md). Run:

```sh
python3 <skill-directory>/scripts/render_flats.py --input design.json --output design-front-back.svg
```

Write output into the user's working/output directory, never into this installed
skill. The script uses only the Python standard library. Do not install packages
or call paid APIs for it. On hosts with SVG artifacts but no shell, create an SVG
artifact directly using the same front/back consistency checks.

Treat the templates as starting silhouettes. Use custom SVG geometry for a feature
the renderer does not support; never silently drop a requested detail or label a
template as an exact interpretation of a reference. When a requested photographic
edit is unavailable, distinguish a proposed vector interpretation from an edited
photograph. Do not claim that Claude has native photographic image generation.

## 3. Resolve one coherent concept

- Select a silhouette, length, neckline, sleeves, material appearance and colour
  palette that work together. Describe texture and drape as a proposal.
- Keep both views of the same garment consistent: colour, sleeve length, hem,
  seam placement, straps, pockets and closures. Show appropriate front/back
  differences; do not mirror the front and call it the back.
- Make the concept visually understandable: include a plausible entry/closure
  where needed and avoid accidentally changing garment type.
- Use uncluttered garment-only views by default. Do not introduce a model,
  accessories, branding or marketing text unless requested.
- Keep visual proportions conceptual. Do not invent centimetre dimensions,
  measurement-derived geometry, grading or printable cutting lines.

## 4. Make and inspect the visual

- Show the actual generated image, SVG artifact or rendered vector preview when
  the host can display it. Provide the real downloadable output when supported.
  Do not substitute source code blocks for a visual the host can render.
- For image work, attach available target references according to the host's
  image-editing rules. Preserve accepted images and unaffected details during
  revisions; change only what the user requested or a confirmed visual defect.
- For vectors, keep the SVG editable and self-contained. Avoid external images,
  scripts, network links and tracing a photo into supposed pattern geometry.
- Check requested garment, front/back agreement, all requested details, cropping,
  fabric/colour agreement, obvious impossible joins and stray text. Inspect with
  the host's rendering/viewing tools when available; otherwise validate SVG XML
  and explicitly distinguish structural validation from visual inspection.
- Correct confirmed defects with a bounded local revision. Do not regenerate an
  accepted asset just to produce another version. If rendering/generation fails,
  preserve the brief and label the visual pending; never report it complete.

## 5. Deliver compactly

Return the visual first, then a short brief with:

- Concept name and intended wearer/category.
- Main silhouette, neckline/sleeves, front/back details and palette.
- Suggested material appearance and any assumptions, including an inferred back.
- A short note that it is a design concept, not a validated cutting pattern.

Offer named revisions only when helpful, without adding an approval gate. When
files are supported, retain `design.json` as the chosen renderer input. Record
custom SVG edits in `design-brief.md`; JSON alone does not reproduce manual edits.
Follow the host's normal file-saving rules.
Use [design-brief.json](references/design-brief.json) as an input example, replacing
its values with the user's choices. Do not call a raster preview editable SVG.
Do not promise PNG/PDF export unless those files were actually produced.

## Boundaries

Create designs only. Leave cutting pieces, body/finished measurement tables,
grading, pattern PDFs, seam allowances, cutting instructions, sewing tutorials,
listings and video production to separate workflows. If asked for those, explain
the scope and ask whether to start that separate task; do not present this
concept as tested fit or manufacture-ready geometry.

Read [host-capabilities.md](references/host-capabilities.md) when platform
compatibility, missing tools or installing this skill is material. Respect the
host's current rules over examples in this package.
