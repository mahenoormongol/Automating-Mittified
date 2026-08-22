import json
from pathlib import Path

ast = json.loads(Path('graphify-out/.graphify_ast.json').read_text())
# Create dummy semantic json
sem = {'nodes': [], 'edges': [], 'hyperedges': [], 'input_tokens': 0, 'output_tokens': 0}
Path('graphify-out/.graphify_semantic.json').write_text(json.dumps(sem, indent=2))

merged = {
    'nodes': ast['nodes'],
    'edges': ast['edges'],
    'hyperedges': [],
    'input_tokens': 0,
    'output_tokens': 0,
}
Path('graphify-out/.graphify_extract.json').write_text(json.dumps(merged, indent=2))
print(f"Merged: {len(ast['nodes'])} nodes, {len(ast['edges'])} edges (AST only)")
