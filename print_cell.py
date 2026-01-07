import json

def print_cell():
    with open('model_comparison.ipynb', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i, cell in enumerate(data['cells']):
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if 'evaluate_model' in source:
                for line in cell['source']:
                    if 'RocCurveDisplay' in line:
                        print(f"FOUND LINE: {line.strip()}")

if __name__ == "__main__":
    print_cell()
