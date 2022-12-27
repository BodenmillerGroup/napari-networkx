from typing import Union

import networkx as nx
from napari_graph import DirectedGraph as DirectedNapariGraph
from napari_graph import UndirectedGraph as UndirectedNapariGraph


def nx_graph_to_napari_graph(
    nx_graph: nx.Graph,
) -> Union[DirectedNapariGraph, UndirectedNapariGraph]:
    raise NotImplementedError()  # TODO


def napari_graph_to_nx_graph(
    napari_graph: Union[DirectedNapariGraph, UndirectedNapariGraph]
) -> nx.Graph:
    raise NotImplementedError()  # TODO
