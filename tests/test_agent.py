from types import SimpleNamespace
from unittest.mock import Mock

from ai_learning_feed.harness import agent
from ai_learning_feed.tools.web_search import WEB_SEARCH_TOOL


def test_run_passes_query_profile_and_web_search_tool(monkeypatch, learning_profile):
    response = SimpleNamespace(output_text="Search results")
    create_mock = Mock(return_value=response)
    monkeypatch.setattr(agent.client.responses, "create", create_mock)
    query = "Find Python learning resources"

    result = agent.LearningAgent(learning_profile).run(query)

    assert result == "Search results"
    create_mock.assert_called_once()
    arguments = create_mock.call_args.kwargs
    assert arguments["input"] == query
    assert arguments["model"] == "gpt-6-luna"
    assert arguments["tools"] == [WEB_SEARCH_TOOL]
    assert learning_profile.background in arguments["instructions"]
    assert "Python" in arguments["instructions"]
