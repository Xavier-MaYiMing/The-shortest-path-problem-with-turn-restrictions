#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/14 13:59
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : labeling_v2.py
# @Statement : The link-based-Dijkstra for the shortest path problem with turn restrictions
# @Reference : Li Qingquan, et al. A hybrid link-node approach for finding shortest paths in road networks with turn restrictions[J]. Transactions in GIS, 2015.
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
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbor(network)
    explored_label = []
    p_list = {}  # path label
    d_list = {}  # length label
    queue = []
    label_in = 0
    label_out = 0
    inf = 1e6
    restricted_node = set()
    for turn in turn_restrictions:
        if turn[1] != source and turn[1] != destination:
            restricted_node.add(turn[1])

    for i in range(nn):
        for j in neighbor[i]:
            if j in restricted_node:
                temp_index = str([i, j])
            else:
                temp_index = j
            p_list[temp_index] = []
            d_list[temp_index] = inf

    temp_index = source
    p_list[temp_index] = [source]
    d_list[temp_index] = 0

    for j in neighbor[source]:
        temp_cost = network[source][j]
        temp_path = [source, j]
        if j in restricted_node:
            temp_index = str([source, j])
        else:
            temp_index = j
        heapq.heappush(queue, (temp_cost, label_in, temp_index))
        label_in += 1
        p_list[temp_index] = temp_path
        d_list[temp_index] = temp_cost

    # Step 2. Path selection
    while queue:
        temp_cost, _, temp_label = heapq.heappop(queue)
        label_out += 1
        if temp_label in explored_label:
            continue
        explored_label.append(temp_label)
        temp_path = p_list[temp_label]
        i = temp_path[-2]
        j = temp_path[-1]
        if j == destination:
            return {'path': p_list[temp_label], 'length': temp_cost}, label_in, label_out

        # Step 3. Path extension
        for k in neighbor[j]:
            if [i, j, k] not in turn_restrictions:
                if k in restricted_node and str([j, k]) not in explored_label:
                    new_path_cost = temp_cost + network[j][k]
                    temp_index = str([j, k])
                    if new_path_cost < d_list[temp_index]:
                        new_path = copy.deepcopy(temp_path)
                        new_path.append(k)
                        d_list[temp_index] = new_path_cost
                        p_list[temp_index] = new_path
                        heapq.heappush(queue, (new_path_cost, label_in, temp_index))
                        label_in += 1
                elif k not in restricted_node and k not in explored_label:
                    new_path_cost = temp_cost + network[j][k]
                    if new_path_cost < d_list[k]:
                        new_path = copy.deepcopy(temp_path)
                        new_path.append(k)
                        d_list[k] = new_path_cost
                        p_list[k] = new_path
                        heapq.heappush(queue, (new_path_cost, label_in, k))
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
    tr = [[0, 2, 5]]
    print(main(test_network, 0, 5, tr))
