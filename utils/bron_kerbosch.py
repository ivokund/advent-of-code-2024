def find_cliques(graph):
    def bron_kerbosch(r, p, x):
        if not p and not x:
            if len(r) > 1:
                cliques.append(r.copy())
            return

        if not p:  # Handle empty set case
            return

        pivot = next(iter(p))
        for v in list(p - graph[pivot]):
            r.add(v)
            new_p = p & graph[v]
            new_x = x & graph[v]
            bron_kerbosch(r, new_p, new_x)
            r.remove(v)
            p.remove(v)
            x.add(v)

    cliques = []
    nodes = set(graph.keys())
    bron_kerbosch(set(), nodes, set())
    return cliques
