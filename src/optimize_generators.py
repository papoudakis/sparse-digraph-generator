from generators import *
import numpy as np
from scipy.stats import ks_2samp
from utils import *
import copy
import os
# functions for computing the optimal parameters of SDG, GDGNC, Bollobas and ESDG


def optimize_sdg(graph):
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    epsilon1 = 0.3
    epsilon2 = 0.05
    in_degree_or = sorted(graph.in_degree().values())
    out_degree_or = sorted(graph.out_degree().values())
    best_MSD = np.inf
    best_graph = None
    best_epsilon1 = -1
    best_epsilon2 = -1
    while epsilon1 < 0.5:
        while epsilon2 < 1.0 * num_nodes / num_edges:
            gen_graph = sdg(num_nodes, num_edges, epsilon1, epsilon2)

            in_degree_gen = sorted(gen_graph.in_degree().values())
            out_degree_gen = sorted(gen_graph.out_degree().values())

            temp_MSD = max(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gen), 2.0)),
                           np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gen), 2.0)))
            if temp_MSD < best_MSD:
                best_graph = gen_graph
                best_MSD = temp_MSD
                best_epsilon1 = epsilon1
                best_epsilon2 = epsilon2

            epsilon2 += 0.05
        epsilon1 += 0.05
        epsilon2 = 0.05
    return best_graph, best_epsilon1, best_epsilon2


def optimize_bollobas(graph):
    num_edges = len(graph.edges())
    in_degree_or = sorted(graph.in_degree().values())
    out_degree_or = sorted(graph.out_degree().values())
    cdf_in_emp = to_cumulative(in_degree_or)
    cdf_out_emp = to_cumulative(out_degree_or)
    alpha = 0.1
    beta = 0.1
    best_Ks = np.inf
    best_graph = None
    best_alpha = -1
    best_beta = -1
    while alpha < 1.0:
        while alpha + beta < 1.0 - 1e-6:
            gen_graph = bollobas(num_edges, alpha, beta)
            in_degree_gen = sorted(gen_graph.in_degree().values())
            out_degree_gen = sorted(gen_graph.out_degree().values())
            cdf_in_gen = to_cumulative(in_degree_gen)
            cdf_out_gen = to_cumulative(out_degree_gen)

            temp_Ks = max(ks_2samp(cdf_in_gen, cdf_in_emp)[0], ks_2samp(cdf_out_gen, cdf_out_emp)[0])
            if temp_Ks < best_Ks:
                best_graph = gen_graph
                best_Ks = temp_Ks
                best_alpha = alpha
                best_beta = beta
            beta += 0.1
        alpha += 0.1
        beta = 0.1
    return best_graph, best_alpha, best_beta


def optimize_gdgnc(graph, gdgncPath):
    in_degree_or = sorted(graph.in_degree().values())
    out_degree_or = sorted(graph.out_degree().values())
    num_nodes = len(graph.nodes())
    # optimize the values for GDGNC
    counter = 0
    p = 0.0
    q = 0.0
    best_graph = None
    best_gdgnc_msd = np.inf
    best_p = -1
    best_q = -1
    while p <= 1:
        q = 0.0
        while q <= 1:
            os.system('python ' + gdgncPath + 'graphgen.py 1' + ' nodes=' + str(num_nodes) + ' p=' + str(p) + ' q=' +
                      str(q) + '> /tmp/temp' + str(counter) + '.csv')

            gdgnc_graph = loadGraphFromEdgeListTxt('/tmp/temp' + str(counter) + '.csv')
            in_degree_gen = sorted(gdgnc_graph.in_degree().values())
            out_degree_gen = sorted(gdgnc_graph.out_degree().values())

            temp_msd = max(np.mean(np.power(np.asarray(in_degree_gen) - np.asarray(in_degree_or), 2.0)),
                           np.mean(np.power(np.asarray(out_degree_gen) - np.asarray(out_degree_or), 2.0)))

            if temp_msd < best_gdgnc_msd:
                best_gdgnc_msd = temp_msd
                best_graph = gdgnc_graph
                best_p = p
                best_q = q
            # increase the counter
            counter += 1

            # increase the q value
            q += 0.1

        # increase the p value
        p += 0.1

    return best_graph, best_p, best_q


def optimize_esdg(cur_graph, new_graph, num_of_new_edges, new_nodes):
    threshold = 1e-6
    alpha = 0.1

    in_degree_or = sorted(new_graph.in_degree(new_nodes).values())
    out_degree_or = sorted(new_graph.out_degree(new_nodes).values())

    best_MSD = np.inf
    best_alpha = -1
    best_beta = -1
    best_epsilon1 = -1
    best_epsilon2 = -1
    best_graph = None
    while alpha < 0.7 + threshold:
        beta = 0.1
        while beta < 0.7 + threshold:
            epsilon1 = 0.3
            while epsilon1 < 0.55 + threshold:
                epsilon2 = 0.05
                while epsilon2 <= (1.0 * len(new_graph.nodes()) / len(new_graph.edges())):
                    if alpha + beta < 1.0 - threshold:

                        temp_graph = copy.deepcopy(cur_graph)

                        gen_graph = esdg(temp_graph, num_of_new_edges, new_nodes, epsilon1, epsilon2, alpha, beta)
                        in_degree_gen = sorted(gen_graph.in_degree(new_nodes).values())
                        out_degree_gen = sorted(gen_graph.out_degree(new_nodes).values())
                        temp_MSD = max(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gen), 2.0)),
                                       np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gen), 2.0)))
                        if len(gen_graph.edges()) != len(new_graph.edges()):
                            print 'Error'
                        if temp_MSD < best_MSD:
                            best_graph = gen_graph
                            best_MSD = temp_MSD
                            best_epsilon1 = epsilon1
                            best_epsilon2 = epsilon2
                            best_alpha = alpha
                            best_beta = beta

                    epsilon2 += 0.05
                epsilon1 += 0.05
            beta += 0.1
        alpha += 0.1
    return best_graph, best_alpha, best_beta, best_epsilon1, best_epsilon2
