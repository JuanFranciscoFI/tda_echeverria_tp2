from collections import deque

# ---------------------------------------------------------------------------
# Red de flujo (Edmonds-Karp)
# ---------------------------------------------------------------------------

def _bfs(cap, source, sink, parent):
    visited = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, c in enumerate(cap[u]):
            if v not in visited and c > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    return False


def _edmonds_karp(cap, source, sink, logger=None, label_fn=None):
    """
    label_fn: callable(node_id) -> str, usado solo cuando logger no es None.
    """
    n = len(cap)
    max_flow = 0
    iteration = 0
    while True:
        parent = [-1] * n
        if not _bfs(cap, source, sink, parent):
            if logger:
                logger.debug("No hay más caminos aumentantes — algoritmo termina.")
            break
        # capacidad del cuello de botella
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, cap[u][v])
            v = u
        if logger:
            path = []
            v = sink
            while v != source:
                path.append(v)
                v = parent[v]
            path.append(source)
            path.reverse()
            fmt = label_fn or str
            path_str = " -> ".join(fmt(x) for x in path)
            iteration += 1
            logger.debug(
                "Iter %d: %s  [cuello=%d, flujo acum=%d]",
                iteration, path_str, path_flow, max_flow + path_flow,
            )
        # actualizar red residual
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= path_flow
            cap[v][u] += path_flow
            v = u
        max_flow += path_flow
    return max_flow

