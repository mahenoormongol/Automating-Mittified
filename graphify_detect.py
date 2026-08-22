import json
from graphify.detect import detect
from pathlib import Path
import os

input_path = 'src'
result = detect(Path(input_path))
with open('graphify-out/.graphify_detect.json', 'w') as f:
    json.dump(result, f)
# Only print the summary as per instructions
print(f"Corpus: {result['total_files']} files · ~{result['total_words']} words")
for cat, files in result.get('files', {}).items():
    if files:
        exts = set(Path(f).suffix for f in files)
        print(f"  {cat}: {len(files)} files ({' '.join(exts)})")
