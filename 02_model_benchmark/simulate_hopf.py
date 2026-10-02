# ==============================================================================
# Hopf Bifurcation Analytical Model Simulation for SC-FC Coupling
# ==============================================================================

import os
import scipy.io as sio
import numpy as np
import pandas as pd
import scipy.linalg as la
from scipy.stats import pearsonr

# 1. Path configuration and subject list
data_dir = r"F:\CBP\data\sc_fc_coupling"
output_dir = r"C:\Users\qianliyi\OneDrive\Docs\Research documents\NM2026\scripts"

subjects = [63218063, 44576096, 112288, 16275727, 67342911, 67844279,
            113174215, 111086310, 168370463, 182136619, 191996808, 112517217]

conditions = ["SST_stop_success", "SST_stop_failure", "MID_feed_hit", "MID_antici_hit"]

# Load 217 cortex/subcortex region indices
atlas = sio.loadmat(os.path.join(data_dir, "edge_index", "atlas_region.mat"))
keep_indices = (atlas["uni_region"][0] - 1).astype(int)
triu = np.triu_indices(217, k=1)

results = []

# 2. Loop through subjects and task conditions
for sub in subjects:
    # Load SC and build Graph Laplacian L = D - W
    sc_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_region_connectomes.mat"))["region_connectome"]
    sc = sc_mat[keep_indices, :][:, keep_indices].astype(float)
    sc[sc < 0] = 0.0
    np.fill_diagonal(sc, 0.0)
    
    l_max = np.max(np.real(np.linalg.eigvals(sc)))
    w = sc / l_max
    laplacian = np.diag(w.sum(axis=1)) - w
    
    # Load individual task FC matrices
    mid_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_MID_taskFC.mat"))
    sst_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_SST_taskFC.mat"))
    
    for cond in conditions:
        fc_indiv = (mid_mat if "MID" in cond else sst_mat)[cond][keep_indices, :][:, keep_indices]
        z_indiv = fc_indiv[triu]
        
        # Grid search global coupling parameter gamma
        best_r = -1.0
        best_gamma = 0.001
        
        for gamma in np.linspace(0.001, 50.0, 100):
            # Analytical Hopf covariance: inv(I + gamma * L)
            cov = la.inv(np.eye(217) + gamma * laplacian)
            
            # Standardize covariance to correlation matrix and transform to Fisher z-space
            std = np.sqrt(np.diag(cov))
            fc_pred_r = np.clip(cov / np.outer(std, std), 0.0, 0.9999)
            z_pred = np.arctanh(fc_pred_r)[triu]
            
            r_val, _ = pearsonr(z_pred, z_indiv)
            if r_val > best_r:
                best_r = r_val
                best_gamma = gamma
                
        results.append({
            "subject": sub,
            "condition": cond,
            "optimal_gamma": round(best_gamma, 4),
            "pearson_r": round(best_r, 4)
        })
        print(f"Subject {sub} | Condition {cond} | Optimal gamma: {best_gamma:.3f} | Pearson r: {best_r:.4f}")

# 3. Save subject-level results to CSV
df_res = pd.DataFrame(results)
df_res.to_csv(os.path.join(output_dir, "hopf_fitting_summary.csv"), index=False)
print("Finished Hopf model simulation! Summary saved to hopf_fitting_summary.csv")
