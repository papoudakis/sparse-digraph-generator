import networkx as nx
import numpy as np
import random


def generator(num_nodes, num_edges, epsilon1, epsilon2):
    gen_graph = nx.DiGraph()
    nodes = range(num_nodes)
    gen_graph.add_nodes_from(nodes)
    i = 0
    while i < num_edges:
        # choose out node uniformly
        if random.random() < epsilon1 or len(gen_graph.edges()) < 1:
            out_node = random.choice(nodes)
        # choose out based on preferential attachment
        else:
            out_nodes = gen_graph.out_degree().keys()
            out_degree = np.array(gen_graph.out_degree().values())

            out_node = np.random.choice(out_nodes, p=out_degree/(1.0 * i))
        # choose in node uniformly
        if random.random() < epsilon2 or len(gen_graph.edges()) < 1:
            if 0 not in gen_graph.in_degree().values():
                in_node = random.choice(nodes)
        # choose in based on preferential attachment
            else:

                if len(nx.isolates(gen_graph)) > 0:
                    in_node = random.choice(nx.isolates(gen_graph))
                else:
                    in_node_degree = 1
                    while in_node_degree > 0:
                        in_node = random.choice(gen_graph.nodes())
                        in_node_degree = gen_graph.in_degree(in_node)
        else:
            in_nodes = gen_graph.in_degree().keys()
            in_degree = np.array(gen_graph.in_degree().values())
            in_node = np.random.choice(in_nodes, p=in_degree / (1.0 * i))

        if out_node != in_node and (out_node, in_node) not in gen_graph.edges():
            gen_graph.add_edge(out_node, in_node)
            i += 1

    return gen_graph


def bollobas(num_edges, alpha, beta, delta1=1.0, delta2=1.0):
    i = 0
    gen_graph = nx.DiGraph()
    nodes_counter = 1
    gen_graph.add_node(0)
    while i < num_edges:
        p = random.random()

        if p < alpha:
            # choose the in node
            in_degree = np.array(gen_graph.in_degree().values())
            in_nodes = gen_graph.in_degree().keys()
            in_node = np.random.choice(in_nodes, p=1.0*(in_degree + delta1) / (i + delta1*nodes_counter))
            out_node = nodes_counter
            gen_graph.add_node(nodes_counter)
            nodes_counter += 1
            i += 1
            gen_graph.add_edge(out_node, in_node)
        elif alpha < p < (beta + alpha):
            in_degree = np.array(gen_graph.in_degree().values())
            in_nodes = gen_graph.in_degree().keys()
            in_node = np.random.choice(in_nodes, p=1.0 * (in_degree + delta1) / (i + delta1*nodes_counter))

            out_degree = np.array(gen_graph.out_degree().values())
            out_nodes = gen_graph.out_degree().keys()
            out_node = np.random.choice(out_nodes, p=1.0 * (out_degree + delta2) / (i + delta2*nodes_counter))

            if (out_node, in_node) not in gen_graph.edges():
                i += 1
                gen_graph.add_edge(out_node, in_node)

        else:
            # choose the in node
            out_degree = np.array(gen_graph.out_degree().values())
            out_nodes = gen_graph.out_degree().keys()
            out_node = np.random.choice(out_nodes, p=1.0 * (out_degree + delta2) / (i + delta2*nodes_counter))
            in_node = nodes_counter
            gen_graph.add_node(nodes_counter)
            nodes_counter += 1
            i += 1
            gen_graph.add_edge(out_node, in_node)

    return gen_graph


