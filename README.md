### The Labeling Algorithms for the Shortest Path Problem with Time Windows

##### Reference: Gutiérrez E, Medaglia A L. Labeling algorithm for the shortest path problem with turn prohibitions with application to large-scale road networks[J]. Annals of Operations Research, 2008, 157(1): 169-182. (labeling_v1)

##### Reference: Li Qingquan, et al. A hybrid link-node approach for finding shortest paths in road networks with turn restrictions[J]. Transactions in GIS, 2015. (labeling_v2)

The shortest path problem with turn restrictions aims to find the shortest path on a network with turn restrictions.

| Variables   | Meaning                                                      |
| ----------- | ------------------------------------------------------------ |
| network     | Dictionary, {node1: {node2: [cost1, time1], node3: [cost2, time2] ...}, ...} |
| source      | The source node                                              |
| destination | The destination node                                         |
| nn          | The number of nodes                                          |
| neighbor    | Dictionary, {node1: {node2: length, node3: length, ...}, ...} |
| l_list      | List, the length label associated to each label              |
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
        2: {0: 1, 1: 2, 3: 2},
        3: {4: 1},
        4: {5: 2},
        5: {2: 1},
    }
    tr = [[0, 2, 5]]
    print(main(test_network, 0, 5, tr))
```

##### Output (labeling_v1):

```python
({'path': [0, 2, 3, 4, 5], 'length': 6}, 7, 7)
```

##### Output (labeling_v2):

```python
({'path': [0, 2, 3, 4, 5], 'length': 6}, 6, 6)
```

The results indicate that labeling_v2 is more efficient than labeling_v1, as it adds and extracts less labels from the priority queue.

