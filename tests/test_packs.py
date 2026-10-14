"""The packs of this repository: each built on the engine's own vocabularies. Each checks clean
(`oto pack check`), and each embeds exactly the engine's shipped copy of every ontology it carries:
when the engine changes one, `oto pack refresh packs/<name>` re-embeds it and this test says so
until then. Needs the engine importable (the CI installs oto-kg at the release it pins)."""
import filecmp
import json
import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS = sorted(p.name for p in (ROOT / "packs").iterdir() if (p / "manifest.json").exists())
PROVENANCE = ("source", "path", "ref", "commit", "registry", "fetched_at", "_about")

oto = pytest.importorskip("oto")


@pytest.fixture(autouse=True)
def bare_machine(tmp_path, monkeypatch):
    """Only the engine's shipped ontologies: none of the machine's own, none from installed packs."""
    monkeypatch.setenv("OTO_ONTOLOGIES", str(tmp_path / "no-ontologies"))
    monkeypatch.setenv("OTO_PACKS", str(tmp_path / "no-packs"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "no-claude"))


def _manifest(path):
    manifest = json.load(open(os.path.join(path, "manifest.json"), encoding="utf-8"))
    return {k: v for k, v in manifest.items() if k not in PROVENANCE}


def _same(a, b):
    """The same files; a manifest compared without the provenance that embedding it records."""
    if os.path.exists(os.path.join(a, "manifest.json")) and _manifest(a) != _manifest(b):
        return False
    cmp = filecmp.dircmp(a, b, ignore=[".DS_Store", "__pycache__", "manifest.json"])
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    if filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)[1:] != ([], []):
        return False
    return all(_same(os.path.join(a, d), os.path.join(b, d)) for d in cmp.common_dirs)


def test_there_are_packs():
    assert {"prd-architecture-studio", "ddd", "work"} <= set(PACKS)


@pytest.mark.parametrize("pack", PACKS)
def test_the_pack_checks_clean(pack):
    from oto.model import packs
    assert packs.check(str(ROOT / "packs" / pack)) == []


@pytest.mark.parametrize("pack", PACKS)
def test_the_pack_embeds_the_engines_own_ontologies(pack):
    from oto.model import ontologies
    embedded = ROOT / "packs" / pack / "ontology"
    for unit in sorted(os.listdir(embedded)):
        shipped = ontologies.dir_for(unit)
        assert shipped and ontologies.origin(unit) == ontologies.BUILTIN, \
            "%s embeds %s, which the engine does not ship: it belongs in the repository of that ontology" % (pack, unit)
        assert _same(str(embedded / unit), shipped), \
            "packs/%s embeds an outdated %s: oto pack refresh packs/%s" % (pack, unit, pack)


def test_the_architecture_skill_finds_patterns_and_never_names_them():
    """A new pattern pack must not need an edit here: architecture-build reads the project's patterns
    from `oto status --json` (each pack's `pattern`) and names none of them."""
    text = (ROOT / "packs" / "software-architecture" / "skills" / "architecture-build" / "SKILL.md").read_text(encoding="utf-8")
    assert "oto status --project <root> --json" in text and "`pattern`" in text and "`for`" in text and "`skill`" in text
    for name in ("ddd", "medallion", "model-domain", "design-pipeline", "bounded context", "bronze"):
        assert name not in text.lower(), "architecture-build names %r: a pattern should be found, not named" % name
    for pack in PACKS:
        manifest = json.load(open(ROOT / "packs" / pack / "manifest.json", encoding="utf-8"))
        if manifest.get("pattern"):
            assert manifest["pattern"]["of"] == "software-architecture", pack
