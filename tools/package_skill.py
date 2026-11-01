"""Package the declared Fashion Design Studio skill files, without local caches."""

from pathlib import Path
import hashlib
import zipfile

FILES = (
    "SKILL.md", "LICENSE", "agents/openai.yaml", "assets/icon.svg",
    "references/design-brief.json", "references/host-capabilities.md",
    "references/svg-options.md", "references/visual-directions.md",
    "scripts/render_flats.py",
)


def main():
    root = Path(__file__).resolve().parent.parent
    source = root / "fashion-design-studio"
    output = root / "downloads" / "fashion-design-studio.zip"
    for name in FILES:
        if not (source / name).is_file():
            raise SystemExit(f"Required skill file is missing: {name}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in FILES:
            info = zipfile.ZipInfo("fashion-design-studio/" + name, date_time=(2026, 11, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (source / name).read_bytes())
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(FILES)
        for name in FILES:
            assert archive.read("fashion-design-studio/" + name) == (source / name).read_bytes()
    print(output)
    print("SHA-256: " + hashlib.sha256(output.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
