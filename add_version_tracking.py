"""
Script to add library version tracking cells to all notebooks for reproducibility.
This ensures all notebooks record their library versions.
"""

import json
import os

# Library version cell to add
version_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Record library versions for reproducibility\n",
        "import sys\n",
        "print(\"=\"*60)\n",
        "print(\"LIBRARY VERSIONS (for reproducibility)\")\n",
        "print(\"=\"*60)\n",
        "print(f\"Python version: {sys.version}\")\n",
        "print(f\"NumPy version: {np.__version__}\")\n",
        "print(f\"Pandas version: {pd.__version__}\")\n",
        "print(f\"Scikit-learn version: {sklearn.__version__}\")\n",
        "print(f\"Matplotlib version: {matplotlib.__version__}\")\n",
        "print(f\"Seaborn version: {sns.__version__}\")\n",
        "print(f\"Random State: {RANDOM_STATE}\")\n",
        "print(\"=\"*60)"
    ]
}

notebooks = [
    "analysis.ipynb",
    "model_evaluation_comparison.ipynb",
    "random_forest_model.ipynb",
    "rf_vs_best_model_comparison.ipynb",
    "kmeans_clustering_analysis.ipynb",
    "dbscan_clustering_analysis.ipynb"
]

def add_version_cell_to_notebook(notebook_path):
    """Add library version tracking cell to a notebook if not already present."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Check if version cell already exists
        has_version_cell = False
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if 'LIBRARY VERSIONS' in source and 'reproducibility' in source:
                    has_version_cell = True
                    break
        
        if not has_version_cell:
            # Find the first code cell (usually imports)
            insert_index = 1
            for i, cell in enumerate(nb['cells']):
                if cell['cell_type'] == 'code':
                    insert_index = i + 1
                    break
            
            # Insert version cell after first code cell
            nb['cells'].insert(insert_index, version_cell)
            
            # Save modified notebook
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=4)
            
            print(f"✅ Added version cell to {notebook_path}")
        else:
            print(f"ℹ️  Version cell already exists in {notebook_path}")
    
    except Exception as e:
        print(f"❌ Error processing {notebook_path}: {e}")

if __name__ == "__main__":
    print("Adding library version tracking to notebooks...\n")
    
    for notebook in notebooks:
        if os.path.exists(notebook):
            add_version_cell_to_notebook(notebook)
        else:
            print(f"⚠️  Notebook not found: {notebook}")
    
    print("\n✅ Done! All notebooks now include library version tracking.")
