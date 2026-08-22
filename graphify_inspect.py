import json
from networkx.readwrite import json_graph
from pathlib import Path

data = json.loads(Path('graphify-out/graph.json').read_text())
analysis = json.loads(Path('graphify-out/.graphify_analysis.json').read_text())
communities = analysis['communities']

for cid, nodes in communities.items():
    labels = []
    for nid in nodes:
        node_data = next((n for n in data['nodes'] if n['id'] == nid), {})
        labels.append(node_data.get('label', nid))
    print(f"Community {cid}: {', '.join(labels[:10])}")
