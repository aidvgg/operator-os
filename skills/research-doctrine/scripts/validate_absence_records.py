#!/usr/bin/env python3
"""Validate deterministic research-doctrine verified-absence records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


REQUIRED_FIELDS = (
    "absence_id", "q_ids", "component_ids", "corpus_or_paths",
    "terms_and_synonyms", "search_date", "tool_or_method",
    "inspected_count", "retrieval_status", "scoped_result", "consequence",
)
METHOD_FIELDS = {"tool", "procedure", "parameters", "completion"}
TOOL_FIELDS = {"kind", "identity"}
PARAMETER_FIELDS = {"terms_and_synonyms", "corpus_or_paths", "options"}
COMPLETION_FIELDS = {"declared_count", "inspected_count", "blocked_count", "match_count"}
RESULT_FIELDS = {"outcome", "inspected_count", "corpus_or_paths"}
CONSEQUENCE_FIELDS = {"mode", "component_ids", "corpus_or_paths"}
PROCEDURES = {"SEARCH_THEN_INSPECT_ALL_MATCHES", "MANUAL_REVIEW_ALL_DECLARED_ITEMS"}
CONSEQUENCE_MODES = {"BOUNDED_ABSENCE", "UNKNOWN", "NO_DURABLE_CLAIM", "QUESTION_OPEN"}
TOOL_KINDS = {"EXECUTABLE", "MANUAL"}
OPTION_ENUMS = {"CASE_INSENSITIVE", "CASE_SENSITIVE", "FIXED_STRING", "REGEX", "RECURSIVE", "LINE_BY_LINE"}

VERSIONED_TOOL_PATTERN = re.compile(
    r"[A-Za-z][A-Za-z0-9_.-]* v?(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"
)
EXECUTABLE_PATH_OR_FILE_PATTERN = re.compile(
    r"(?:(?:[A-Za-z]:[\\/]|/|\./|\.\./)?(?:[A-Za-z0-9_.-]+[\\/])*[A-Za-z0-9_.-]+\.(?:py|sh|js|exe|bin))",
    re.IGNORECASE,
)
GLOB_PATTERN = re.compile(r"[*?\[\]{}]")
DOT_SEGMENT_PATTERN = re.compile(r"(?:^|[\\/])\.+(?:[\\/]|$)")
ROOT_ONLY_PATTERN = re.compile(r"^(?:[\\/]+|[A-Za-z]:[\\/]*)$")
INVALID_PERCENT_ESCAPE_PATTERN = re.compile(r"%(?![0-9A-Fa-f]{2})")
UNBOUNDED_BOUNDARY_PATTERN = re.compile(
    r"^(?:all|every|any|corpus|corpora|paths?|records?|documents?|files?|websites?|everything|everywhere|whole|entire|global|globally|universal|world|worldwide|world-wide|web|internet|internet-wide)$|(?:^|[\s/_-])(?:all|every|any)[\s_-]*(?:corpus|corpora|paths?|records?|documents?|files?|websites?)(?:$|[\s/_-])|^(?:the[\s_-]+)?(?:whole|entire)[\s_-]+(?:world|internet|corpus|corpora|paths?|records?|documents?|files?|websites?)$|^(?:internet|world)[\s_-]*wide$|^(?:company|org|organization|enterprise)[\s_-]*wide$",
    re.IGNORECASE,
)


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(item) for item in value)


def nonnegative_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def valid_executable_identity(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    identity = value.strip()
    return bool(VERSIONED_TOOL_PATTERN.fullmatch(identity) or EXECUTABLE_PATH_OR_FILE_PATTERN.fullmatch(identity))


def valid_file_uri(boundary: str) -> bool:
    try:
        parsed = urlsplit(boundary)
    except ValueError:
        return False
    if parsed.scheme.lower() != "file" or INVALID_PERCENT_ESCAPE_PATTERN.search(parsed.path):
        return False
    try:
        decoded_path = unquote(parsed.path, encoding="utf-8", errors="strict").replace("\\", "/")
        decoded_authority = unquote(parsed.netloc, encoding="utf-8", errors="strict")
    except UnicodeDecodeError:
        return False
    if INVALID_PERCENT_ESCAPE_PATTERN.search(parsed.netloc):
        return False
    if decoded_authority and ("/" in decoded_authority or "\\" in decoded_authority or re.fullmatch(r"\.+", decoded_authority)):
        return False
    segments = [segment for segment in decoded_path.split("/") if segment]
    if any(re.fullmatch(r"\.+", segment) for segment in segments):
        return False
    if len(segments) == 1 and re.fullmatch(r"[A-Za-z]:", segments[0]):
        return False
    if parsed.netloc:
        has_resource = bool(segments)
    elif decoded_path.startswith("//"):
        has_resource = len(segments) >= 2
    else:
        has_resource = bool(segments)
    resource_label = decoded_path.strip("/")
    return bool(
        has_resource
        and not GLOB_PATTERN.search(decoded_path)
        and not UNBOUNDED_BOUNDARY_PATTERN.search(resource_label)
    )


def valid_boundary(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    boundary = value.strip()
    if boundary.lower().startswith("file:"):
        return valid_file_uri(boundary)
    return not (
        GLOB_PATTERN.search(boundary)
        or DOT_SEGMENT_PATTERN.search(boundary)
        or ROOT_ONLY_PATTERN.fullmatch(boundary)
        or UNBOUNDED_BOUNDARY_PATTERN.search(boundary)
    )


def validate_record(record: Any, position: int) -> list[str]:
    prefix = f"record {position}"
    if not isinstance(record, dict):
        return [f"{prefix}: must be a JSON object"]
    errors = [f"{prefix}: missing required field '{field}'" for field in REQUIRED_FIELDS if field not in record]
    if errors:
        return errors
    unexpected = sorted(set(record) - set(REQUIRED_FIELDS))
    if unexpected:
        errors.append(f"{prefix}: unexpected top-level fields: {', '.join(unexpected)}")

    if not nonempty_string(record["absence_id"]) or not re.fullmatch(r"A[1-9][0-9]*", record["absence_id"]):
        errors.append(f"{prefix}: absence_id must be a stable ID such as A1")
    if not string_list(record["q_ids"]) or not all(re.fullmatch(r"Q[1-9][0-9]*", item) for item in record["q_ids"]):
        errors.append(f"{prefix}: q_ids must contain at least one Q ID")
    component_pattern = re.compile(r"R[1-9][0-9]*\.[A-Za-z][A-Za-z0-9_-]*")
    if not string_list(record["component_ids"]) or not all(component_pattern.fullmatch(item) for item in record["component_ids"]):
        errors.append(f"{prefix}: component_ids must contain at least one atomic component ID")
    if not string_list(record["corpus_or_paths"]):
        errors.append(f"{prefix}: corpus_or_paths must contain at least one inspected boundary")
    elif not all(valid_boundary(item) for item in record["corpus_or_paths"]):
        errors.append(f"{prefix}: corpus_or_paths must contain specific bounded names or paths without glob syntax")
    elif len(record["corpus_or_paths"]) != len(set(record["corpus_or_paths"])):
        errors.append(f"{prefix}: corpus_or_paths must contain unique boundaries")

    terms = record["terms_and_synonyms"]
    if not isinstance(terms, dict) or set(terms) != {"terms", "synonyms"}:
        errors.append(f"{prefix}: terms_and_synonyms must contain only terms and synonyms lists")
    else:
        if not string_list(terms["terms"]):
            errors.append(f"{prefix}: terms_and_synonyms.terms must contain at least one term")
        if not isinstance(terms["synonyms"], list) or not all(nonempty_string(item) for item in terms["synonyms"]):
            errors.append(f"{prefix}: terms_and_synonyms.synonyms must be a list of recorded synonyms, or an empty list")

    search_date = record["search_date"]
    valid_date = nonempty_string(search_date) and bool(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", search_date))
    if valid_date:
        try:
            date.fromisoformat(search_date)
        except ValueError:
            valid_date = False
    if not valid_date:
        errors.append(f"{prefix}: search_date must be a valid ISO calendar date in YYYY-MM-DD form")

    inspected_count = record["inspected_count"]
    if not nonnegative_integer(inspected_count) or inspected_count == 0:
        errors.append(f"{prefix}: inspected_count must be a positive integer")

    method = record["tool_or_method"]
    if not isinstance(method, dict) or set(method) != METHOD_FIELDS:
        errors.append(f"{prefix}: tool_or_method must contain only tool, procedure, parameters, and completion")
    else:
        tool = method["tool"]
        tool_kind: str | None = None
        if not isinstance(tool, dict) or set(tool) != TOOL_FIELDS:
            errors.append(f"{prefix}: tool_or_method.tool must contain only kind and identity")
        else:
            kind = tool["kind"]
            identity = tool["identity"]
            if not isinstance(kind, str) or kind not in TOOL_KINDS:
                errors.append(f"{prefix}: tool_or_method.tool.kind must be EXECUTABLE or MANUAL")
            else:
                tool_kind = kind
            if kind == "MANUAL" and identity != "manual review":
                errors.append(f"{prefix}: MANUAL tool identity must be manual review")
            if kind == "EXECUTABLE" and not valid_executable_identity(identity):
                errors.append(f"{prefix}: EXECUTABLE tool identity must use a closed executable form")

        procedure = method["procedure"]
        if not isinstance(procedure, str) or procedure not in PROCEDURES:
            errors.append(f"{prefix}: tool_or_method.procedure must use a controlled procedure enum")
        elif tool_kind == "MANUAL" and procedure != "MANUAL_REVIEW_ALL_DECLARED_ITEMS":
            errors.append(f"{prefix}: MANUAL tool requires MANUAL_REVIEW_ALL_DECLARED_ITEMS")
        elif tool_kind == "EXECUTABLE" and procedure != "SEARCH_THEN_INSPECT_ALL_MATCHES":
            errors.append(f"{prefix}: EXECUTABLE tool requires SEARCH_THEN_INSPECT_ALL_MATCHES")

        parameters = method["parameters"]
        if not isinstance(parameters, dict) or set(parameters) != PARAMETER_FIELDS:
            errors.append(f"{prefix}: tool_or_method.parameters must contain only terms_and_synonyms, corpus_or_paths, and options")
        else:
            if parameters["terms_and_synonyms"] != record["terms_and_synonyms"]:
                errors.append(f"{prefix}: tool_or_method.parameters.terms_and_synonyms must exactly equal terms_and_synonyms")
            if parameters["corpus_or_paths"] != record["corpus_or_paths"]:
                errors.append(f"{prefix}: tool_or_method.parameters.corpus_or_paths must exactly equal corpus_or_paths")
            options = parameters["options"]
            valid_options = (
                isinstance(options, list)
                and bool(options)
                and all(isinstance(option, str) and option in OPTION_ENUMS for option in options)
                and len(options) == len(set(options))
            )
            if not valid_options:
                errors.append(f"{prefix}: tool_or_method.parameters.options must be a unique nonempty controlled enum list")
            elif tool_kind == "MANUAL" and options != ["LINE_BY_LINE"]:
                errors.append(f"{prefix}: MANUAL tool options must be exactly LINE_BY_LINE")
            elif tool_kind == "EXECUTABLE":
                case_modes = {"CASE_INSENSITIVE", "CASE_SENSITIVE"}.intersection(options)
                match_modes = {"FIXED_STRING", "REGEX"}.intersection(options)
                if len(case_modes) != 1:
                    errors.append(f"{prefix}: EXECUTABLE tool options must contain exactly one case mode")
                if len(match_modes) != 1:
                    errors.append(f"{prefix}: EXECUTABLE tool options must contain exactly one match mode")
                if "LINE_BY_LINE" in options:
                    errors.append(f"{prefix}: EXECUTABLE tool options must not include LINE_BY_LINE")
        completion = method["completion"]
        if not isinstance(completion, dict) or set(completion) != COMPLETION_FIELDS:
            errors.append(f"{prefix}: tool_or_method.completion must contain only declared_count, inspected_count, blocked_count, and match_count")
        else:
            for field in sorted(COMPLETION_FIELDS):
                if not nonnegative_integer(completion[field]):
                    errors.append(f"{prefix}: tool_or_method.completion.{field} must be a nonnegative integer")
            if nonnegative_integer(completion["declared_count"]) and completion["declared_count"] != inspected_count:
                errors.append(f"{prefix}: tool_or_method.completion.declared_count must equal inspected_count")
            if nonnegative_integer(completion["inspected_count"]) and completion["inspected_count"] != inspected_count:
                errors.append(f"{prefix}: tool_or_method.completion.inspected_count must equal inspected_count")
            if nonnegative_integer(completion["blocked_count"]) and completion["blocked_count"] != 0:
                errors.append(f"{prefix}: tool_or_method.completion.blocked_count must equal 0")
            if nonnegative_integer(completion["match_count"]) and completion["match_count"] != 0:
                errors.append(f"{prefix}: tool_or_method.completion.match_count must equal 0")

    if record["retrieval_status"] != "COMPLETE":
        errors.append(f"{prefix}: retrieval_status must be COMPLETE")
    result = record["scoped_result"]
    if not isinstance(result, dict) or set(result) != RESULT_FIELDS:
        errors.append(f"{prefix}: scoped_result must contain only outcome, inspected_count, and corpus_or_paths")
    else:
        if result["outcome"] != "NOT_FOUND":
            errors.append(f"{prefix}: scoped_result.outcome must be NOT_FOUND")
        if not nonnegative_integer(result["inspected_count"]) or result["inspected_count"] == 0:
            errors.append(f"{prefix}: scoped_result.inspected_count must be a positive integer")
        elif result["inspected_count"] != inspected_count:
            errors.append(f"{prefix}: scoped_result.inspected_count must equal inspected_count")
        if result["corpus_or_paths"] != record["corpus_or_paths"]:
            errors.append(f"{prefix}: scoped_result.corpus_or_paths must exactly equal corpus_or_paths")

    consequence = record["consequence"]
    if not isinstance(consequence, dict) or set(consequence) != CONSEQUENCE_FIELDS:
        errors.append(f"{prefix}: consequence must contain only mode, component_ids, and corpus_or_paths")
    else:
        if not isinstance(consequence["mode"], str) or consequence["mode"] not in CONSEQUENCE_MODES:
            errors.append(f"{prefix}: consequence.mode must use a controlled consequence enum")
        if consequence["component_ids"] != record["component_ids"]:
            errors.append(f"{prefix}: consequence.component_ids must exactly equal component_ids")
        if consequence["corpus_or_paths"] != record["corpus_or_paths"]:
            errors.append(f"{prefix}: consequence.corpus_or_paths must exactly equal corpus_or_paths")
    return errors


def load_records(path: Path) -> list[Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else [payload]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record_file", type=Path)
    args = parser.parse_args()
    try:
        records = load_records(args.record_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"validate-absence-records: ERROR: {error}", file=sys.stderr)
        return 2
    if not records:
        print("validate-absence-records: INVALID: record array is empty", file=sys.stderr)
        return 1
    errors: list[str] = []
    seen_ids: set[str] = set()
    for position, record in enumerate(records, start=1):
        errors.extend(validate_record(record, position))
        if isinstance(record, dict) and nonempty_string(record.get("absence_id")):
            absence_id = record["absence_id"]
            if absence_id in seen_ids:
                errors.append(f"record {position}: duplicate absence_id '{absence_id}'")
            seen_ids.add(absence_id)
    if errors:
        for error in errors:
            print(f"validate-absence-records: INVALID: {error}", file=sys.stderr)
        return 1
    print(f"validate-absence-records: VALID: {len(records)} record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
