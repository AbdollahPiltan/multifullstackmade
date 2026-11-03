"""These foundation tests must never call a live model or tracing service."""

import socket

import pytest


@pytest.fixture(autouse=True)
def no_live_services(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "false")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "false")

    def denied(*args, **kwargs):
        raise AssertionError("Network access is forbidden in foundation tests.")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
