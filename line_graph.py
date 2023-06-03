#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 13:49
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : line_graph.py
# @Statement : The line graph method for the shortest path problem with turn restrictions (SPPTR)
# @Reference : Winter S. Modeling costs of turns in route planning[J]. GeoInformatica, 2002, 6(4): 363-380.
from SPPTR.algorithms import Dijkstra


def find_neighbors(network):
    # find the incoming and outgoing neighbors of each node
    incoming = {}
    outgoing = {}
    for i in network.keys():
        incoming[i] = []
        outgoing[i] = list(network[i].keys())
    for i in network.keys():
        for j in network[i].keys():
            incoming[j].append(i)
    return incoming, outgoing


def main(network, source, destination, tr):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param tr: turn restrictions
    :return:
    """
    incoming, outgoing = find_neighbors(network)
    # Step 1. Create the line graph
    net = {}
    for node1 in network.keys():
        for node2 in outgoing[node1]:
            temp_node = str(node1) + '_' + str(node2)
            net[temp_node] = {}
            for node3 in outgoing[node2]:
                if [node1, node2, node3] not in tr:
                    net[temp_node][str(node2) + '_' + str(node3)] = network[node2][node3]

    # Step 2. Define the sources and destinations
    sources = []
    destinations = []
    for node in outgoing[source]:
        sources.append(str(source) + '_' + str(node))
    for node in incoming[destination]:
        destinations.append(str(node) + '_' + str(destination))

    # Step 3. Add dummy source and dummy destination
    ds = 'dummy source'
    dd = 'dummy destination'
    net[ds] = {}
    net[dd] = {}
    for node in sources:
        [n1, n2] = node.split('_')
        net[ds][node] = network[int(n1)][int(n2)]
    for node in destinations:
        net[node][dd] = 0

    # Step 4. Solve the shortest path problem
    result = Dijkstra.main(net, ds, dd)
    temp_path = result['path'][1: -1]
    path = [source]
    for p in temp_path:
        path.append(int(p.split('_')[1]))
    return {'path': path, 'length': result['length']}


if __name__ == '__main__':
    test_network = {
        0: {2: 1},
        1: {2: 1},
        2: {0: 1, 1: 1, 3: 2, 5: 1},
        3: {4: 1},
        4: {5: 2},
        5: {2: 1},
    }
    s = 0
    d = 5
    tr = [[0, 2, 5]]
    print(main(test_network, s, d, tr))
