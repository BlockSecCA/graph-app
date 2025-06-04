import pytest
from graph_analysis import analyze_graph


def test_simple_graph():
    nodes = [
        {'id': 'A', 'label': 'A'},
        {'id': 'B', 'label': 'B'},
        {'id': 'C', 'label': 'C'},
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'type': '+', 'weight': 1},
        {'source': 'B', 'target': 'C', 'type': '+', 'weight': 2},
    ]
    result = analyze_graph(nodes, edges)
    assert result['influence_scores'] == {'A': 0, 'B': 1, 'C': 2}
    assert result['positive_paths'] == [['A', 'B', 'C']]
    assert result['negative_paths'] == []
    assert result['error'] == ''


def test_all_negative_edges():
    nodes = [
        {'id': 'A', 'label': 'A'},
        {'id': 'B', 'label': 'B'},
        {'id': 'C', 'label': 'C'},
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'type': '-', 'weight': 1},
        {'source': 'B', 'target': 'C', 'type': '-', 'weight': 1},
    ]
    result = analyze_graph(nodes, edges)
    assert result['influence_scores'] == {'A': 0, 'B': -1, 'C': -1}
    assert result['positive_paths'] == []
    assert result['negative_paths'] == []
    assert result['error'] == ''


def test_disconnected_graph():
    nodes = [
        {'id': 'A', 'label': 'A'},
        {'id': 'B', 'label': 'B'},
        {'id': 'C', 'label': 'C'},
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'type': '+', 'weight': 1},
    ]
    result = analyze_graph(nodes, edges)
    assert result['influence_scores'] == {'A': 0, 'B': 1, 'C': 0}
    assert result['positive_paths'] == []
    assert result['negative_paths'] == []
    assert result['error'] == ''


def test_cyclic_graph():
    nodes = [
        {'id': 'A', 'label': 'A'},
        {'id': 'B', 'label': 'B'},
        {'id': 'C', 'label': 'C'},
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'type': '+', 'weight': 1},
        {'source': 'B', 'target': 'C', 'type': '+', 'weight': 1},
        {'source': 'C', 'target': 'A', 'type': '+', 'weight': 1},
    ]
    result = analyze_graph(nodes, edges)
    # Should handle cycle without infinite loops
    assert result['positive_paths'] == [['A', 'B', 'C']]
    assert result['negative_paths'] == []
    assert result['error'] == ''


def test_zero_weights():
    nodes = [
        {'id': 'A', 'label': 'A'},
        {'id': 'B', 'label': 'B'},
        {'id': 'C', 'label': 'C'},
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'type': '+', 'weight': 0},
        {'source': 'B', 'target': 'C', 'type': '+', 'weight': 0},
    ]
    result = analyze_graph(nodes, edges)
    assert result['influence_scores'] == {'A': 0, 'B': 0, 'C': 0}
    assert result['positive_paths'] == []
    assert result['negative_paths'] == []
    assert result['error'] == ''


def test_malformed_graph_returns_error():
    nodes = [{'id': 'A', 'label': 'A'}, {'id': 'B', 'label': 'B'}]
    # Edge references non-existent target 'C'
    edges = [{'source': 'A', 'target': 'C', 'type': '+', 'weight': 1}]
    result = analyze_graph(nodes, edges)
    assert result['influence_scores'] == {}
    assert result['positive_paths'] == []
    assert result['negative_paths'] == []
    assert result['error'] != ''
