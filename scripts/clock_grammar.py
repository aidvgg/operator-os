"""clock_grammar - the ONE owner of the repo's Due/Stale line grammar.

Why this file exists. The grammar used to be hand-copied into scripts/horizon, scripts/money and
scripts/repo-doctor. One edit taught ONE of the three that a strikethrough only kills the token
it wraps, not the whole line. The other two kept the whole-line test, so the repo's own
documented rollover shape

    ~~**Due:** 2026-07-31~~ **Due:** 2026-08-05 - NL-2026-002 payment due

made horizon print a live commitment while money called the same receivable unarmed, exited 1
and refused to write MONEY.md, after which repo-doctor's HARD money-stale demanded the file
money would not produce. Three copies, one edit, a deadlock. That is why the grammar has exactly
one owner now: do not re-copy these functions into a fourth consumer.

CONTRACT, and it is load-bearing: this module holds constants and PURE FUNCTIONS ONLY, with
zero module-level execution and no sys.exit under any circumstance. Consumers load it in-process
(repo-doctor loads it by path), and a module-level exit would terminate the importing checker at
the module's own status. repo-doctor exiting 0 half-loaded is read as CLEAN by both git hooks,
which would turn a broken grammar into a silent full-off switch for the secrets gate. Keep this
file free of side effects. Anything that can fail belongs in the caller.
"""
import re

# A Due token is either line-start, or a mid-line bold `**Due:**`. Mid-line bare prose is NOT a
# token: most mid-line mentions in knowledge/ and outputs/ are quotations of a Due line inside
# prose or backticks, and counting those turns the clock into an alarm swamp. Narrow on purpose:
# this rule adds nothing to the live scan while making the rollover shape visible, which a
# line-start anchor cannot see at all.
DUE_ANY_RE = re.compile(
    r"(?:^[\s>*-]{0,6}\**\s*due:?\**|\*\*\s*due:?\s*\*\*)\s*(\d{4}-\d{2}-\d{2})", re.I)
STALE_RE = re.compile(r"^\**\s*stale after:?\**\s*(\d{4}-\d{2}-\d{2})", re.I)
STRIKE_RE = re.compile(r"~~")
# Strips the separator between a date and its text. The em and en dash are \u escapes ON PURPOSE:
# a Due line pasted in from somewhere else may use one as that separator, so the class must know
# them, while this OS's global ban forbids a literal em dash in authored text. The escape form
# satisfies both, and this file contains zero literal em or en dashes.
DASH_LEAD_RE = re.compile(r"^[\s\u2014\u2013-]+")
# A fenced block opener/closer. Due tokens inside fences are TEMPLATES, not commitments.
FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")


def struck_spans(line):
    """Half-open [start, end) ranges that ~~strikethrough~~ covers on this line.

    Runs of `~~` pair in order. An UNPAIRED trailing `~~` strikes to end of line, because a
    malformed strike must not re-animate text the author meant to retire.
    """
    marks = [m.start() for m in STRIKE_RE.finditer(line)]
    spans = [(marks[i], marks[i + 1] + 2) for i in range(0, len(marks) - 1, 2)]
    if len(marks) % 2:
        spans.append((marks[-1], len(line)))
    return spans


def due_tokens(line):
    """[(date-string, description)] for every LIVE Due token on the line.

    A token is struck only when a strikethrough span actually wraps IT. Testing the line for a
    `~~` anywhere is what made the rollover shape invisible: one dead date hid a live one.
    """
    spans = struck_spans(line)
    hits = [(m.start(), m.end(), m.group(1)) for m in DUE_ANY_RE.finditer(line)]
    out = []
    for idx, (s, e, datestr) in enumerate(hits):
        if any(a <= s < b or a < e <= b for a, b in spans):
            continue                                   # the strike wraps this token
        if s > 0:
            head = "".join(c for i, c in enumerate(line[:s])
                           if not any(a <= i < b for a, b in spans))
            if head.strip(" \t>*-"):
                continue                               # prose or a backtick quote, not a token
        stop = len(line)
        if idx + 1 < len(hits):
            stop = min(stop, hits[idx + 1][0])          # the next Due token ends this one
        for a, b in spans:
            if a >= e:
                stop = min(stop, a)                     # a following strike ends it too
                break
        out.append((datestr, DASH_LEAD_RE.sub("", line[e:stop].strip()).strip()))
    return out


def fenced_flags(lines):
    """[bool] per line: True when the line sits INSIDE a ``` or ~~~ fenced block.

    Fences are where paste templates and spec examples live, and a Due token in a template is
    not a promise. This has bitten: phantom commitments copied out of a template block sat in
    the live aggregate, one of them a drill already completed, and they would have started
    reporting chronic on a date nobody had ever promised anything for.

    Returns (flags, odd_parity). odd_parity is True when the file has an unclosed fence, which
    the caller must REPORT rather than swallow: failing open there would silently drop every
    token after a stray backtick line.
    """
    flags, inside = [], False
    for ln in lines:
        if FENCE_RE.match(ln):
            flags.append(True)          # the fence line itself is never a commitment
            inside = not inside
            continue
        flags.append(inside)
    return flags, inside


def grammar_selfcheck():
    """[(label, ok)] for each invariant. Pure: returns results, never exits, never prints.

    In-band ratchet. This tests the GRAMMAR, not the consumer wiring; the wiring is covered by
    the guardrail-fixture suite in knowledge/ops/os-roadmap.md. A caller decides what a failure
    means: money refuses to write on a Due-family failure, repo-doctor emits a soft line and
    exits 0.
    """
    r = []
    roll = "~~**Due:** 2026-07-31~~ **Due:** 2026-08-05 - NL payment due"
    t = due_tokens(roll)
    r.append(("due:rollover-keeps-live-token", [d for d, _ in t] == ["2026-08-05"]))
    r.append(("due:rollover-drops-struck", "2026-07-31" not in [d for d, _ in t]))
    r.append(("due:linestart", [d for d, _ in due_tokens("**Due:** 2026-08-01 - x")] == ["2026-08-01"]))
    r.append(("due:prose-quote-ignored",
              due_tokens("see the `**Due:** 2026-08-01` convention") == []))
    r.append(("due:fully-struck-line", due_tokens("~~**Due:** 2026-08-01 - done~~") == []))
    r.append(("due:description-kept",
              due_tokens("**Due:** 2026-08-05 - NL payment")[0][1] == "NL payment"))
    f, odd = fenced_flags(["a", "```", "**Due:** 2026-08-08 - template", "```", "b"])
    r.append(("fence:inside-flagged", f == [False, True, True, True, False]))
    r.append(("fence:balanced-parity", odd is False))
    r.append(("fence:unclosed-reported", fenced_flags(["```", "x"])[1] is True))
    r.append(("stale:linestart", bool(STALE_RE.match("**Stale after:** 2026-09-01"))))
    return r
