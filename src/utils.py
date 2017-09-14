import networkx as nx


def loadGraphFromEdgeListTxt(file_name):
    f = open(file_name, 'r')
    G = nx.DiGraph()
    for line in f:
        edge = line.split(';')
        n1 = int(edge[0])
        n2 = int(edge[1].split('\n')[0])
        G.add_edge(n1, n2)
    return G


def to_cumulative(dist):
    cumulative = []
    c = 0
    for i in range(int(max(dist)) + 1):
        cumulative.append((len(dist) - c) / float(len(dist)))
        c += dist.count(i)

    return cumulative
