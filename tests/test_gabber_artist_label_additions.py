"""Reviewed artist/label additions must reach the existing bounded prompt route."""
import ast
from pathlib import Path
import re
import unittest
from unittest.mock import Mock
from core.mhjh_context import get_relevant_mhjh_context, unverified_person_reply

ROOT = Path(__file__).resolve().parents[1]

class ArtistLabelAdditionTests(unittest.TestCase):
    def test_reviewed_artist_aliases_leave_unknown_fallback_and_retrieve_profile(self):
        for name in ["DaBuddha", "dabuddha", "dabudda", "Da Buddha", "Daniel Gouweleeuw"]:
            with self.subTest(name=name):
                question = "ken je " + name + "?"
                context = get_relevant_mhjh_context(question)
                self.assertIsNone(unverified_person_reply(question))
                self.assertIn("Nederlandse dj en entertainer Daniel Gouweleeuw", context)
                self.assertNotIn("HARD NAAMVANGRAIL", context)
        tree = ast.parse((ROOT / "llm.py").read_text(encoding="utf-8"))
        wrapper = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "call_gabber_yello_llm")
        model = Mock(return_value=("normal", {}))
        ns = {"re": re, "call_yello_llm": model}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[wrapper], type_ignores=[])), "llm.py", "exec"), ns)
        self.assertEqual(ns["call_gabber_yello_llm"]("ken je dabudda?", kb_answer=get_relevant_mhjh_context("ken je dabudda?")), ("normal", {}))
        model.assert_called_once()

    def test_photo_succession_keeps_its_actual_source_with_artist_context(self):
        for question in ["Wat heeft DaBuddha met Mirko en Thunderdome te maken?", "Wie is dabudda?"]:
            with self.subTest(question=question):
                context = get_relevant_mhjh_context(question)
                self.assertIn("Volgens Dennis van MHJH", context)
                self.assertIn("overgenomen als officieel fotograaf van Thunderdome", context)
                self.assertIn("openbare dj-profielen zijn geen bron voor die opvolging", context)

    def test_bridgeway_label_and_sets_stay_distinct_in_selected_context(self):
        for question in ["Ken je Bridgeway Records?", "Wat is Bridgeway Records Waddinxveen?", "Is een Bridgeway liveset een labelrelease?"]:
            with self.subTest(question=question):
                context = get_relevant_mhjh_context(question)
                self.assertIn("platenlabel, opnamestudio en dj-platform in Waddinxveen", context)
                self.assertIn("iets anders dan een afzonderlijke trackrelease", context)
                self.assertNotIn("HARD NAAMVANGRAIL", context)

if __name__ == "__main__":
    unittest.main()
