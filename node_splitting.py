#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/13 16:01
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : node_splitting.py
# @Statement : The node splitting method for the shortest path problem with turn restrictions
# @Reference : Kirby R F, Potts R B. The minimum route problem for networks with turn penalties and prohibitions[J]. Transportation Research, 1969, 3(3): 397-408.
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
    # Step 1. Find restricted nodes
    rn = set()  # restricted nodes
    for turn in tr:
        if turn[1] != source and turn[1] != destination:
            rn.add(turn[1])

    # Step 2. Add dummy nodes
    for node1 in rn:
        for node2 in incoming[node1]:
            network[str(node1) + '_' + str(node2) + '_i'] = {}
        for node3 in outgoing[node1]:
            network[str(node1) + '_' + str(node3) + '_o'] = {}
    for node1 in rn:
        for node2 in incoming[node1]:
            if node2 in rn:
                network[str(node2) + '_' + str(node1) + '_o'][str(node1) + '_' + str(node2) + '_i'] = network[node2][node1]
            else:
                network[node2][str(node1) + '_' + str(node2) + '_i'] = network[node2][node1]
        for node3 in outgoing[node1]:
            if node3 in rn:
                network[str(node1) + '_' + str(node3) + '_o'][str(node3) + '_' + str(node1) + '_i'] = network[node1][node3]
            else:
                network[str(node1) + '_' + str(node3) + '_o'][node3] = network[node1][node3]

    # Step 3. Add edges among dummy nodes
    for j in rn:
        for i in incoming[j]:
            for k in outgoing[j]:
                if [i, j, k] not in tr:
                    network[str(j) + '_' + str(i) + '_i'][str(j) + '_' + str(k) + '_o'] = 0

    # Step 4. Delete restricted nodes
    for node in rn:
        network.pop(node)
    for node1 in network.keys():
        removal = []
        for node2 in network[node1].keys():
            if node2 in rn:
                removal.append(node2)
        for r in removal:
            network[node1].pop(r)

    # Step 5. Use Dijkstra's algorithm to solve the problem
    result = Dijkstra.main(network, source, destination)
    result_path = result['path']
    path = []
    ind = 0
    while ind < len(result_path):
        if type(result_path[ind]) == str:
            ind += 1
            path.append(int(result_path[ind].split('_')[0]))
        else:
            path.append(result_path[ind])
        ind += 1
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

