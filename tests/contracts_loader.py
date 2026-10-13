from pathlib import Path
import ast
from dataclasses import dataclass
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
def contracts():
    tree = ast.parse((ROOT / "app/agent.py").read_text())
    wanted = {"ModelSelectionError", "GoalPlan", "GoalPlanPhase", "goal_plan_tool_schema", "normalize_goal_plan", "normalize_goal_phase_icon_id", "retrieval_tool_schemas", "submit_selection_tool_schema", "energy_goal_tool_schema"}
    constants = {"GOAL_PHASE_ICON_IDS", "DEFAULT_GOAL_PHASE_ICON_ID"}
    nodes = [n for n in tree.body if (isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name in wanted) or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in n.targets))]
    ns = {"dataclass": dataclass, "Any": Any, "ENERGY_GOALS": frozenset({"boost", "lower"})}
    future = ast.parse("from __future__ import annotations").body
    exec(compile(ast.Module(body=future + nodes, type_ignores=[]), "snapshot-contracts", "exec"), ns)
    return ns
