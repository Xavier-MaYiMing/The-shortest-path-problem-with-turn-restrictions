#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 16:27
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling_v1.py
# @Statement : The link-based labeling method for the shortest path problem with turn restrictions (SPPTR)
# @Reference : Gutiérrez E, Medaglia A L. Labeling algorithm for the shortest path problem with turn prohibitions with application to large-scale road networks[J]. Annals of Operations Research, 2008, 157(1): 169-182.
from numpy import inf
from pqdict import PQDict


def find_neighbors(network):
    # find the neighbors of each node
    neighbor = []
    for i in network.keys():
        neighbor.append(list(network[i].keys()))
    return neighbor


def main(network, source, destination, tr):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param tr: turn restrictions
    :return:
    """
    # Step 1. Initialize parameters
    neighbor = find_neighbors(network)
    omega = []  # the list of explored labels
    queue = PQDict({})  # priority queue
    p_list = {}  # path label
    label_in = 0  # the number of labels added to the priority queue
    label_out = 0  # the number of labels popped from the priority queue

    # Step 2. Add the first labels
    for node in neighbor[source]:
        ind = str([source, node])
        queue[ind] = network[source][node]
        p_list[ind] = [source, node]
        label_in += 1

    # Step 3. The main loop
    while queue:

        # Step 3.1. Select the label with the minimum length
        (label, length) = queue.popitem()
        label_out += 1
        path = p_list[label]
        omega.append(label)
        i = path[-2]
        j = path[-1]
        if j == destination:
            return {
                'path': path,
                'length': length,
                'label in': label_in,
                'label out': label_out,
            }

        # Step 3.2. Extend labels
        for k in neighbor[j]:
            ind = str([j, k])
            if [i, j, k] not in tr and ind not in omega:
                temp_length = length + network[j][k]
                if temp_length < queue.get(ind, inf):
                    temp_path = path.copy()
                    temp_path.append(k)
                    queue[ind] = temp_length
                    p_list[ind] = temp_path
                    label_in += 1

    return {}


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
