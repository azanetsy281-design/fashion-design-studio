# Bundled SVG renderer

Use `scripts/render_flats.py` for a small, reproducible illustrated front/back sheet.
Require Python 3.10 or newer. Use no network or third-party packages. Output is
editable SVG, not a photograph, a cutting pattern or a measurement-based draft.

Pass a JSON object using these supported fields:

| Field | Values / default |
| --- | --- |
| `title` | A short concept name, at most 80 characters; default `Garment concept` |
| `garment` | `top`, `dress`, `skirt`; required |
| `audience` | `adult`, `child`; default `adult` (concept context only) |
| `silhouette` | `straight`, `a-line`; default `straight` for top, otherwise `a-line` |
| `length` | `cropped`, `regular`, `long`; default `regular`; cropped is top-only |
| `colour` | Six-digit CSS hex; default `#71866f` |
| `accent` | Six-digit CSS hex; default `#eee2ce` |
| `print` | `solid`, `dots`, `stripes`, `floral`; default `solid` |
| `pockets` | `none`, `patch`; default `none`; patch pockets are front-only |
| `front_closure` | `none`, `buttons`; default `none` |
| `back_closure` | `none`, `buttons`, `zip`; default `none` |
| `neckline` | Top/dress only: `round`, `v`, `square`; default `round` |
| `sleeves` | Top/dress only: `none`, `short`, `long`, `flutter`; default `short` |

Store extra creative notes separately in the concept brief. The renderer rejects
unknown fields and unsupported combinations rather than ignoring them. A skirt
must not include neckline/sleeves or use a cropped length. User-selected details
outside this table need a custom SVG or a capable image tool; do not quietly
replace them with supported defaults.

Example command:

```sh
python3 <skill-directory>/scripts/render_flats.py --input design.json --output design-front-back.svg
```

For a complete minimal input example, see `design-brief.json` beside this file.
Run `--help` for CLI usage. The two views share a deterministic silhouette but
use a higher back neckline and the declared side-specific closures/pockets.
Audience changes the visual proportions slightly; it never derives garment size.
