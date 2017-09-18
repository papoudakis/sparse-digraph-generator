import argparse
from utils import *
import copy
from generators import *
from optimize_generators import *

parser = argparse.ArgumentParser(description='Node prediction for graph time series with kernel regression')
parser.add_argument('graphPath', action='store', type=str, help='path of directory that contains the csv graph files')
parser.add_argument('resultPathGraphs', action='store', type=str, help='path of directory that results will be stored')
parser.add_argument('resultPathPlotDegree', action='store', type=str, help='path of directory that results will be stored')

args = parser.parse_args()
graphPath = args.graphPath
resultPathGraphs = args.resultPathGraphs
resultPathPlotDegree = args.resultPathPlotDegree

if graphPath[-1] != "/":
    graphPath += "/"
if resultPathGraphs[-1] != "/":
    resultPathGraphs += "/"
if resultPathPlotDegree[-1] != "/":
    resultPathPlotDegree += "/"

try:
    os.makedirs(resultPathGraphs)
except:
    pass
try:
    os.makedirs(resultPathPlotDegree)
except:
    pass

for folder in sorted(os.listdir(graphPath)):
    temp_files = os.listdir(graphPath + folder)
    files = []
    for f in temp_files:
        files.append(f.split('.csv')[0])
    files = sorted(files)
    new_nodes = []
    new_edges = []
    graph1 = loadGraphFromEdgeListTxt(graphPath + folder + '/' + files[0] + '.csv')
    nodes1 = graph1.nodes()
    edges1 = graph1.edges()

    graph2 = loadGraphFromEdgeListTxt(graphPath + folder + '/' + files[i + 1] + '.csv')
    nodes2 = graph2.nodes()
    edges2 = graph2.edges()

    # create an object for the new graph
    gen_graph = copy.deepcopy(graph1)
    # compute the new nodes
    for n in nodes2:
        if n not in nodes1:
            new_nodes.append(n)
    # compute the removed nodes
    for n in nodes1:
        if n not in nodes2:
            gen_graph.remove_node(n)

    # compute the new edges
    for e in edges2:
        if e not in edges1:
            new_edges.append(e)

    # compute the removed edges
    for e in edges1:
        if e not in edges2:
            try:
                gen_graph.remove_edge(e[0], e[1])
            except:
                pass

    num_of_new_nodes = len(new_nodes)
    num_of_new_edges = len(new_edges)

    temp_graph = copy.deepcopy(gen_graph)
    # find the optimal parameters
    best_graph, alpha, beta, epsilon1, epsilon2 = optimize_sedge(gen_graph, graph2, num_of_new_edges, new_nodes)
    if len(best_graph.nodes()) != len(graph2.nodes()):
        print 'Error'
        continue

    in_degree_or = sorted(graph2.in_degree(new_nodes).values())
    out_degree_or = sorted(graph2.out_degree(new_nodes).values())
    cdf_in_emp = to_cumulative(in_degree_or)
    cdf_out_emp = to_cumulative(out_degree_or)

    KS_in_list = []
    KS_out_list = []
    MSD_in_list = []
    MSD_out_list = []

    # generate 100 graphs for the optimized parameters
    for _ in range(100):
        temp_graph = copy.deepcopy(gen_graph)
        evolved_graph = sedge(temp_graph, num_of_new_edges, new_nodes, epsilon1, epsilon2, alpha, beta)
        if len(best_graph.nodes()) != len(graph2.nodes()):
            print 'Error'
            continue
        in_degree_gen = sorted(evolved_graph.in_degree(new_nodes).values())
        out_degree_gen = sorted(evolved_graph.out_degree(new_nodes).values())
        cdf_in_gen = to_cumulative(in_degree_gen)
        cdf_out_gen = to_cumulative(out_degree_gen)
        KS_in_list.append(ks_2samp(cdf_in_emp, cdf_in_gen))
        KS_out_list.append(ks_2samp(cdf_out_emp, cdf_out_gen))
        MSD_in_list.append(np.mean(np.power(np.asarray(in_degree_or) - np.asarray(in_degree_gen), 2.0)))
        MSD_out_list.append(np.mean(np.power(np.asarray(out_degree_or) - np.asarray(out_degree_gen), 2.0)))
    # print in latex table form
    print files[i].split('.csv')[0] + ' & ' + files[i + 1].split('.csv')[0] + ' & ' + str(len(new_nodes)) + ' & ' +\
          str(len(new_edges)) + ' & ' + str(round(np.mean(np.array(KS_in_list)), 2)) + ' & ' + \
          str(round(np.mean(np.array(KS_out_list)), 2)) + ' & ' + str(round(np.mean(np.array(MSD_in_list)), 2)) + \
          ' & ' + str(round(np.mean(np.array(MSD_out_list)), 2))


