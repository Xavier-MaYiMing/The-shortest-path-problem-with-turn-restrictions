### The Shortest Path Problem with Time Windows



##### The shortest path problem with turn restrictions (SPPTR) aims to find the shortest path on a network with turn restrictions. Five different algorithms and the 0-1 programming model for the SPPTR.



##### Reference: Gutiérrez E, Medaglia A L. Labeling algorithm for the shortest path problem with turn prohibitions with application to large-scale road networks[J]. Annals of Operations Research, 2008, 157(1): 169-182. (labeling_v1)

##### Reference: Li Qingquan, et al. A hybrid link-node approach for finding shortest paths in road networks with turn restrictions[J]. Transactions in GIS, 2015. (labeling_v2)

##### Referenece: Kirby R F, Potts R B. The minimum route problem for networks with turn penalties and prohibitions[J]. Transportation Research, 1969, 3(3): 397-408. (node_spliting)

##### Reference: Winter S. Modeling costs of turns in route planning[J]. GeoInformatica, 2002, 6(4): 363-380. (line_graph)

##### labeling_v3 is the labeling algorithm for the SPPTR with improved labeling strategies.

##### SPPTR_01 is a 0-1 mathematical programmimg model for the SPPTR.

| Variables   | Meaning                                                      |
| ----------- | ------------------------------------------------------------ |
| network     | Dictionary, {node1: {node2: [cost1, time1], node3: [cost2, time2] ...}, ...} |
| source      | The source node                                              |
| destination | The destination node                                         |
| tr          | Turn restrictions                                            |
| nn          | The number of nodes                                          |
| neighbor    | Dictionary, {node1: {node2: length, node3: length, ...}, ...} |
| p_list      | List, the path label associated to each label                |
| queue       | The priority queue, which outputs the label that has the minimum value of the summation of objectives at each iteration |
| omega       | List, the ever explored labels                               |
| label_in    | The number of labels added into the priority queue           |
| label_out   | The number of labels extracted from the priority queue       |

#### Example

![](https://github.com/Xavier-MaYiMing/The-labeling-algorithms-for-the-shortest-path-problem-with-turn-restrictions/blob/main/SPPTR%20example.png)

```python
if __name__ == '__main__':
    test_network = {
        0: {2: 1},
        1: {2: 1},
        2: {0: 1, 1: 1, 3: 2, 5: 1},
        3: {4: 1},
        4: {5: 2},
        5: {2: 1},
    }
    tr = [[0, 2, 5]]
    print(main(test_network, 0, 5, tr))
```

##### Output (labeling_v1):

```python
({'path': [0, 2, 1, 2, 5], 'length': 4}, 8, 7)
```

##### Output (labeling_v2):

```python
({'path': [0, 2, 1, 2, 5], 'length': 4}, 6, 6)
```

The results indicate that labeling_v2 is more efficient than labeling_v1, as it adds and extracts less labels from the priority queue.

