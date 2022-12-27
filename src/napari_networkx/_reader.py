import os
from functools import partial
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import networkx as nx
from napari.types import LayerDataTuple

from .utils import nx_graph_to_napari_graph

PathLike = Union[str, os.PathLike]
NXReaderFunction = Callable[[PathLike], nx.Graph]


# don't forget to update filename_patterns in napari.yaml!
NX_READER_FUNCTIONS: Dict[str, NXReaderFunction] = {
    ".adjlist": nx.read_adjlist,
    ".multiline-adjlist": nx.read_multiline_adjlist,
    ".edgelist": nx.read_edgelist,
    ".weighted-edgelist": nx.read_weighted_edgelist,
    ".gexf": nx.read_gexf,
    ".gml": nx.read_gml,
    ".graphml": nx.read_graphml,
    ".leda": nx.read_leda,
    ".graph6": nx.read_graph6,
    ".sparse6": nx.read_sparse6,
    ".net": nx.read_pajek,
}


def napari_get_reader(
    path: PathLike,
) -> Optional[Callable[[PathLike], List[LayerDataTuple]]]:
    if isinstance(path, list):
        raise ValueError("Can only open single graph file")
    suffix = Path(path).suffix.lower()
    if suffix in (".gz", ".bz2"):
        suffix = Path(path).with_suffix("").suffix.lower()
    nx_reader_function = NX_READER_FUNCTIONS.get(suffix)
    if nx_reader_function is not None:
        return partial(
            graph_reader_function, nx_reader_function=nx_reader_function
        )
    return None


def graph_reader_function(
    path: PathLike, nx_reader_function: NXReaderFunction
) -> List[LayerDataTuple]:
    nx_graph = nx_reader_function(path)
    napari_graph = nx_graph_to_napari_graph(nx_graph)
    return [(napari_graph, {}, "graph")]
