import argparse
from utils import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from optimize_generators import *

parser = argparse.ArgumentParser(description='Script for generating plots for the paper. For tuned sdg, gdgnc, '
                                             'bollobas and no-tuned sdg')
parser.add_argument('graphFile', action='store', type=str, help='path the csv graph file')
parser.add_argument('resultPath', action='store', type=str, help='path the images will be stored')
args = parser.parse_args()
graphFile = args.graphFile
resultPath = args.resultPath

if resultPath[-1] != "/":
    resultPath += "/"

graph = loadGraphFromEdgeListTxt(graphFile)

in_degree_or = sorted(graph.in_degree().values())
out_degree_or = sorted(graph.out_degree().values())
cdf_in_emp = to_cumulative(in_degree_or)
cdf_out_emp = to_cumulative(out_degree_or)
graph_spectrum = sorted(nx.linalg.adjacency_spectrum(graph.to_undirected()))

gen_graph, _, _ = optimize_sdg(graph)
in_degree_gen = sorted(gen_graph.in_degree().values())
out_degree_gen = sorted(gen_graph.out_degree().values())
cdf_in_gen = to_cumulative(in_degree_gen)
cdf_out_gen = to_cumulative(out_degree_gen)
gen_spectrum = sorted(nx.linalg.adjacency_spectrum(gen_graph.to_undirected()))

gdgnc_graph, _, _ = optimize_gdgnc(graph)
in_degree_gdgnc = sorted(gdgnc_graph.in_degree().values())
out_degree_gdgnc = sorted(gdgnc_graph.out_degree().values())
cdf_in_gdgnc = to_cumulative(in_degree_gdgnc)
cdf_out_gdgnc = to_cumulative(out_degree_gdgnc)
gdgnc_spectrum = sorted(nx.linalg.adjacency_spectrum(gdgnc_graph.to_undirected()))

bollobas_graph, _, _ = optimize_bollobas(graph)
in_degree_bollobas = sorted(bollobas_graph.in_degree().values())
out_degree_bollobas = sorted(bollobas_graph.out_degree().values())
cdf_in_bollobas = to_cumulative(in_degree_bollobas)
cdf_out_bollobas = to_cumulative(out_degree_bollobas)

gen_graph2 = sdg(len(graph.nodes()), len(graph.edges()), 0.45, 0.12)
in_degree_gen2 = sorted(gen_graph2.in_degree().values())
out_degree_gen2 = sorted(gen_graph2.out_degree().values())
cdf_in_gen2 = to_cumulative(in_degree_gen2)
cdf_out_gen2 = to_cumulative(out_degree_gen2)
gen_spectrum2 = sorted(nx.linalg.adjacency_spectrum(gen_graph2.to_undirected()))

pp = PdfPages(resultPath + 'in.pdf')
plt.figure()
ax = plt.subplot(1, 1, 1)

plt.plot(cdf_in_emp, label='Original')
plt.plot(cdf_in_gen, label='SDG tuning')
plt.plot(cdf_in_gdgnc, label='GDGNC tuning')
plt.plot(cdf_in_gen2, label='SDG no tuning')
plt.plot(cdf_in_bollobas, label='Bollobas tuning')

plt.ylabel('Cumulative frequency')
plt.xlabel('In degree')
plt.legend()
plt.xlim([1, 10000])
plt.ylim([0.001, 1.0])
ax.set_xscale('log')
ax.set_yscale('log')
plt.title('In-degree distribution of ant')
pp.savefig()
pp.close()

pp = PdfPages(resultPath + 'out.pdf')
plt.figure()
ax = plt.subplot(1, 1, 1)
plt.plot(cdf_out_emp, label='Original')
plt.plot(cdf_out_gen, label='SDG tuning')
plt.plot(cdf_out_gdgnc, label='GDGNC tuning')
plt.plot(cdf_out_gen2, label='SDG no tuning')
plt.plot(cdf_out_bollobas, label='Bollobas tuning')

plt.ylabel('Cumulative frequency')
plt.xlabel('Out degree')
plt.legend()
plt.xlim([1, 10000])
plt.ylim([0.001, 1.0])
ax.set_xscale('log')
ax.set_yscale('log')
plt.title('Out-degree distribution of ant')
pp.savefig()
pp.close()

pp = PdfPages(resultPath + 'spec.pdf')
plt.figure()
plt.plot(graph_spectrum, label='Original')
plt.plot(gen_spectrum, label='SDG tuning')
plt.plot(gdgnc_spectrum, label='GDGNC tuning')
plt.plot(gen_spectrum2, label='SDG no tuning')
plt.xlabel('Eigenvalue index')
plt.ylabel('Eigenvalue')
plt.title('Sorted spectrum of ant')
plt.legend()
pp.savefig()
pp.close()
plt.show()
