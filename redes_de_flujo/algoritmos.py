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


def _edmonds_karp(cap, source, sink):
    n = len(cap)
    max_flow = 0
    while True:
        parent = [-1] * n
        if not _bfs(cap, source, sink, parent):
            break
        # capacidad del camino aumentante
        path_flow = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, cap[u][v])
            v = u
        # actualizar red residual
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= path_flow
            cap[v][u] += path_flow
            v = u
        max_flow += path_flow
    return max_flow

