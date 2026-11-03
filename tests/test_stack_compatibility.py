"""Trusted toy operations prove installed interfaces, not mission/runtime acceptance."""

import importlib
from typing import TypedDict

import pytest
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, ValidationError


class Counter(TypedDict):
    value: int


def test_langgraph_sqlite_interfaces_on_selected_python():
    def increment(state: Counter) -> Counter:
        return {"value": state["value"] + 1}

    graph = StateGraph(Counter)
    graph.add_node("increment", increment)
    graph.add_edge(START, "increment")
    graph.add_edge("increment", END)
    with SqliteSaver.from_conn_string(":memory:") as saver:
        runner = graph.compile(checkpointer=saver)
        config = {"configurable": {"thread_id": "synthetic-compatibility"}}
        assert runner.invoke({"value": 0}, config)["value"] == 1
        assert runner.get_state(config).values == {"value": 1}


def test_pydantic_v2_strict_boundary_interface():
    class Input(BaseModel):
        model_config = ConfigDict(strict=True, extra="forbid")
        count: int

    assert Input.model_validate({"count": 1}).count == 1
    with pytest.raises(ValidationError):
        Input.model_validate({"count": "1", "unknown": True})


@pytest.mark.parametrize("module", ["openai", "fastapi", "uvicorn", "playwright.sync_api", "httpx"])
def test_selected_optional_packages_import_without_live_calls(module):
    importlib.import_module(module)
