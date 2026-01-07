"""
Corrected script to fix DBSCAN notebook.
Ensures X_encoded is defined before being used.
"""

import json
import os

def fix_dbscan_notebook():
    notebook_path = "dbscan_clustering_analysis.ipynb"
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for cell in nb['cells']:
            if cell['cell_type'] == 'code' and 'X_scaled = scaler.fit_transform' in ''.join(cell['source']):
                new_source = [
                    "# Identify categorical and numerical features\n",
                    "num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()\n",
                    "cat_features = X.select_dtypes(include=['object']).columns.tolist()\n",
                    "\n",
                    "print(f\"Numerical features ({len(num_features)}): {num_features}\")\n",
                    "print(f\"Categorical features ({len(cat_features)}): {cat_features}\")\n",
                    "\n",
                    "# One-hot encode categorical features if they exist\n",
                    "if len(cat_features) > 0:\n",
                    "    X_encoded = pd.get_dummies(X, columns=cat_features, drop_first=False)\n",
                    "    print(f\"\\n✓ Categorical features encoded\")\n",
                    "else:\n",
                    "    X_encoded = X.copy()\n",
                    "    print(f\"\\n✓ No categorical features to encode\")\n",
                    "\n",
                    "# Initialize and fit SimpleImputer to handle NaNs\n",
                    "imputer = SimpleImputer(strategy='median')\n",
                    "X_imputed = imputer.fit_transform(X_encoded)\n",
                    "\n",
                    "# Scale features with StandardScaler\n",
                    "scaler = StandardScaler()\n",
                    "X_scaled = scaler.fit_transform(X_imputed)\n",
                    "\n",
                    "print(f\"\\nScaled feature matrix shape: {X_scaled.shape}\")\n",
                    "print(f\"✓ Features scaled using StandardScaler\")"
                ]
                cell['source'] = new_source
                break

        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        
        print(f"✅ Correctly fixed DBSCAN notebook")
    
    except Exception as e:
        print(f"❌ Error fixing DBSCAN: {e}")

if __name__ == "__main__":
    fix_dbscan_notebook()
