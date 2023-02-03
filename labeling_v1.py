#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/1/12 9:02
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling_v1.py
# @Statement : The link-based-Dijkstra's algorithm for the shortest path problem with turn restrictions
# @Reference : Gutiérrez E, Medaglia A L. Labeling algorithm for the shortest path problem with turn prohibitions with application to large-scale road networks[J]. Annals of Operations Research, 2008, 157(1): 169-182.
import heapq


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: [[the neighbor nodes of node1], [the neighbor nodes of node2], ...]
    """
    neighbor = []
    for i in range(len(network)):
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
    # Step 1. Initialize parameters
    nn = len(network)  # node number
    neighbor = find_neighbor(network)
    omega = []  # the list to store explored labels
    queue = []  # the priority queue
    l_list = {}  # length label
    p_list = {}  # path_ label
    label_in = 0  # the number of labels added in the priority queue
    label_out = 0  # the number of labels popped from the priority queue
    inf = 1e10

    # Step 2. Initialize labels
    for i in range(nn):
        for j in neighbor[i]:
            temp_index = str([i, j])
            l_list[temp_index] = inf
            p_list[temp_index] = []

    # Step 3. Add the first labels
    for node in neighbor[source]:
        temp_length = network[source][node]
        temp_index = str([source, node])
        l_list[temp_index] = temp_length
        p_list[temp_index] = [source, node]
        heapq.heappush(queue, (temp_length, label_in, [source, node]))
        label_in += 1

    # Step 4. The main loop
    while queue:

        # Step 4.1. Select the label with the minimum length
        length, _, label = heapq.heappop(queue)
        path = p_list[str(label)]
        label_out += 1
        omega.append(label)
        i = label[0]
        j = label[1]
        if length >= inf:  # no feasible solution
            return {}
        elif j == destination:
            return {
                'path': path,
                'length': length,
                'label in': label_in,
                'label out': label_out
            }

        # Step 4.2. Extend labels
        for k in neighbor[j]:
            if [j, k] not in omega and [i, j, k] not in turn_restrictions:
                temp_index = str([j, k])
                temp_length = length + network[j][k]
                if l_list[temp_index] > temp_length:
                    l_list[temp_index] = temp_length
                    temp_path = path.copy()
                    temp_path.append(k)
                    p_list[temp_index] = temp_path
                    heapq.heappush(queue, (temp_length, label_in, [j, k]))
                    label_in += 1

    return {}


if __name__ == '__main__':
    test_network = {
        0: {2: 1},
        1: {2: 1},
        2: {0: 1, 1: 2, 3: 2},
        3: {4: 1},
        4: {5: 2},
        5: {2: 1},
    }
    s = 0
    d = 5
    tr = [[0, 2, 5]]
    print(main(test_network, s, d, tr))
