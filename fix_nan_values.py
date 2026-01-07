"""
Fix NaN Values in DBSCAN Analysis

This script provides code to check for and handle NaN values in your data.
Copy and paste the relevant sections into your notebook before the K-distance calculation.
"""

# ============================================================================
# STEP 1: Check for missing values in original data
# ============================================================================
# Add this cell AFTER loading and encoding your data, BEFORE scaling

print("=" * 80)
print("CHECKING FOR MISSING VALUES IN ORIGINAL DATA")
print("=" * 80)

# Check original dataframe
print(f"\nDataset shape: {df.shape}")
print(f"\nMissing values per column:")
missing_counts = df.isnull().sum()
if missing_counts.sum() > 0:
    print(missing_counts[missing_counts > 0])
    print(f"\nTotal missing values: {missing_counts.sum()}")
    print(f"Percentage: {(missing_counts.sum() / (df.shape[0] * df.shape[1])) * 100:.2f}%")
else:
    print("✓ No missing values found in original data.")

# Check features (X)
print(f"\n\nFeatures (X) shape: {X.shape}")
print(f"Missing values in X:")
x_missing = X.isnull().sum()
if x_missing.sum() > 0:
    print(x_missing[x_missing > 0])
else:
    print("✓ No missing values in X")

# Check encoded features
print(f"\n\nEncoded features shape: {X_encoded.shape}")
print(f"Missing values in X_encoded:")
x_enc_missing = X_encoded.isnull().sum()
if x_enc_missing.sum() > 0:
    print(x_enc_missing[x_enc_missing > 0])
else:
    print("✓ No missing values in X_encoded")


# ============================================================================
# STEP 2: Handle missing values BEFORE scaling (RECOMMENDED)
# ============================================================================
# Add this cell BEFORE the StandardScaler step

from sklearn.impute import SimpleImputer

print("\n" + "=" * 80)
print("HANDLING MISSING VALUES")
print("=" * 80)

# Check if there are any missing values
if X_encoded.isnull().sum().sum() > 0:
    print("\n⚠️  Found missing values. Applying imputation...")
    
    # Option 1: Fill with median (recommended for numerical data)
    imputer = SimpleImputer(strategy='median')
    X_imputed = pd.DataFrame(
        imputer.fit_transform(X_encoded),
        columns=X_encoded.columns,
        index=X_encoded.index
    )
    
    print(f"✓ Missing values imputed using median strategy")
    print(f"Remaining missing values: {X_imputed.isnull().sum().sum()}")
    
    # Use imputed data for scaling
    X_to_scale = X_imputed
else:
    print("✓ No missing values to handle")
    X_to_scale = X_encoded

# Now scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_to_scale)

print(f"\n✓ Features scaled using StandardScaler")
print(f"Scaled feature matrix shape: {X_scaled.shape}")


# ============================================================================
# STEP 3: Check and fix NaN/Inf in scaled data (FALLBACK)
# ============================================================================
# Add this cell AFTER scaling, BEFORE K-distance calculation

print("\n" + "=" * 80)
print("VALIDATING SCALED DATA")
print("=" * 80)

# Check for NaN and Inf values
nan_count = np.isnan(X_scaled).sum()
inf_count = np.isinf(X_scaled).sum()

print(f"\nNaN values in X_scaled: {nan_count}")
print(f"Inf values in X_scaled: {inf_count}")

if nan_count > 0 or inf_count > 0:
    print("\n⚠️  WARNING: Found NaN or Inf values in scaled data!")
    
    # Check which columns have issues
    nan_cols = np.where(np.isnan(X_scaled).any(axis=0))[0]
    inf_cols = np.where(np.isinf(X_scaled).any(axis=0))[0]
    
    if len(nan_cols) > 0:
        print(f"\nColumns with NaN: {nan_cols}")
    if len(inf_cols) > 0:
        print(f"Columns with Inf: {inf_cols}")
    
    print("\nApplying fixes...")
    
    # Replace NaN and Inf with 0 (mean of standardized data)
    X_scaled = np.nan_to_num(X_scaled, nan=0.0, posinf=0.0, neginf=0.0)
    
    print("✓ NaN and Inf values replaced with 0 (mean of standardized features)")
    
    # Verify fix
    print(f"\nVerifying fix...")
    print(f"   NaN values remaining: {np.isnan(X_scaled).sum()}")
    print(f"   Inf values remaining: {np.isinf(X_scaled).sum()}")
else:
    print("\n✓ No NaN or Inf values detected. Data is clean!")

# Print statistics
print(f"\nFinal X_scaled statistics:")
print(f"   Shape: {X_scaled.shape}")
print(f"   Min:   {X_scaled.min():.4f}")
print(f"   Max:   {X_scaled.max():.4f}")
print(f"   Mean:  {X_scaled.mean():.4f}")
print(f"   Std:   {X_scaled.std():.4f}")

print("\n" + "=" * 80)
print("✅ DATA VALIDATION COMPLETE - Ready for K-distance calculation!")
print("=" * 80)
