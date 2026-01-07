"""
Script to fix NaN handling in clustering notebooks.
Adds SimpleImputer to handle missing values before scaling.
"""

import json
import os

def fix_nan_handling(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # We need to find the cell where scaling happens and insert an imputer before it.
        # However, for simplicity and robustness, let's update the import cell and the scaling cell.
        
        # 1. Update imports
        for cell in nb['cells']:
            if cell['cell_type'] == 'code' and 'StandardScaler' in ''.join(cell['source']):
                source = cell['source']
                if 'SimpleImputer' not in ''.join(source):
                    # Add SimpleImputer to imports
                    for i, line in enumerate(source):
                        if 'from sklearn.preprocessing import StandardScaler' in line:
                            source.insert(i, 'from sklearn.impute import SimpleImputer\n')
                            break
                    cell['source'] = source
        
        # 2. Update scaling/preprocessing cell
        # For simplicity, I'll look for where X_scaled = scaler.fit_transform(X_encoded) happens
        for cell in nb['cells']:
            if cell['cell_type'] == 'code' and 'X_scaled = scaler.fit_transform' in ''.join(cell['source']):
                source = cell['source']
                if 'imputer' not in ''.join(source):
                    new_source = []
                    found = False
                    for line in source:
                        if 'scaler = StandardScaler()' in line:
                            new_source.append('    # Initialize and fit SimpleImputer to handle NaNs\n')
                            new_source.append('    imputer = SimpleImputer(strategy=\'median\')\n')
                            new_source.append('    X_imputed = imputer.fit_transform(X_encoded)\n\n')
                            new_source.append('    ' + line)
                            found = True
                        elif 'X_scaled = scaler.fit_transform(X_encoded)' in line:
                            new_source.append(line.replace('X_encoded', 'X_imputed'))
                        elif 'X_scaled = scaler.fit_transform(X_scaled)' in line: # Fallback
                             new_source.append(line.replace('X_scaled)','X_imputed)'))
                        else:
                            new_source.append(line)
                    
                    if found:
                        cell['source'] = new_source
                    else:
                        # Sometimes it's not indented
                        new_source = []
                        for line in source:
                            if 'scaler = StandardScaler()' in line:
                                new_source.append('# Initialize and fit SimpleImputer to handle NaNs\n')
                                new_source.append('imputer = SimpleImputer(strategy=\'median\')\n')
                                new_source.append('X_imputed = imputer.fit_transform(X_encoded)\n\n')
                                new_source.append(line)
                                found = True
                            elif 'X_scaled = scaler.fit_transform(X_encoded)' in line:
                                new_source.append(line.replace('X_encoded', 'X_imputed'))
                            else:
                                new_source.append(line)
                        if found:
                            cell['source'] = new_source

        # Save modified notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=4)
        
        print(f"✅ Fixed NaN handling in {notebook_path}")
    
    except Exception as e:
        print(f"❌ Error fixing {notebook_path}: {e}")

if __name__ == "__main__":
    fix_nan_handling("kmeans_clustering_analysis.ipynb")
    fix_nan_handling("dbscan_clustering_analysis.ipynb")
