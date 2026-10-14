# OTO packs

The [OTO](https://github.com/Cynergis/oto) packs built on the engine's own vocabularies, maintained
here and published from here to the registry, [Cynergis/oto-registry](https://github.com/Cynergis/oto-registry).
A pack is one vocabulary, the skills that use it and the views that show it. Packs built on an
ontology that lives in its own repository are kept with it instead (`report`, `product-report` and
`flow` in [report-ontology](https://github.com/Cynergis/report-ontology); `medallion` and
`report-medallion` in [medallion-ontology](https://github.com/Cynergis/medallion-ontology)).

| Pack | Vocabulary | What it brings |
|---|---|---|
| `prd-architecture-studio` | `software-architecture` | Atlas and the studio's skills, and the `prd-site` view (below; to be split into a `product` and a `software-architecture` pack) |
| `ddd` | `ddd` | Domain-driven design for a part of a product: `model-domain` |
| `work` | `work` | Work items and milestones over a product's requirements, features and components |
| `auto-claims` | `auto-claims` | Motor vehicle claims: policy, coverage, claim, incident, handling, money in and out |
| `organization-process` | `organization-process` | How an organisation works: units, roles, processes, policies, systems and measures |
| `professional-services` | `professional-services` | Engagements: scope, deliverables, governance, sessions, decisions and the work that follows |

This repository was `prd-architecture-studio` until 2026-10-14; GitHub redirects the old name.

## Changing a pack, and releasing it

1. Change it here, in `packs/<name>/`: its skills and views by hand, its embedded ontologies only by
   `oto pack refresh packs/<name>` (they are the engine's shipped copies).
2. `python -m pytest -q tests/test_packs.py`: every pack checks clean and embeds exactly the
   engine's copy of each ontology it carries, at the engine release CI pins
   (`.github/workflows/packs.yml`). When the engine changes a vocabulary, move the pin and refresh
   the packs together.
3. Publish it, from here and never from `~/.oto/packs`, on a branch of the registry, then open the
   registry pull request:

   ```bash
   oto pack publish --from packs/<name> --to https://github.com/Cynergis/oto-registry.git --ref <branch> --note "<what changed>"
   ```

The registry numbers the release; a pack's `manifest.json` here carries the release and changelog it
was last published with.

## Layout

| Path | Contents |
|---|---|
| `packs/<name>/` | A pack: `manifest.json` (its release, the ontology it embeds, the engine it needs), `ontology/` (the embedded ontology and its bases, written by `oto pack refresh`), `skills/`, `views/`; `.claude-plugin/plugin.json` and `skills/start/` are generated. |
| `tests/test_packs.py` | Every pack checks clean and matches the engine's ontologies. |
| `tests/test_scenes.py`, `fixtures/` | The studio's scenes on a report product, scripted; not published. |
| `GETTING-STARTED.md`, `WALKTHROUGH.md`, `PUBLISH.md`, `publish-plugins.sh` | The studio's guides. |

CI also refuses client names and credentials (`oto publishable --strict`, `.github/workflows/publishable.yml`).

## The PRD & Architecture Studio pack

Atlas, the Lead Product Engineer, and the skills that carry a product from an idea to a published
knowledge base that other people query. The studio is the front door of [OTO](https://github.com/Cynergis/oto)'s
arc: it captures a product's specification and design **against OTO packs**, contributes every
confirmed section to the knowledge base **as it goes**, through the curate gates, and carries no
graph of its own.

It is an **OTO pack**, `packs/prd-architecture-studio/`: its skills, the vocabulary every product
shares (`software-architecture`, which brings `product` and `portfolio`: the specification and a
pattern-neutral architecture) and the `prd-site` view, released and checked together (`oto pack
check`). A product starts from the pack with its type, the design patterns its parts follow and
the flow merged beside it:

```bash
oto init --empty --pack prd-architecture-studio --ontology product-report,ddd,flow --project <root>
```

Atlas runs that in scene 1. A pattern is per part, not per product: DDD for an application (the
`ddd` pack), the medallion pattern for its data pipeline (the `medallion` pack, with
`report-medallion` when a report reads it), or none. The site's DDD pages are optional
(`$optional`), so they fill only in a product that adds `ddd`. It needs OTO 0.11.12 or later, which
finds the ontology of an installed pack by name, declares the plugins the project uses in its
`.claude/settings.json`, and records the tools in `oto.lock.json` (commit both).

### The arc

```
1 Start ─► 2 Specify ─► 3 Derive the domain ─► 4 Design and flow ─► 5 Build ─► 6 Publish ─► 7 Readers
```

| Skill | What it does |
|---|---|
| **atlas** | The one owner of the arc. "Atlas, lead this product." Asks which kind of product and what you have, then runs the scenes, stopping at every gate; "run the studio" runs them all in one go. Orients with `oto status`; never voices a second persona. |
| **elicit** | The elicitation: runs OTO's **capture-form** on a pack's `capture.json` (the questions by asker, the classes with their fields and links, every field carrying its term) with the BMAD menu at every confirmation (**[A]** elicit, **[P]** perspectives, **[C]** continue); on every **C** the section goes through `oto curate propose`, `add` and `check`, and the graph's answers are reported (`oto query questions`). |
| **prd-build** | The specification, captured against `product` (in the pack) and the product type merged beside it (`product-report`, …). |
| **architecture-build** | The design: the architecture against `software-architecture` (in the pack), then each part with the pattern it follows, modelled by the pattern's pack (`ddd:model-domain` for DDD, `medallion:design-pipeline` for a data pipeline). |
| **feature-flow** | A feature through the gates, read from the graph: the idea against the product's purpose (`kg_ask`), the impact on the design and the flow (`kg_neighbors`, `kg_brief impact-*`), the scenarios, then each step test-first through the flow pack's **implement-step** — BLOCKED by name until the missing fact is captured. |
| **prd-site** | The navigable site, the pack's view `prd-site`, installed in the project when it starts from the pack: `data.js` is written from the graph by the engine on every build, never by hand. |

What left in version 2: `knowledge-graph` and the mesh ontology (the packs are the ontology; the
knowledge base is the graph), the built-in section lists of `prd-build` and `architecture-build`
(the capture schema is the form), and `data.js` as the source of truth (it is a projection).
In 2.1.0: `studio` folded into `atlas` ("run the studio" still works), `capture` renamed `elicit`
so it is not mistaken for OTO's `capture`. After 2.1.1 the studio became a pack: its version
follows the pack's release (`<release>.0.0`, from 1.0.0), so an installed 2.x plugin is
uninstalled and the pack installed, not updated.

### How it fits with OTO

```
pack (ontology + questions)  ──oto ontology capture──►  capture.json  ──elicit skill───►  captures/<doc>.json
                                                                                              │
graph.json  ◄── oto curate apply ◄── oto curate check ◄── oto curate add ◄── oto curate propose ─┘
    │
    └──► oto build ──► kg_* tools, questions.yaml, capture.json, data.js (projection) ──► the site, the readers
```

- The pack says what to ask (`sections`, `types`, `x-term`); the studio asks it.
- What the person confirms becomes a capture, then a proposal, then facts — with the document,
  the section and the quote as evidence — under the same gates as any document.
- A reader installs the published pack and asks `kg_ask`; a correction comes back through the
  gates as a pull request.

### Its tests

`tests/test_scenes.py` runs scenes 1 to 7 scripted on the report application (`OTO_HOME` or
`oto-kg` installed, and the `product` and `product-report` packs on the machine, plus `ddd` and
`flow`): the pack checked and a product started from it, a capture of the report product's
obligations, the gates, the questions the graph answers and the ones left open, the design and the
flow traced to the specification, and the implementing agent's brief (BLOCKED by name, the missing
fact captured, READY); the site from the graph, the domain pack on a marketplace and the product's
store published; a reader who installs the pack and one who syncs the store, both asking.
