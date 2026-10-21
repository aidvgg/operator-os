# Greenfield project branch

Initialize the smallest project that can prove one real user journey and support reliable future
agent work. Do not turn setup into a framework showcase.

## Intake

Ask at most three questions, folding known answers into the prompt:

1. What user and observable first journey make the project useful?
2. Which platform, deployment target, language, or interoperability constraint is fixed?
3. Which risk-bearing capabilities are in the first slice: identity, money, personal data, file
   handling, external integrations, privileged actions, or production access?

Recommend a boring, well-supported default where the user has no preference. A default must fit the
journey and deployment constraint; popularity alone is not a reason.

## Product contract

Create `docs/agentic/PROJECT.md` from `assets/harness/PROJECT.md.template` before application code.
Record the user, problem, first journey, non-goals, constraints, risks, deployment boundary, and
success evidence. Product ambiguity stays visible rather than being guessed inside implementation.

## Initializer

Create or adapt these capabilities:

1. A short `AGENTS.md` map from `assets/harness/AGENTS.md.template`.
2. `ARCHITECTURE.md` from `assets/harness/ARCHITECTURE.md.template`, naming dependency direction and
   public boundaries before the codebase grows around accidental patterns.
3. `docs/agentic/QUALITY.md` from `assets/harness/QUALITY.md.template`.
4. An active task contract from `assets/harness/TASK.md.template`.
5. Project-native format, lint, strict type, test, and build commands, composed behind one check
   command. Add only checks that can run and fail meaningfully.
6. One vertical tracer journey through the real runtime, with a user-level acceptance test.
7. A local development entrypoint and seed or fixture path that a fresh agent can run without
   reconstructing setup from chat history.

Create no empty subsystem directories, speculative abstractions, generalized workflow engine, or
unused infrastructure. The first architecture should make the first journey easy and later changes
inspectable.

## Bootstrap checkpoint

After the tracer journey is green, run the observer and create a baseline snapshot. The initializer
is complete only when a fresh context can locate the project rules, start the system, run the unified
gate, demonstrate the journey, and identify the next task from repository artifacts alone.
