# Operator OS, the guide

This is the short, plain-words guide. If you have never used a terminal on purpose, start here.
The long version, with the why and the internals, is [`SETUP.md`](SETUP.md).

## 1. What this is, in one minute

Operator OS is a folder of plain text files that holds your whole business: who your clients
are, what you charge, what you decided and why, every invoice, a daily log, your brand voice.
An AI agent (Claude Code, or a similar AI coding agent) sits on top of that folder. You talk to
it in normal sentences. It reads the files, writes new ones, makes proposals and invoices as PDFs,
keeps your daily log, and saves a snapshot of everything so you can always go back.

You do not type commands. The agent does the typing. You answer questions and say what you want.

What it is not: it is not an app you log into, it does not send anything to clients on its own,
and it does not store your bank details anywhere it could share them.

The folder ships with a made-up demo business ("Sam Rivera / Northwind Labs") so you can see
every part working before it becomes yours. Setup takes about 30 to 45 minutes, most of it
answering questions. After that, a normal day is a few sentences.

## 2. What you need

- A Mac or a Linux computer. On Windows, install WSL first (Windows Subsystem for Linux, a free
  Microsoft feature that gives you a Linux terminal inside Windows) and do everything below inside
  it. Windows without WSL is untested.
- Claude Code, the AI coding agent this was built for. Get it from
  https://claude.com/claude-code and follow the install steps there. It needs a Claude
  subscription or an API budget; that is the one running cost.
- Google Chrome, because proposals and invoices are printed to PDF through it. You probably have it.
- A free GitHub account, optional. It is only for keeping a private online copy of your folder
  (your backup) and for asking questions. You can add it later.
- About 30 to 45 minutes.

## 3. Get the files

The fastest way is two lines in the terminal. The terminal is the text window where you type
commands; on a Mac it is the app called Terminal (open it from Spotlight: press Command-Space and
type Terminal).

Paste this line and press Enter. It downloads the Operator OS folder into your home folder:

```
git clone https://github.com/aidvgg/operator-os
```

You will see a few lines starting with `Cloning into 'operator-os'...` and then the prompt again.
If a window pops up offering to install "command line developer tools", click Install, wait for it
to finish, and paste the line again.

Now paste this line and press Enter. It moves you into that folder:

```
cd operator-os
```

You will see nothing special, just a new prompt line. That is correct.

The alternative: if Claude Code is already installed, start it in the terminal (type `claude`) and
say "Download https://github.com/aidvgg/operator-os into my home folder." It runs the first line
for you. Then type `/exit`, paste the `cd operator-os` line yourself, and go to section 4.

## 4. Open it with your agent and say one sentence

In the same terminal window, still inside the folder, type `claude` and press Enter. Claude Code
starts and shows its prompt. (Opening a folder in Claude Code means starting it from inside that
folder; that is all.)

Now say exactly this:

```
Set up Operator OS for me.
```

That sentence runs the agent's setup recipe, `skills/onboard/SKILL.md`. You do not need to read
it. Here is what the agent will do, in plain words:

1. Switch on the safety checks and create the one file that holds your payment details (empty for
   now). You will see it run `scripts/repo-doctor`, a checker, and report back.
2. Ask you plain questions, one at a time: your name, your business name, what you sell, who you
   sell to, how you charge, which channels you use (for example LinkedIn, email), and how you like
   to sound. Answer in a sentence each. "Skip" is an allowed answer.
3. Replace the demo business with yours, everywhere the demo name appears, and wipe the demo
   clients, invoices and logs.
4. Run the checkers again, make the first saved snapshot (a commit, a saved version you can always
   go back to), and end with a short summary of what it changed and what to do next.

The one thing you do by hand: your bank or wire details. The agent will not ask for them in the
chat, and you should never type them there. Chat text can end up in logs. Instead the agent will
tell you to open one file in a text editor and fill it in yourself:

```
knowledge/business/invoices/PAYMENT-DETAILS.md
```

Say "open the payment details file in TextEdit for me" and it opens. Replace every placeholder in
angle brackets with your real values, save, close. This file is deliberately excluded from the
saved history and from any online copy, and the checker refuses to ever save it. Invoices read it;
nothing else touches it.

What "done" looks like: the agent runs the checker one last time and you see this line, with
nothing else above it:

```
repo-doctor: clean
```

Before setup, the same checker prints two warnings instead. They are expected and they go away:

```
soft  payment-details-missing: knowledge/business/invoices/PAYMENT-DETAILS.md not on disk, invoicing is broken. Copy PAYMENT-DETAILS.template.md next to it and fill in the real values, which stay local-only
soft  hooks-unwired: run `git config core.hooksPath .githooks` (one-time per clone)
repo-doctor: 2 soft warning(s), no hard violations
```

You will also see one line from the deadline clock each time the agent starts, like
`horizon: 0 overdue, 0 in next 14d, 1 DECISIONS event gate(s); no verified backup recorded yet`.
Zero overdue is good. The backup part is covered in section 7.

## 5. Make it yours

The setup questions, and why each one matters:

- **Your name and business name.** They go on every proposal and invoice, and into the agent's
  standing instructions so it knows who it works for.
- **What you sell and who you sell to.** This is how the agent writes proposals in your words and
  judges whether a prospect fits you.
- **How you charge** (hourly, per project, retainer, packages) and your usual price range. The
  agent will flag when something looks underpriced, and it will never quote a price it cannot
  find in your files.
- **Which channels you use.** Email, LinkedIn, X, calls. Only those get voice rules.
- **How you like to sound.** Formal or casual, short or detailed, any words you never use.

The demo business disappears completely: its clients, invoices, logs, research and decisions are
deleted, and its name is replaced in every file that carried it. What stays is the machinery.

Nothing is final. Afterwards you can say "change my price range to X", "add a client called Y", or
"we also use Instagram now" at any time, and the agent updates the right file and saves a snapshot.

## 6. Your first week

One sentence a day. Each one runs one of the agent's recipes (the folder calls them skills).

- **Day 1: "plan my day."** The agent asks what you intend to do today, writes it to a page for
  that date under `knowledge/ops/logbook/days/`, and reads back anything overdue. Recipe:
  daily-log.
- **Day 2: "log my day."** The agent asks what got done, closes the day, and updates your
  streak and completion numbers in `knowledge/ops/logbook/STATS.md`. Same recipe. Do this every
  evening; plan every morning.
- **Day 3: "write a proposal for <client>."** The agent asks what the work is and what it costs,
  checks the price, and produces a branded PDF in `outputs/proposals/`. It also checks its own
  facts before it shows you the draft. Recipe: proposal-creator. You read the PDF and you send it;
  the agent never sends anything.
- **Day 4: "invoice <client> for <work>."** The agent takes the next invoice number from your
  ledger, copies the payment details from the file you filled in, and produces a branded PDF in
  `outputs/invoices/`. That folder stays on your computer only, so keep a copy where you keep
  invoices. Recipe: invoice-creator.
- **Day 5: "weekly review."** The agent rolls the week up into one page under
  `knowledge/ops/logbook/reviews/`: planned versus done, money collected and outstanding, what
  slipped. Recipe: daily-log again.

One more, any day you said something worth sharing: "harvest this session." The agent pulls one to
three short post ideas, each backed by a real fact from the session, into `outputs/content/seeds/`.
Recipe: harvest. It never posts.

Where things land, in short: `knowledge/` is what is true about your business (the agent keeps it
current). `outputs/` is what you produced (proposals, invoices, drafts). Every session ends with
the agent saving a snapshot, so you never lose a version.

## 7. Keep it safe

The folder has guardrails. They are small checkers that run on their own; you will mostly notice
them when they stop something. In plain words, they do two things:

- They stop secrets from being saved into the shared history. Anything shaped like a bank number,
  a routing number, a password or an API key gets caught before a snapshot is saved or sent to
  GitHub, and the payment details file can never be saved at all.
- They stop the agent from deleting history. Commands that would throw away saved versions or skip
  the checks are refused, and you will see a one-line explanation when that happens.

Backups. Your saved snapshots live on your computer. Two things to turn on, in this order:

1. A private GitHub copy. Create a free account and an empty private repository called
   `operator-os` on github.com, then say to the agent "connect this folder to my private GitHub
   repository and push." From then on every snapshot is also online.
2. The encrypted backup of the local-only files (payment details, invoices). It uses a tool called
   rclone and a cloud drive you already have. Say "set up the encrypted backup" when you are
   ready; the agent walks you through it, and the clock line stops saying
   `no verified backup recorded yet`. This one is optional.

Four things not to do:

1. Never type bank, card or wire numbers, passwords or API keys into the chat. Always into the
   named file, in a text editor.
2. If the agent ever suggests a command containing `--no-verify` or `--force`, say no. Those skip
   the guardrails.
3. Do not hand-edit the files under `.agents/`, `.claude/skills/`, or `AGENTS.md` and `GEMINI.md`.
   They are generated copies; ask the agent instead.
4. Do not delete the hidden `.git` folder inside `operator-os`. It is the history.

## 8. If something looks wrong

The five messages you are most likely to see, and what to say.

- `soft  payment-details-missing: ...` together with `soft  hooks-unwired: ...` means setup did
  not finish. Say: "finish the Operator OS setup."
- `repo-doctor: 1 HARD violation(s), commit blocked ...`, with a line above it such as
  `HARD  secrets: <file> matches a secret shape near offset ...`, means a file holds something
  that looks like a key or a bank number and the snapshot was refused. That is the guardrail
  working. Say: "take that value out of the file and keep it local only."
- `soft  dead-pointer: <file> cites ... which does not exist on disk` means a file still mentions
  a demo file that was deleted. Harmless until fixed. Say: "clear the dead pointers."
- `money: FAIL - collected mismatch: computed $0 but register states $10,000, refusing to write
  wrong numbers` means two money files disagree and the agent stopped rather than guess. Say: "reconcile
  the invoice summary and rerun money."
- `FAIL: no Chrome binary found ... HTML was written; PDF was not.` means Google Chrome is not
  installed, so no PDF. Install Chrome and say: "make the PDF again."

A PDF is good when the checker prints `PASS <file>`. If it prints `FAIL <file> [header]: no
%PDF-1.x header (a text file with a .pdf name?)`, the file is not a real PDF; say "regenerate it."

Anything else: copy the message into the chat and ask "what does this mean and what should we do?"
The agent has the long version and the scripts in front of it.

## 9. Words you will see

- **repo**: the folder with all your business files, plus its saved history. This folder.
- **terminal**: the text window where you type commands; on a Mac, the app called Terminal.
- **commit**: a saved snapshot of the folder that you can always go back to.
- **push**: sending your snapshots to your private online copy on GitHub.
- **agent**: the AI (Claude Code) that reads and writes the files for you.
- **skill**: a recipe the agent follows for one job, like writing an invoice. Lives in `skills/`.
- **guardrail**: a small checker that stops a bad save, like a secret in a shared file.
- **knowledge folder**: `knowledge/`, the files that hold what is true about your business.
- **outputs folder**: `outputs/`, the files you produced: proposals, invoices, drafts.
- **demo**: the made-up Northwind Labs business that ships in the folder and disappears at setup.

## 10. Where to go next

- [`SETUP.md`](SETUP.md) is the long version: every step the agent takes, what each checker
  does, and how to change things by hand if you ever want to.
- [`CHANGELOG.md`](CHANGELOG.md) lists what changed in each release.
- To ask a question: go to https://github.com/aidvgg/operator-os, click "Issues", then "New
  issue", and pick "Question". Say which file or section and what you were trying to do.
