import unittest
from contracts_loader import contracts
C = contracts()
class Contracts(unittest.TestCase):
    def payload(self, minutes=10, icon="scene-heart-support"):
        return {"title":"陪我待一会儿", "totalMinutes":minutes, "phases":[{"title":"慢慢停下来", "durationMinutes":minutes, "iconId":icon}]}
    def test_single_companionship_plan(self):
        plan=C["normalize_goal_plan"](self.payload(), split=False)
        self.assertEqual((len(plan.phases),plan.total_minutes,plan.phases[0].icon_id),(1,10,"scene-heart-support"))
    def test_split_requires_multiple_phases(self):
        with self.assertRaisesRegex(C["ModelSelectionError"],"multiple_phases"):
            C["normalize_goal_plan"](self.payload(),split=True)
    def test_duration_sum_and_icon_validation(self):
        p=self.payload(); p["totalMinutes"]=15
        with self.assertRaisesRegex(C["ModelSelectionError"],"total_mismatch"):
            C["normalize_goal_plan"](p,split=False)
        with self.assertRaisesRegex(C["ModelSelectionError"],"invalid_phase_icon"):
            C["normalize_goal_plan"](self.payload(icon="invented"),split=False)
    def test_goal_submit_contains_all_stage_material(self):
        s=C["submit_selection_tool_schema"](["unit-example"],goal_mode=True)["parameters"]
        self.assertTrue({"energyGoal","openingText","postReceiptText"}.issubset(s["required"]))
        self.assertEqual(set(s["properties"]["energyGoal"]["enum"]),{"boost","lower"})
    def test_internal_tool_and_real_top_k(self):
        tools=C["retrieval_tool_schemas"](False)
        self.assertEqual({t["name"] for t in tools},{"library_profile_search","music_description_recall"})
        for t in tools: self.assertEqual(t["parameters"]["properties"]["topK"]["maximum"],5)
        internal=C["retrieval_tool_schemas"](True)[0]
        self.assertNotIn("topK",internal["parameters"]["properties"])
    def test_plan_icon_enum(self):
        p=C["goal_plan_tool_schema"]()["parameters"]["properties"]["phases"]["items"]
        self.assertEqual(len(p["properties"]["iconId"]["enum"]),69)
        self.assertIn("iconId",p["required"])
if __name__=="__main__": unittest.main()
