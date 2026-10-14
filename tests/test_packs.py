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
    assert {"product", "software-architecture", "ddd", "work"} <= set(PACKS)
    assert "prd-architecture-studio" not in PACKS, "the studio is the project's assembled site, not a pack"


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


def test_no_pack_keeps_an_elicit_skill_or_names_the_studio():
    """The confirmation menu is capture-form's own (engine 0.11.20), and the studio is no plugin any more."""
    for pack in PACKS:
        assert not (ROOT / "packs" / pack / "skills" / "elicit").exists(), pack
        for skill in (ROOT / "packs" / pack / "skills").glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            assert "**elicit**" not in text and "elicit skill" not in text, skill
            assert "a studio's" not in text and "--pack <studio>" not in text, skill


def test_atlas_is_the_product_packs_playbook_and_leaves_orientation_to_the_concierge():
    manifest = json.load(open(ROOT / "packs" / "product" / "manifest.json", encoding="utf-8"))
    assert manifest["playbook"]["skill"] == "atlas"
    text = (ROOT / "packs" / "product" / "skills" / "atlas" / "SKILL.md").read_text(encoding="utf-8")
    assert "**Where are we**" not in text and "concierge" in text
    assert "7. **Where are we**" not in text


def test_every_pack_skill_talks_in_plain_language():
    """Technical details are the record's: no skill talks in codes, ids or engine output, and none
    offers them; the start skills get the same rule from the engine (0.11.22)."""
    for pack in PACKS:
        for skill in sorted((ROOT / "packs" / pack / "skills").glob("*/SKILL.md")):
            text = skill.read_text(encoding="utf-8")
            assert text.count("## Talking with the person") == 1, skill
            assert "Never offer them" in text, skill
            assert "engine's words" not in text and "N of M" not in text, skill


def test_atlas_speaks_plainly_again():
    text = (ROOT / "packs" / "product" / "skills" / "atlas" / "SKILL.md").read_text(encoding="utf-8")
    assert "Holding here" in text and "— Atlas" in text and "(scene 1)" not in text
    assert "**Start a new product**" in text and "**Describe what it must do**" in text
