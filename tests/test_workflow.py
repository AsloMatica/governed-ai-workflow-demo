import copy
import json
import unittest
from pathlib import Path
from demo.workflow import evaluate

EXAMPLE = json.loads((Path(__file__).resolve().parents[1] / "examples" / "scenario.json").read_text(encoding="utf-8"))


class WorkflowTests(unittest.TestCase):
    def test_unsupported_claim_blocks(self):
        result = evaluate(EXAMPLE)
        self.assertEqual(result["gate"], "BLOCKED")
        self.assertFalse(result["action_executed"])
        self.assertEqual(len(result["blockers"]), 1)

    def test_valid_references_without_approval_wait(self):
        p = copy.deepcopy(EXAMPLE)
        p["claims"] = p["claims"][:1]
        self.assertEqual(evaluate(p)["gate"], "AWAITING_HUMAN_APPROVAL")

    def test_approval_does_not_execute(self):
        p = copy.deepcopy(EXAMPLE)
        p["claims"] = p["claims"][:1]
        p["human_approved"] = True
        result = evaluate(p)
        self.assertEqual(result["gate"], "RECOMMEND_FOR_HUMAN_REVIEW")
        self.assertFalse(result["action_executed"])

    def test_unknown_source_blocks(self):
        p = copy.deepcopy(EXAMPLE)
        p["claims"][0]["source_ids"] = ["UNKNOWN"]
        self.assertEqual(evaluate(p)["gate"], "BLOCKED")

    def test_boolean_is_required(self):
        p = copy.deepcopy(EXAMPLE)
        p["human_approved"] = "yes"
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_duplicate_source_ids_rejected(self):
        p = copy.deepcopy(EXAMPLE)
        p["sources"].append(copy.deepcopy(p["sources"][0]))
        with self.assertRaises(ValueError):
            evaluate(p)


if __name__ == "__main__":
    unittest.main()
