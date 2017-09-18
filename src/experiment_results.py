import os
import argparse
from utils import *
from generators import *
from scipy.stats import ks_2samp

parser = argparse.ArgumentParser(description='Generate similarity metrics for generated graphs in latex table for the '
                                             'paper')
parser.add_argument('graphPath', action='store', type=str, help='path of directory that contains the graph csv files')
parser.add_argument('generatedPath', action='store', type=str, help='path of directory that contains the generated '
                                                                    'graph folders')

args = parser.parse_args()
graphPath = args.graphPath
generatedPath = args.generatedPath

if graphPath[-1] != "/":
    graphPath += "/"
if generatedPath[-1] != "/":
    generatedPath += "/"

KS_gen_in = []
KS_gen_out = []
KS_gdgnc_in = []
KS_gdgnc_out = []
KS_bollobas_in = []
KS_bollobas_out = []
MSE_gen_in = []
MSE_gen_out = []
MSE_gdgnc_in = []
MSE_gdgnc_out = []
KS_in = []
KS_out = []
MSD_in = []
MSD_out = []
softwares = []
for folder in ['SDG', 'GDGNC', 'Bollobas']:

    for g in sorted(os.listdir(graphPath)):
        graph = loadGraphFromEdgeListTxt(graphPath + g)
        num_nodes = len(graph.nodes())
        num_edges = len(graph.edges())
        in_degree_or = sorted(graph.in_degree().values())
        out_degree_or = sorted(graph.out_degree().values())
        cdf_in_emp = to_cumulative(in_degree_or)
        cdf_out_emp = to_cumulative(out_degree_or)
        #  compute the spectrum of the original graph
        graph_spectrum = np.real(sorted(nx.linalg.adjacency_spectrum(graph.to_undirected())))
        # compute diameter
        graph_diameter = nx.diameter(graph.to_undirected())

        KS_in_list = []
        KS_out_list = []
        MSD_in_list = []
        MSD_out_list = []
        diam_list = []
        spec_list = []

        for f in sorted(os.listdir(generatedPath + folder + '/' + g.split('.')[0])):
            gen_graph = loadGraphFromEdgeListTxt(generatedPath + folder + '/' + g.split('.')[0] + '/' + f)

            in_degree_gen = sorted(gen_graph.in_degree().values())
            out_degree_gen = sorted(gen_graph.out_degree().values())
            cdf_in_gen = to_cumulative(in_degree_gen)
            cdf_out_gen = to_cumulative(out_degree_gen)

            KS_in_list.append(ks_2samp(cdf_in_emp, cdf_in_gen)[0])
            KS_out_list.append(ks_2samp(cdf_out_emp, cdf_out_gen)[0])
            if folder != 'Bollobas':
                MSD_in_list.append(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gen), 2.0)))
                MSD_out_list.append(np.mean(np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gen),
                                                             2.0))))

        KS_in.append(np.mean(np.array(KS_in_list)))
        KS_out.append(np.mean(np.array(KS_out_list)))
        if folder != 'Bollobas':
            MSD_in.append(np.mean(np.array(MSD_in_list)))
            MSD_out.append(np.mean(np.array(MSD_out_list)))
        softwares.append(g.split('.')[0])
for i in range(10):
    print softwares[i] + ' & ' + str(round(KS_in[i], 2)) + ' & ' + str(round(KS_in[10 + i], 2)) + ' & ' + \
          str(round(KS_in[20 + i], 2)) + ' & ' +  str(round(KS_out[i], 2)) + ' & ' + str(round(KS_out[10 + i], 2)) + \
          ' & ' + str(round(KS_out[20 + i], 2)) + ' & ' + str(round(MSD_in[i], 2)) + ' & ' + \
          str(round(MSD_in[10 + i], 2)) + ' & ' + str(round(MSD_out[i], 2)) + ' & ' + str(round(MSD_out[10 + i], 2)) \
          + '\\\ '

