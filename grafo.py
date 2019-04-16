from collections import deque, namedtuple


# we'll use infinity as a default distance to verticess.
inf = float('inf')
aresta = namedtuple('aresta', 'ini, fim, custo')


def make_aresta(ini, fim, custo=1):
  return aresta(ini, fim, custo)


class Graph:
    def __init__(grafo, arestas):
        # let's check that the data is right
        wrong_arestas = [i for i in arestas if len(i) not in [2, 3]]
        if wrong_arestas:
            raise ValueError('Wrong arestas data: {}'.format(wrong_arestas))

        grafo.arestas = [make_aresta(*aresta) for aresta in arestas]

    @property
    def vertices(grafo):
        return set(
            sum(
                ([aresta.ini, aresta.fim] for aresta in grafo.arestas), []
            )
        )

    def get_vertices_pairs(grafo, n1, n2, both_fins=True):
        if both_fins:
            vertices_pairs = [[n1, n2], [n2, n1]]
        else:
            vertices_pairs = [[n1, n2]]
        return vertices_pairs

    def remove_aresta(grafo, n1, n2, both_fins=True):
        vertices_pairs = grafo.get_vertices_pairs(n1, n2, both_fins)
        arestas = grafo.arestas[:]
        for aresta in arestas:
            if [aresta.ini, aresta.fim] in vertices_pairs:
                grafo.arestas.remove(aresta)

    def add_aresta(grafo, n1, n2, custo=1, both_fins=True):
        vertices_pairs = grafo.get_vertices_pairs(n1, n2, both_fins)
        for aresta in grafo.arestas:
            if [aresta.ini, aresta.fim] in vertices_pairs:
                return ValueError('aresta {} {} already exists'.format(n1, n2))

        grafo.arestas.append(aresta(ini=n1, fim=n2, custo=custo))
        if both_fins:
            grafo.arestas.append(aresta(ini=n2, fim=n1, custo=custo))

    @property
    def neighbours(grafo):
        neighbours = {vertex: set() for vertex in grafo.vertices}
        for aresta in grafo.arestas:
            neighbours[aresta.ini].add((aresta.fim, aresta.custo))

        return neighbours

    def dijkstra(grafo, origem, alvo):
        assert origem in grafo.vertices, 'Such origem vertices doesn\'t exist'
        distances = {vertex: inf for vertex in grafo.vertices}
        previous_vertices = {
            vertex: None for vertex in grafo.vertices
        }
        distances[origem] = 0
        vertices = grafo.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, custo in grafo.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + custo
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), alvo
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

    def guloso():
        return

graph = Graph([
    ("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 14), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
    ("e", "f", 9)])

op = 1

while op:
    op = input('\n(1) Procura por Dijkstra\n(2) Procura por Guloso\n\n(0) Sair\n\n-> ')
    print('\n')

    if op == 0:
        print('Saindo do Programa...\n')
    else:
        if op == 1:
            print( graph.dijkstra("c", "e"))
        else:
            if op == 2:
                print('guloso\n')
            else:
                op = 1
