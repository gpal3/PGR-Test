from src.app.services.graph_similarity import graph_similarity_service


def test_graph_similarity_neighbors() -> None:
    nodes = list(graph_similarity_service.graph.nodes)
    assert nodes, "Graph should be initialized with demo data"
    supplier_nodes = [n for n in nodes if graph_similarity_service.graph.nodes[n].get("type") == "supplier"]
    if supplier_nodes:
        neighbors = graph_similarity_service.nearest_neighbors(supplier_nodes[0])
        assert isinstance(neighbors, list)
