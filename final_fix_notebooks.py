"""
Script to fix indentation and NaN handling in clustering notebooks.
Corrects the errors introduced by the previous script.
"""

import json
import os

def final_fix_notebook(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for cell in nb['cells']:
            if cell['cell_type'] == 'code' and 'X_scaled = scaler.fit_transform' in ''.join(cell['source']):
                # Complete replacement to ensure cleanliness
                if 'KMeans' in notebook_path:
                    new_source = [
                        "# Initialize and fit SimpleImputer to handle NaNs\n",
                        "imputer = SimpleImputer(strategy='median')\n",
                        "X_imputed = imputer.fit_transform(X_encoded)\n",
                        "\n",
                        "# Initialize and fit StandardScaler on full X\n",
                        "scaler = StandardScaler()\n",
                        "X_scaled = scaler.fit_transform(X_imputed)\n",
                        "\n",
                        "print(f\"\u2713 Features scaled using StandardScaler\")\n",
                        "print(f\"Scaled data shape: {X_scaled.shape}\")\n",
                        "print(f\"\\nScaled data statistics:\")\n",
                        "print(f\"   Mean: {X_scaled.mean():.6f} (should be ~0)\")\n",
                        "print(f\"   Std:  {X_scaled.std():.6f} (should be ~1)\")\n",
                        "print(f\"   Min:  {X_scaled.min():.4f}\")\n",
                        "print(f\"   Max:  {X_scaled.max():.4f}\")"
                    ]
                else: # DBSCAN
                    new_source = [
                        "# Initialize and fit SimpleImputer to handle NaNs\n",
                        "imputer = SimpleImputer(strategy='median')\n",
                        "X_imputed = imputer.fit_transform(X_encoded)\n",
                        "\n",
                        "# Scale features with StandardScaler\n",
                        "scaler = StandardScaler()\n",
                        "X_scaled = scaler.fit_transform(X_imputed)\n",
                        "\n",
                        "print(f\"\\nScaled feature matrix shape: {X_scaled.shape}\")\n",
                        "print(f\"\u2713 Features scaled using StandardScaler\")"
                    ]
                cell['source'] = new_source

        # Save modified notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        
        print(f"✅ Final fix applied to {notebook_path}")
    
    except Exception as e:
        print(f"❌ Error fixing {notebook_path}: {e}")

if __name__ == "__main__":
    final_fix_notebook("kmeans_clustering_analysis.ipynb")
    final_fix_notebook("dbscan_clustering_analysis.ipynb")
