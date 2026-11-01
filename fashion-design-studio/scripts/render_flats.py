"""Render a small, editable front/back fashion concept sheet, not a cutting pattern."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import textwrap
import xml.etree.ElementTree as ET


def validate(raw):
    if not isinstance(raw, dict):
        raise ValueError("Input must be one JSON object.")
    defaults = {
        "title": "Garment concept", "audience": "adult", "length": "regular",
        "colour": "#71866f", "accent": "#eee2ce", "print": "solid",
        "pockets": "none", "front_closure": "none", "back_closure": "none",
    }
    garment = raw.get("garment")
    if garment not in {"top", "dress", "skirt"}:
        raise ValueError("garment must be top, dress or skirt.")
    defaults["silhouette"] = "straight" if garment == "top" else "a-line"
    if garment != "skirt":
        defaults.update(neckline="round", sleeves="short")
    allowed = set(defaults) | {"garment"}
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError("Unsupported fields for this garment: " + ", ".join(sorted(unknown)))
    design = {**defaults, **raw}
    if any(not isinstance(value, str) for value in design.values()):
        raise ValueError("All design values must be strings.")
    choices = {
        "audience": {"adult", "child"}, "silhouette": {"straight", "a-line"},
        "length": {"cropped", "regular", "long"}, "print": {"solid", "dots", "stripes", "floral"},
        "pockets": {"none", "patch"}, "front_closure": {"none", "buttons"},
        "back_closure": {"none", "buttons", "zip"},
        "neckline": {"round", "v", "square"}, "sleeves": {"none", "short", "long", "flutter"},
    }
    for key, options in choices.items():
        if key in design and design[key] not in options:
            raise ValueError(f"{key} must be one of: {', '.join(sorted(options))}.")
    if garment != "top" and design["length"] == "cropped":
        raise ValueError("cropped length is supported only for a top.")
    if not 1 <= len(design["title"].strip()) <= 80 or re.search(r"[\x00-\x1f]", design["title"]):
        raise ValueError("title must contain 1–80 characters without control characters.")
    for key in ("colour", "accent"):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", design[key]):
            raise ValueError(f"{key} must be a six-digit hex colour, for example #71866f.")
    return design


def add(parent, tag, **attrs):
    return ET.SubElement(parent, tag, {key.replace("_", "-"): str(value) for key, value in attrs.items()})


def text(parent, value, x, y, size=22, **attrs):
    node = add(parent, "text", x=x, y=y, font_size=size, **attrs)
    node.text = value
    return node


def pattern(defs, design):
    motif = design["print"]
    if motif == "solid":
        return design["colour"]
    tile = add(defs, "pattern", id="fabric-print", width=42, height=42, patternUnits="userSpaceOnUse")
    add(tile, "rect", width=42, height=42, fill=design["colour"])
    if motif == "dots":
        add(tile, "circle", cx=12, cy=12, r=3.5, fill=design["accent"])
        add(tile, "circle", cx=33, cy=33, r=3.5, fill=design["accent"])
    elif motif == "stripes":
        add(tile, "rect", x=9, y=0, width=7, height=42, fill=design["accent"], opacity="0.7")
        add(tile, "rect", x=30, y=0, width=7, height=42, fill=design["accent"], opacity="0.7")
    else:
        for cx, cy in ((17, 12), (23, 16), (21, 23), (13, 23), (10, 16)):
            add(tile, "circle", cx=cx, cy=cy, r=4.2, fill=design["accent"], opacity="0.85")
        add(tile, "circle", cx=17, cy=18, r=3.2, fill="#bc985e")
    return "url(#fabric-print)"


def geometry(design, back=False):
    garment = design["garment"]
    if garment == "skirt":
        hem_y = 670 if design["length"] == "regular" else 800
        hem_w = 280 if design["silhouette"] == "a-line" else 175
        outline = f"M -150 130 Q 0 112 150 130 L {hem_w} {hem_y} Q 0 {hem_y + 18} {-hem_w} {hem_y} Z"
        return outline, hem_y, hem_w, 280
    if garment == "top":
        hem_y = {"cropped": 425, "regular": 520, "long": 610}[design["length"]]
        hem_w = 205 if design["silhouette"] == "a-line" else 165
    else:
        hem_y = 735 if design["length"] == "regular" else 860
        hem_w = 270 if design["silhouette"] == "a-line" else 180
    sleeves = design["sleeves"]
    left = {
        "none": "Q -128 174 -155 225",
        "short": "L -230 165 L -195 230 L -155 205",
        "long": "L -305 460 L -245 480 L -155 205",
        "flutter": "L -230 165 Q -218 247 -168 230 L -155 205",
    }[sleeves]
    right = {
        "none": "Q 128 174 145 105",
        "short": "L 195 230 L 230 165 L 145 105",
        "long": "L 245 480 L 305 460 L 145 105",
        "flutter": "L 168 230 Q 218 247 230 165 L 145 105",
    }[sleeves]
    neck = ("C 55 135 -55 135 -70 100" if back else {
        "round": "C 55 180 -55 180 -70 100",
        "v": "L 0 195 L -70 100",
        "square": "L 70 175 L -70 175 L -70 100",
    }[design["neckline"]])
    underarm = 225 if sleeves == "none" else 205
    outline = f"M -70 100 L -145 105 {left} L {-hem_w} {hem_y} Q 0 {hem_y + 12} {hem_w} {hem_y} L 155 {underarm} {right} L 70 100 {neck} Z"
    return outline, hem_y, hem_w, 305 if sleeves == "long" else 270


def garment_view(parent, design, fill, back=False):
    side = "back" if back else "front"
    outline, hem_y, hem_w, max_width = geometry(design, back)
    scale = min(1.2, 300 / max_width, 710 / (hem_y - 100))
    anchor = 1170 if back else 430
    outer = add(parent, "g", id=f"{side}-view", transform=f"translate({anchor}, {275 - 100 * scale:.3f}) scale({scale:.5f})")
    group = add(outer, "g", transform="scale(1.04, 0.94)" if design["audience"] == "child" else "scale(1)")
    add(group, "path", id=f"{side}-body", d=outline, fill=fill, stroke="#263b3b", stroke_width=3, stroke_linejoin="round")
    if design["garment"] == "skirt":
        add(group, "path", d="M -153 154 Q 0 136 153 154", fill="none", stroke=design["accent"], stroke_width=8)
        closure_start = 158
    else:
        neck = ("M 70 100 C 55 135 -55 135 -70 100" if back else {
            "round": "M 70 100 C 55 180 -55 180 -70 100",
            "v": "M 70 100 L 0 195 L -70 100",
            "square": "M 70 100 L 70 175 L -70 175 L -70 100",
        }[design["neckline"]])
        add(group, "path", d=neck, fill="none", stroke=design["accent"], stroke_width=7, stroke_linejoin="round")
        closure_start = 147 if back else {"round": 177, "v": 212, "square": 192}[design["neckline"]]
        if design["garment"] == "dress":
            # Conceptual waist seam; no real-world measurement is implied.
            underarm = 225 if design["sleeves"] == "none" else 205
            waist_w = 155 + (hem_w - 155) * (350 - underarm) / (hem_y - underarm)
            add(group, "path", d=f"M {-waist_w:.2f} 350 Q 0 360 {waist_w:.2f} 350", fill="none", stroke=design["accent"], stroke_width=5)
    add(group, "path", d=f"M {-hem_w + 5} {hem_y - 13} Q 0 {hem_y - 2} {hem_w - 5} {hem_y - 13}", fill="none", stroke="#314743", stroke_width=1.7, stroke_dasharray="5 5")
    if not back and design["pockets"] == "patch":
        pocket_y = 300 if design["garment"] == "top" else 410
        if design["garment"] == "skirt":
            pocket_y = 285
        for x, label in ((-135, "left"), (70, "right")):
            add(group, "path", id=f"front-pocket-{label}", d=f"M {x} {pocket_y} h 65 v 65 q -32 25 -65 0 Z", fill=design["accent"], stroke="#263b3b", stroke_width=2)
            add(group, "path", d=f"M {x + 5} {pocket_y + 9} h 55", stroke="#5b6c63", fill="none", stroke_width=1.5)
    closure = design[f"{side}_closure"]
    if closure != "none":
        details = add(group, "g", id=f"{side}-closure")
        end = min(hem_y - 35, closure_start + 230) if closure == "zip" else hem_y - 35
        add(details, "path", d=f"M 0 {closure_start} V {end}", fill="none", stroke=design["accent"], stroke_width=5 if closure == "buttons" else 3)
        if closure == "zip":
            add(details, "path", d=f"M 0 {closure_start} V {end}", fill="none", stroke="#344c47", stroke_width=2, stroke_dasharray="3 4")
            add(details, "rect", x=-4, y=closure_start, width=8, height=15, rx=2, fill="#b5955c")
        else:
            for y in range(int(closure_start + 14), int(end), 48):
                add(details, "circle", cx=0, cy=y, r=5, fill=design["accent"], stroke="#344c47", stroke_width=1.5)


def render(raw):
    design = validate(raw)
    root = ET.Element("svg", {"xmlns": "http://www.w3.org/2000/svg", "width": "1600", "height": "1190", "viewBox": "0 0 1600 1190", "role": "img", "aria-labelledby": "sheet-title sheet-description"})
    add(root, "title", id="sheet-title").text = design["title"]
    add(root, "desc", id="sheet-description").text = "Editable illustrated front and back garment concept; not a cutting pattern."
    defs = add(root, "defs")
    fill = pattern(defs, design)
    add(root, "rect", width=1600, height=1190, fill="#f4f1eb")
    board = add(root, "g", font_family="Arial, Helvetica, sans-serif", fill="#253a38")
    text(board, "FASHION DESIGN STUDIO", 80, 48, 16, letter_spacing=3)
    title_lines = textwrap.wrap(design["title"], width=53) or [design["title"]]
    for index, line in enumerate(title_lines):
        text(board, line, 80, 93 + index * 32, 29, font_weight=600)
    for x, label in ((80, "FRONT"), (850, "BACK")):
        add(board, "rect", x=x, y=157, width=670, height=875, rx=25, fill="#fffefa", stroke="#dedbd3", stroke_width=2)
        text(board, label, x + 335, 209, 18, text_anchor="middle", letter_spacing=3)
    garment_view(board, design, fill, back=False)
    garment_view(board, design, fill, back=True)
    text(board, f"{design['audience'].capitalize()} {design['garment']} concept · {design['silhouette']} · {design['length']} length", 80, 1082, 22)
    for x, colour in ((1220, design["colour"]), (1375, design["accent"])):
        add(board, "circle", cx=x, cy=1076, r=17, fill=colour, stroke="#b9b9ad", stroke_width=1)
        text(board, colour, x + 24, 1082, 16)
    text(board, "Illustrated design concept · Not a cutting pattern · No fit or measurement validation", 80, 1143, 18, fill="#68746b")
    ET.indent(root, space="  ")
    return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Design JSON object")
    parser.add_argument("--output", required=True, type=Path, help="Output .svg file")
    args = parser.parse_args(argv)
    try:
        if args.output.suffix.lower() != ".svg":
            raise ValueError("Output filename must end in .svg.")
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output must be different files.")
        if args.input.stat().st_size > 1024 * 1024:
            raise ValueError("Design JSON exceeds 1 MiB.")
        raw = json.loads(args.input.read_text(encoding="utf-8-sig"))
        svg = render(raw)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(svg, encoding="utf-8")
        print(args.output)
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Cannot render design: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
