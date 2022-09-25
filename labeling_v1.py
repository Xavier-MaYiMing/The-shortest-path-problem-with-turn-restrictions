#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/12 7:05
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling_v1.py
# @Statement : The link-based-Dijkstra's algorithm for the shortest path problem with turn restrictions
# @Reference : Gutiérrez E, Medaglia A L. Labeling algorithm for the shortest path problem with turn prohibitions with application to large-scale road networks[J]. Annals of Operations Research, 2008, 157(1): 169-182.
import copy
import heapq


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def main(network, source, destination, turn_restrictions):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param turn_restrictions: turn restrictions [[node1, node2, node3], ...]
    :return:
    """
    nn = len(network)  # node number
    neighbor = find_neighbor(network)
    omega1 = []  # searched links
    omega2 = []  # unsearched links
    queue = []
    d_list = {}  # length label
    p_list = {}  # path label
    label_in = 0
    label_out = 0
    inf = 1e6
    best_index = 0
    for i in range(nn):
        for j in neighbor[i]:
            omega2.append([i, j])
            temp_index = str([i, j])
            d_list[temp_index] = inf
            p_list[temp_index] = []
    for node in neighbor[source]:
        temp_length = network[source][node]
        temp_index = str([source, node])
        d_list[temp_index] = temp_length
        p_list[temp_index] = [source, node]
        heapq.heappush(queue, (temp_length, label_in, [source, node]))
        label_in += 1
    while queue:
        dis, _, ak = heapq.heappop(queue)
        label_out += 1
        omega1.append(ak)
        omega2.remove(ak)
        node1 = ak[0]
        node2 = ak[1]
        best_index = str(ak)
        if dis >= inf:
            return {}
        elif node2 == destination:
            break
        for node in neighbor[node2]:
            if [node2, node] in omega2 and [node1, node2, node] not in turn_restrictions:
                temp_index = str([node2, node])
                temp_length = dis + network[node2][node]
                if d_list[temp_index] > temp_length:
                    d_list[temp_index] = temp_length
                    temp_path = copy.deepcopy(p_list[best_index])
                    temp_path.append(node)
                    p_list[temp_index] = temp_path
                    heapq.heappush(queue, (temp_length, label_in, [node2, node]))
                    label_in += 1
    result = {'path': p_list[best_index], 'length': d_list[best_index]}
    return result, label_in, label_out


if __name__ == '__main__':
    test_network = {
        0: {2: 1},
        1: {2: 1},
        2: {0: 1, 1: 2, 3: 2},
        3: {4: 1},
        4: {5: 2},
        5: {2: 1},
    }
    tr = [[0, 2, 5]]
    print(main(test_network, 0, 5, tr))
