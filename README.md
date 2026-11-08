# Governed AI Workflow Demo

**AsloMatica · Synthetic demonstration · Python standard library only**

A small, runnable **deterministic** example showing how a proposed business action can pass through source-reference checks, a human-approval gate, and a structured handoff. The example uses entirely **fictional** information. It does **not** call an AI model or execute an action.

## Why this exists

Generating a recommendation is not enough. An operator needs to distinguish claims with references from unsupported claims, and distinguish recommendation from authorisation. This demo makes those distinctions visible in output.

## Run locally

Requires Python 3.10+ and no third-party dependencies.

```bash
python -m demo.workflow examples/scenario.json
python -m unittest discover -s tests -v
```

The sample intentionally includes an unsupported claim. Expected gate: `BLOCKED`. Remove that claim to receive `AWAITING_HUMAN_APPROVAL`. After setting `human_approved` to `true` for the supported-claim scenario, the gate becomes `RECOMMEND_FOR_HUMAN_REVIEW`; **no external action is executed** in any state.

## The six stages

1. **Input:** Receive a question, proposed action, source register, claims and approval flag.
2. **Evidence references:** Check source IDs and their declared types.
3. **Claim gate:** Flag claims without a referenced `official_document` record.
4. **Decision:** Block, await human approval, or recommend another review.
5. **Validation:** Reject malformed inputs and test key gate conditions.
6. **Handoff:** Return structured JSON with blockers, gate state and limits.

## Repository structure

| File | Purpose |
|---|---|
| `demo/workflow.py` | Runnable Python evaluator and command-line interface |
| `demo/__init__.py` | Python package marker |
| `examples/scenario.json` | Synthetic scenario with one deliberately unsupported claim |
| `tests/test_workflow.py` | Six unit tests |
| `LIMITATIONS.md` | Evidential and security boundaries |

## Proof and limitations

**Demonstrated:** deterministic source-reference classification, explicit decision states, no external actions and executable tests.

**Not demonstrated:** real-world source authenticity or factual verification, AI-model reasoning, autonomous agents, actual authenticated approval, enterprise deployment, business impact, regulatory compliance, or independent operator reproducibility.

In particular, `official_document` is **metadata supplied in the input**, not proof that a document is genuine or accurate. The `human_approved` flag is also supplied by the caller; it is **not an identity or authorisation system**. These gates are for education and illustration, not security enforcement.

The repository contains no proprietary AAPS control documents, private client records or credentials. See [LIMITATIONS.md](LIMITATIONS.md).

## Authorship

A new standalone illustrative implementation maintained under **AsloMatica** by **Asif Aslam**. This is not a direct release of AsloMatica's private operating systems, and no customer deployment or revenue outcomes are claimed.
