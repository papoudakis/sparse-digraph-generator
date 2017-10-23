import os
import argparse
from utils import *
from optimize_generators import *
from generators import *


parser = argparse.ArgumentParser(description='Script for generating 100 graphs for each software for the paper '
                                             'experiments')
parser.add_argument('graphPath', action='store', type=str, help='path of directory that contains the csv graph files')
parser.add_argument('resultPath', action='store', type=str, help='path of directory that graphs will be stored')

args = parser.parse_args()
graphPath = args.graphPath
resultPath = args.resultPath

if graphPath[-1] != "/":
    graphPath += "/"
if resultPath[-1] != "/":
    resultPath += "/"

KS_in_gen = []
KS_out_gen = []
KS_in_gdgnc = []
KS_out_gdgnc = []
KS_in_bol = []
KS_out_bol = []
MSD_in_gen = []
MSD_out_gen = []
MSD_in_gdgnc = []
MSD_out_gdgnc = []

try:
    os.makedirs(resultPath)
except:
    pass
try:
    os.makedirs(resultPath + 'GDGNC')
except:
    pass
try:
    os.makedirs(resultPath + 'SDG')
except:
    pass
try:
    os.makedirs(resultPath + 'Bollobas')
except:
    pass


for f in sorted(os.listdir(graphPath)):
    graph = loadGraphFromEdgeListTxt(graphPath + f)
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())

    in_degree_or = sorted(graph.in_degree().values())
    out_degree_or = sorted(graph.out_degree().values())
    cdf_in_emp = to_cumulative(in_degree_or)
    cdf_out_emp = to_cumulative(out_degree_or)

    try:
        os.makedirs(resultPath + 'GDGNC/' + f.split('.')[0])
    except:
        pass
    try:
        os.makedirs(resultPath + 'SDG/' + f.split('.')[0])
    except:
        pass
    try:
        os.makedirs(resultPath + 'Bollobas/' + f.split('.')[0])
    except:
        pass

    #  compute the spectrum of the original graph
    graph_spectrum = sorted(nx.linalg.adjacency_spectrum(graph.to_undirected()))

    _, p, q = optimize_gdgnc(graph)
    KS_in_list_gdgnc = []
    KS_out_list_gdgnc = []
    MSD_in_list_gdgnc = []
    MSD_out_list_gdgnc = []
    print 'Done with GDGNC optimization'

    for i in range(100):

        gdgnc_graph = gdgnc(num_nodes, p, q)

        in_degree_gdgnc = sorted(gdgnc_graph.in_degree().values())
        out_degree_gdgnc = sorted(gdgnc_graph.out_degree().values())
        cdf_in_gdgnc = to_cumulative(in_degree_gdgnc)
        cdf_out_gdgnc = to_cumulative(out_degree_gdgnc)

        KS_in_list_gdgnc.append(ks_2samp(cdf_in_emp, cdf_in_gdgnc))
        KS_out_list_gdgnc.append(ks_2samp(cdf_out_emp, cdf_out_gdgnc))
        MSD_in_list_gdgnc.append(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gdgnc), 2.0)))
        MSD_out_list_gdgnc.append(np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gdgnc),  2.0)))

        f_result = open(resultPath + 'GDGNC/' + f.split('.')[0] + '/' + f.split('.')[0] + str(i) + '.csv', 'w')
        for e in gdgnc_graph.edges():
            f_result.write(str(e[0]) + ';' + str(e[1]) + '\n')
        f_result.close()

    print 'Done with GDGNC'

    _, epsilon1, epsilon2 = optimize_sdg(graph)
    print 'Done with generative optimization'
    KS_in_list = []
    KS_out_list = []
    MSD_in_list = []
    MSD_out_list = []
    diam_gen = []
    spec_gen = []

    for i in range(100):
        gen_graph = sdg(num_nodes, num_edges, epsilon1, epsilon2)

        in_degree_gen = sorted(gen_graph.in_degree().values())
        out_degree_gen = sorted(gen_graph.out_degree().values())
        cdf_in_gen = to_cumulative(in_degree_gen)
        cdf_out_gen = to_cumulative(out_degree_gen)

        KS_in_list.append(ks_2samp(cdf_in_emp, cdf_in_gen))
        KS_out_list.append(ks_2samp(cdf_out_emp, cdf_out_gen))
        MSD_in_list.append(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gen), 2.0)))
        MSD_out_list.append(np.mean(np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gen), 2.0))))

        f_result = open(resultPath + 'SDG/' + f.split('.')[0] + '/' + f.split('.')[0] + str(i) + '.csv', 'w')
        for e in gen_graph.edges():
            f_result.write(str(e[0]) + ';' + str(e[1]) + '\n')
        f_result.close()
        print nx.is_connected(gen_graph.to_undirected())
    print 'Done with sdg'

    _, alpha, beta = optimize_bollobas(graph)
    print 'Done with bollobas optimization'
    KS_in_list_bollobas = []
    KS_out_list_bollobas = []
    diam_boll = []
    for i in range(100):
        bollobas_graph = bollobas(num_edges, alpha, beta)
        in_degree_bollobas = sorted(bollobas_graph.in_degree().values())
        out_degree_bollobas = sorted(bollobas_graph.out_degree().values())
        cdf_in_bollobas = to_cumulative(in_degree_bollobas)
        cdf_out_bollobas = to_cumulative(out_degree_bollobas)

        KS_in_list_bollobas.append(ks_2samp(cdf_in_emp, cdf_in_bollobas))
        KS_out_list_bollobas.append(ks_2samp(cdf_out_emp, cdf_out_bollobas))
        
        f_result = open(resultPath + 'Bollobas/' + f.split('.')[0] + '/' + f.split('.')[0] + str(i) + '.csv', 'w')
        for e in bollobas_graph.edges():
            f_result.write(str(e[0]) + ';' + str(e[1]) + '\n')
        f_result.close()

    print 'Done with bollobas'
