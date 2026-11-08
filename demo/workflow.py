"""Deterministic, human-supervised decision workflow for synthetic records.

No AI model, external data source, or autonomous action is used.
"""
import argparse
import json
from pathlib import Path

ALLOWED_KINDS = {"official_document", "internal_note", "unverified_claim"}


def evaluate(payload: dict) -> dict:
    """Evaluate a proposed action; never execute it."""
    required = {"question", "candidate_action", "claims", "sources", "human_approved"}
    if not isinstance(payload, dict) or required - payload.keys():
        raise ValueError("Input must contain question, candidate_action, claims, sources, human_approved")
    if not isinstance(payload["question"], str) or not payload["question"].strip():
        raise ValueError("question must be a non-empty string")
    if not isinstance(payload["candidate_action"], str) or not payload["candidate_action"].strip():
        raise ValueError("candidate_action must be a non-empty string")
    if not isinstance(payload["claims"], list) or not payload["claims"]:
        raise ValueError("claims must be a non-empty list")
    if not isinstance(payload["sources"], list):
        raise ValueError("sources must be a list")
    if type(payload["human_approved"]) is not bool:
        raise ValueError("human_approved must be true or false")

    source_ids = set()
    verified = set()
    for s in payload["sources"]:
        if not isinstance(s, dict) or not all(k in s for k in ("id", "kind", "description")):
            raise ValueError("each source needs id, kind, description")
        if not all(isinstance(s[k], str) and s[k].strip() for k in ("id", "kind", "description")):
            raise ValueError("source fields must be non-empty strings")
        if s["id"] in source_ids:
            raise ValueError("duplicate source id")
        source_ids.add(s["id"])
        if s["kind"] not in ALLOWED_KINDS:
            raise ValueError("unsupported source kind")
        if s["kind"] == "official_document":
            verified.add(s["id"])

    results = []
    for claim in payload["claims"]:
        if not isinstance(claim, dict) or not isinstance(claim.get("text"), str) or not claim["text"].strip() or not isinstance(claim.get("source_ids"), list):
            raise ValueError("each claim needs text and source_ids")
        ids = claim["source_ids"]
        if not all(isinstance(x, str) for x in ids):
            raise ValueError("claim source_ids must contain strings")
        unknown = sorted(set(ids) - source_ids)
        if unknown:
            status = "BLOCKED_UNKNOWN_SOURCE"
        elif set(ids) & verified:
            status = "SOURCE_REFERENCED_REVIEW_REQUIRED"
        else:
            status = "BLOCKED_NO_OFFICIAL_SOURCE"
        results.append({"claim": claim["text"], "status": status, "source_ids": ids})

    blockers = [r["claim"] for r in results if r["status"].startswith("BLOCKED")]
    if blockers:
        gate = "BLOCKED"
    elif not payload["human_approved"]:
        gate = "AWAITING_HUMAN_APPROVAL"
    else:
        gate = "RECOMMEND_FOR_HUMAN_REVIEW"

    return {
        "scenario": "synthetic_demo",
        "question": payload["question"],
        "candidate_action": payload["candidate_action"],
        "claim_reviews": results,
        "gate": gate,
        "blockers": blockers,
        "human_approved": payload["human_approved"],
        "action_executed": False,
        "handoff": "Human must independently verify referenced documents and authorise any downstream action.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic decision-gate demo")
    parser.add_argument("input", type=Path, help="Path to JSON input")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(evaluate(payload), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
