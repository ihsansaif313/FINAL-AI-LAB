"""
Script to add library version tracking cells to all notebooks for reproducibility.
This version fixes the NameError by importing all required modules within the version cell.
"""

import json
import os

# Library version cell to add
version_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {
        "tags": ["reproducibility"]
    },
    "outputs": [],
    "source": [
        "# Record library versions for reproducibility\n",
        "import sys\n",
        "import numpy as np\n",
        "import pandas as pd\n",
        "import sklearn\n",
        "import matplotlib\n",
        "import seaborn as sns\n",
        "\n",
        "print(\"=\"*60)\n",
        "print(\"LIBRARY VERSIONS (for reproducibility)\")\n",
        "print(\"=\"*60)\n",
        "print(f\"Python version: {sys.version}\")\n",
        "print(f\"NumPy version: {np.__version__}\")\n",
        "print(f\"Pandas version: {pd.__version__}\")\n",
        "print(f\"Scikit-learn version: {sklearn.__version__}\")\n",
        "print(f\"Matplotlib version: {matplotlib.__version__}\")\n",
        "print(f\"Seaborn version: {sns.__version__}\")\n",
        "try:\n",
        "    print(f\"Random State: {RANDOM_STATE}\")\n",
        "except NameError:\n",
        "    print(\"Random State: Not defined yet\")\n",
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
    """Add library version tracking cell to a notebook, replacing old ones if they exist."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Remove any existing version cells I might have added
        new_cells = []
        for cell in nb['cells']:
            source_text = ''.join(cell['source'])
            if 'LIBRARY VERSIONS' in source_text and 'reproducibility' in source_text:
                continue
            new_cells.append(cell)
        
        nb['cells'] = new_cells
        
        # Find the first code cell (usually imports)
        insert_index = 0
        for i, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                insert_index = i + 1
                break
        
        # Insert version cell after first code cell
        nb['cells'].insert(insert_index, version_cell)
        
        # Save modified notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        
        print(f"✅ Updated version cell in {notebook_path}")
    
    except Exception as e:
        print(f"❌ Error processing {notebook_path}: {e}")

if __name__ == "__main__":
    print("Updating library version tracking in notebooks...\n")
    
    for notebook in notebooks:
        if os.path.exists(notebook):
            add_version_cell_to_notebook(notebook)
        else:
            print(f"⚠️  Notebook not found: {notebook}")
    
    print("\n✅ Done! All notebooks updated.")
