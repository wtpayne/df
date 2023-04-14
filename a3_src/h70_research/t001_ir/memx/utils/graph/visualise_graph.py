import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import plotly.graph_objs as go
import numpy as np


class VRGraphVisualizer:
    def __init__(self, graphml_file):
        self.graphml_file = graphml_file

    def visualize(self):
        # Load the GraphML file
        try:
            G = nx.read_graphml(self.graphml_file)
        except FileNotFoundError:
            print("Error: Could not find GraphML file")
            return
        except Exception as e:
            print(f"Error: {e}")
            return

        # Use graphviz_layout to create 3D coordinates for nodes
        pos = graphviz_layout(G, prog='neato')

        # Extract coordinates into an array
        coords = np.array(list(pos.values()))

        # Define color and z-value for each part of speech
        color_dict = {
            'Noun': 'blue',
            'Verb': 'green',
            'Adjective': 'red',
            'Adverb': 'orange',
            'Article': 'purple',
            'Preposition': 'yellow',
            'Determiner': 'pink',
            'PP': 'cyan',
            'VP': 'magenta',
            'NP': 'brown'
        }

        z_dict = {
            'Noun': 0,
            'Verb': 0,
            'Adjective': 0,
            'Adverb': 0,
            'Article': 0,
            'Preposition': 0,
            'Determiner': 0,
            'PP': 0,
            'VP': 0,
            'NP': 0
        }

        # Create dictionary mapping nodes to their part of speech
        pos_dict = {}
        for n in G.nodes():
            if 'part_of_speech' in G.nodes[n]:
                pos_dict[n] = G.nodes[n]['part_of_speech']
            elif 'phrase_type' in G.nodes[n]:
                pos_dict[n] = G.nodes[n]['phrase_type']
            else:
                print(f"Error: Node {n} does not have part of speech information")
                return

        # Create trace for nodes
        node_trace = go.Scatter3d(
            x=coords[:, 0], y=coords[:, 1], z=[z_dict[pos_dict[n]] for n in G.nodes()],
            mode='markers',
            marker=dict(
                size=8,
                line=dict(width=0.5),
                color=[color_dict[pos_dict[n]] for n in G.nodes()],
                opacity=0.8
            ),
            text=[G.nodes[n]['label'] for n in G.nodes()]
        )

        # Create trace for edges
        edge_trace = go.Scatter3d(
            x=[], y=[], z=[],
            mode='lines',
            line=dict(width=1, color='black'),
            hoverinfo='none'
        )

        # Add edges to the edge trace
        for source, target in G.edges():
            source_pos = coords[list(G.nodes()).index(source)]
            target_pos = coords[list(G.nodes()).index(target)]
            edge_trace['x'] += (source_pos[0], target_pos[0], None)
            edge_trace['y'] += (source_pos[1], target_pos[1], None)
            edge_trace['z'] += (z_dict[pos_dict[source]], z_dict[pos_dict[target]], None)

        # Create the figure
        fig = go.Figure(data=[node_trace, edge_trace])

        # Set layout parameters
        fig.update_layout(
            showlegend=True,
            legend_title='Part of Speech',
            scene=dict(
                xaxis=dict(title='X'),
                yaxis=dict(title='Y'),
                zaxis=dict(title='Part of Speech'),
            ),
            margin=dict(l=0, r=0, b=0, t=0),
        )

        # Add legend
        for pos in z_dict:
            fig.add_trace(go.Scatter3d(
                x=[None], y=[None], z=[z_dict[pos]],
                mode='markers',
                marker=dict(
                    size=8,
                    line=dict(width=0.5),
                    color='blue',
                    opacity=0.8
                ),
                name=pos
            ))

        # Show the figure
        fig.show()


vr_vis = VRGraphVisualizer('./example.graphml')
vr_vis.visualize()
