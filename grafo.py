from collections import deque, namedtuple


inf = float('inf')
aresta = namedtuple('aresta', 'ini, fim, custo') # aresta eh formada por uma dupla contendo o valor da aresta e uma tripla com as ligacoes da aresta e o seu valor

# metodo de construcao da aresta
def make_aresta(ini, fim, custo=1): # aresta eh iniciada com valor 1 representando o infinito
  return aresta(ini, fim, custo)

# classe do grafo
class Grafo:
    # metodo de verificacao se o grafo eh valido
    def __init__(grafo, arestas):
        noArestas = [i for i in arestas if len(i) not in [2, 3]]
        if noArestas:
            raise ValueError('Informacoes invalidas: {}'.format(noArestas))

        grafo.arestas = [make_aresta(*aresta) for aresta in arestas]

    # metodo construtor dos vertices
    @property
    def vertices(grafo):
        return set(sum(([aresta.ini, aresta.fim] for aresta in grafo.arestas), []))

    # metodo 'get' dos pares de vertices
    def get_pares(grafo, n1, n2, fins=True):
        if fins:
            parVertices = [[n1, n2], [n2, n1]]
        else:
            parVertices = [[n1, n2]]
        return parVertices

    def remove_aresta(grafo, n1, n2, fins=True):
        parVertices = grafo.get_pares(n1, n2, fins)
        arestas = grafo.arestas[:]
        for aresta in arestas:
            if [aresta.ini, aresta.fim] in parVertices:
                grafo.arestas.remove(aresta)

    def add_aresta(grafo, n1, n2, custo=1, fins=True):
        parVertices = grafo.get_pares(n1, n2, fins)
        for aresta in grafo.arestas:
            if [aresta.ini, aresta.fim] in parVertices:
                return ValueError('Aresta {} {} ja existe'.format(n1, n2))

        grafo.arestas.append(aresta(ini=n1, fim=n2, custo=custo))
        if fins:
            grafo.arestas.append(aresta(ini=n2, fim=n1, custo=custo))

    @property
    def vizinhos(grafo):
        vizinhos = {vert: set() for vert in grafo.vertices}
        for aresta in grafo.arestas:
            vizinhos[aresta.ini].add((aresta.fim, aresta.custo))

        return vizinhos

    def dijkstra(grafo, origem, alvo):
        custoTotal = 0
        dist = {vert: inf for vert in grafo.vertices}
        preVertices = {vert: None for vert in grafo.vertices}
        dist[origem] = 0
        vertices = grafo.vertices.copy()

        while vertices:
            atualVertice = min(vertices, key=lambda vert: dist[vert])
            vertices.remove(atualVertice)

            if dist[atualVertice] == inf:
                break

            for vizinho, custo in grafo.vizinhos[atualVertice]:
                alt = dist[atualVertice] + custo
                if alt < dist[vizinho]:
                    dist[vizinho] = alt
                    preVertices[vizinho] = atualVertice

        caminho, atualVertice = deque(), alvo
        while preVertices[atualVertice] is not None:
            caminho.appendleft(atualVertice)
            atualVertice = preVertices[atualVertice]
            custoTotal = custoTotal + custo
        if caminho:
            caminho.appendleft(atualVertice)

        caminho.appendleft(custoTotal)
        return caminho

    def guloso(grafo, origem, alvo, tipoBusca):
        custoTotal = 0
        dist = {vert: inf for vert in grafo.vertices}
        preVertices = {vert: None for vert in grafo.vertices}
        dist[origem] = 0
        vertices = grafo.vertices.copy()

        while vertices:
            atualVertice = min(vertices, key=lambda vert: dist[vert])
            vertices.remove(atualVertice)

            if dist[atualVertice] == inf:
                break

            for vizinho, custo in grafo.vizinhos[atualVertice]:
                alt = dist[atualVertice] + custo
                if alt < dist[vizinho]:
                    dist[vizinho] = alt
                    preVertices[vizinho] = atualVertice

        caminho, atualVertice = deque(), alvo
        while preVertices[atualVertice] is not None:
            caminho.appendleft(atualVertice)
            atualVertice = preVertices[atualVertice]
            custoTotal = custoTotal + custo
        if caminho:
            caminho.appendleft(atualVertice)

        caminho.appendleft(custoTotal)
        return caminho
g = Grafo([
    ("a", "b", 7),  ("a", "c", 9),  ("a", "f", 14), ("b", "c", 10),
    ("b", "d", 14), ("c", "d", 11), ("c", "f", 2),  ("d", "e", 6),
    ("e", "f", 9)])

op = 1 # variavel de opcoes iniciada para while valido

# menu do programa
while op:
    op = input('\n(1) Procura por Dijkstra\n(2) Procura por Guloso\n\n(0) Sair\n\n-> ')
    print('\n')

    # switch menu
    if op == 0:
        print('Saindo do Programa...\n')
    else:
        if op == 1:
            ori = raw_input('Vertice origem: ')
            des = raw_input('Vertice destino: ')
            print( g.dijkstra(ori, des))
        else:
            if op == 2:
                ori = raw_input('Vertice origem: ')
                des = raw_input('Vertice destino: ')
                tBusca = input('Busca por:\n          (1) Maior valor\n          (2) Menor valor\n-> ')
                print( g.guloso(ori, des, tBusca))
            else:
                op = 3
