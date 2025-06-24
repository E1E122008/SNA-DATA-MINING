import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def analyze(df, analysis_type):
    df.columns = [c.lower() for c in df.columns]
    G = nx.Graph()
    for idx, row in df.iterrows():
        user = row['username']
        tagged = row.get('tagged_users', [])
        for t in tagged:
            G.add_edge(user, t)
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    influencers = sorted(
        [{'user': n, 'degree': degree[n], 'betweenness': betweenness[n]} for n in G.nodes],
        key=lambda x: x['degree'], reverse=True
    )[:10]
    graph_json = nx.readwrite.json_graph.node_link_data(G)
    # Generate gambar graph
    img = BytesIO()
    plt.figure(figsize=(6, 4))
    nx.draw(G, with_labels=True, node_color='#43ea7f', edge_color='#54a0ff', font_weight='bold')
    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    graph_img_base64 = base64.b64encode(img.getvalue()).decode()
    return {
        'graph_url': f'data:image/png;base64,{graph_img_base64}',
        'influencers': influencers
    } 