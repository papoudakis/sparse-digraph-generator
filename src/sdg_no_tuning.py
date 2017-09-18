import os
import argparse
from utils import *
from generators import *
from scipy.stats import ks_2samp


parser = argparse.ArgumentParser(description='Script for computing KS and MSD for SDG model without parameter tuning')
parser.add_argument('graphPath', action='store', type=str, help='path of directory that contains the csv graph files')

args = parser.parse_args()
graphPath = args.graphPath

if graphPath[-1] != "/":
    graphPath += "/"


print 'Software & KS in-degree & KS out-degree & MSD in-degree & MSD out-degree \\\ '
for f in sorted(os.listdir(graphPath)):
    KS_in_list = []
    KS_out_list = []
    MSD_in_list = []
    MSD_out_list = []

    graph = loadGraphFromEdgeListTxt(graphPath + f)
    num_nodes = len(graph.nodes())

    in_degree_or = sorted(graph.in_degree().values())
    out_degree_or = sorted(graph.out_degree().values())
    cdf_in_emp = to_cumulative(in_degree_or)
    cdf_out_emp = to_cumulative(out_degree_or)

    num_edges = len(graph.edges())
    epsilon1 = 0.45
    epsilon2 = (1.0 * num_nodes) / num_edges - 0.05
    for i in range(100):
        gen_graph = sdg(num_nodes, num_edges, epsilon1, epsilon2)

        in_degree_gen = sorted(gen_graph.in_degree().values())
        out_degree_gen = sorted(gen_graph.out_degree().values())
        cdf_in_gen = to_cumulative(in_degree_gen)
        cdf_out_gen = to_cumulative(out_degree_gen)

        KS_in_list.append(ks_2samp(cdf_in_emp, cdf_in_gen)[0])
        KS_out_list.append(ks_2samp(cdf_out_emp, cdf_out_gen)[0])
        MSD_in_list.append(np.mean(np.power(np.array(in_degree_gen) - np.array(in_degree_or), 2)))
        MSD_out_list.append(np.mean(np.power(np.array(out_degree_gen) - np.array(out_degree_or), 2)))

    print f.split('.')[0] + ' & ' + str(round(np.mean(np.array(KS_in_list)), 2)) + ' & ' + \
          str(round(np.mean(np.array(KS_out_list)), 2)) + ' & ' + str(round(np.mean(np.array(MSD_in_list)), 2)) + \
          ' & ' + str(round(np.mean(np.array(MSD_out_list)), 2))

