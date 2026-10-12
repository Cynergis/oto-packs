---
name: architecture-build
description: >
  Design the solution as a knowledge base: captures the architecture against the
  `software-architecture` and `ddd` packs through the elicit skill — context and drivers, ADRs,
  systems, components, interfaces, stores, environments, bounded contexts, aggregates, events —
  every component traced to the requirement it satisfies, every decision recorded with its
  alternatives. Use when the user wants to design or extend the architecture, record an ADR as
  the decision is made, or model the domain. Writing up an ADR or a design brief from decisions
  already in the graph is OTO's spec.
---

# Build the architecture

The design level of the knowledge base: how the solution is shaped to do what the specification
says. Captured against packs, cross-linked to the specification by relations, not conventions.

1. The project already holds `ddd`: this pack embeds it, and `ddd` sits on
   `software-architecture`, which sits on `product`, so one name brings the estate and the model
   (Atlas's scene 1 started the project from the pack). `oto ontology capture` writes the form.
2. Run the **elicit** skill with the schema of that project. Its askers are the architect, the
   on-call engineer, the data owner, the risk owner, the builder, compliance; its items are
   systems, components, interfaces, data stores, environments, teams, runbooks, repositories
   (the estate) and subdomains, bounded contexts and their map, use cases, events, commands,
   reactions, read models, external systems, aggregates, entities, value objects, business
   rules, domain services (the model) — and the links that make the design traceable: a
   component or a use case `satisfies` a requirement (SA17, DD24 say what is left), a context
   is `deployed_as` a component, a decision is `about` what it shaped, a risk `threatens` an
   asset. The people, the requirements, the policies, the scenarios, the terms, the decisions
   and the open questions are the product's: never captured twice.
3. Decision-first: an ADR is captured with its alternatives and consequences before the
   components it shapes; a component with no decision behind it is a finding (`kg_policy`).

What this skill no longer does: keep its own section list or write `window.__ARCH__`.
