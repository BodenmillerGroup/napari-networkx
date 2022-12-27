import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import networkx as nx
from napari_graph import DirectedGraph as DirectedNapariGraph
from napari_graph import UndirectedGraph as UndirectedNapariGraph

from .utils import napari_graph_to_nx_graph

PathLike = Union[str, os.PathLike]
NXWriterFunction = Callable[[nx.Graph, PathLike], None]


# don't forget to update filename_extensions in napari.yaml!
_NX_WRITER_FUNCTIONS: Dict[str, NXWriterFunction] = {
    ".adjlist": nx.write_adjlist,
    ".multiline-adjlist": nx.write_multiline_adjlist,
    ".edgelist": nx.write_edgelist,
    ".weighted-edgelist": nx.write_weighted_edgelist,
    ".gexf": nx.write_gexf,
    ".gml": nx.write_gml,
    ".graphml": nx.write_graphml,
    ".graph6": nx.write_graph6,
    ".sparse6": nx.write_sparse6,
    ".net": nx.write_pajek,
}


def write_graph(path: str, data: Any, meta: dict) -> List[str]:
    if not isinstance(data, (DirectedNapariGraph, UndirectedNapariGraph)):
        raise ValueError("`data` is not a napari_graph `Graph` instance")
    suffix = Path(path).suffix.lower()
    if suffix in (".gz", ".bz2"):
        suffix = Path(path).with_suffix("").suffix.lower()
    nx_writer_function = _NX_WRITER_FUNCTIONS.get(suffix)
    if nx_writer_function is not None:
        nx_graph = napari_graph_to_nx_graph(data)
        nx_writer_function(nx_graph, path)
        return [path]
    return []
