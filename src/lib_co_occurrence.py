import pandas as pd
import numpy as np
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_co_occurrence_matrix(df, target_field):


    # target_field = "affiliation_integration_country"

    # Explode the affiliation_integration_institution column
    df_exploded = df.explode(target_field)

    # Get unique target_field
    unique_target_field = df_exploded[target_field].unique()

    # Create an empty co-occurrence matrix
    co_occurrence_matrix = pd.DataFrame(0, index=unique_target_field, columns=unique_target_field)

    # Iterate through each article
    for _, row in df.iterrows():
        # Get target_field for the current article
        article_target_field = row[target_field]
        
        # Generate all possible pairs of target_field
        target_field_pairs = list(combinations(article_target_field, 2))
        
        # Increment co-occurrence count for each pair
        for inst1, inst2 in target_field_pairs:
            co_occurrence_matrix.loc[inst1, inst2] += 1
            co_occurrence_matrix.loc[inst2, inst1] += 1

    # Set diagonal values to the count of articles for each target_field
    for inst in unique_target_field:
        co_occurrence_matrix.loc[inst, inst] = df_exploded[df_exploded[target_field] == inst].shape[0]

    return co_occurrence_matrix

def convert_co_occurrence_matrix2graph(co_occurrence_matrix, min_degree = 1):
    # Create a graph from the co_occurrence_matrix
    G = nx.from_pandas_adjacency(co_occurrence_matrix)

    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))

    # Remove node with degree < min_degree
    G.remove_nodes_from([node for node, degree in G.degree() if degree < min_degree])

    return G

