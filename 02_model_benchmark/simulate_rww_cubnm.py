# ==============================================================================
# cuBNM Reduced Wong-Wang (rWW) Neural Mass GPU Simulation (WSL Execution)
# ==============================================================================

import os
import scipy.io as sio
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from cubnm.sim import rWWSimGroup

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

# Global coupling parameter grid
G_grid = np.linspace(0.5, 3.5, 15)

results = []

# 2. Loop through subjects and run GPU-accelerated cuBNM simulations
for sub in subjects:
    # Load SC
    sc_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_region_connectomes.mat"))["region_connectome"]
    sc = sc_mat[keep_indices, :][:, keep_indices].astype(float)
    sc[sc < 0] = 0.0
    np.fill_diagonal(sc, 0.0)
    
    l_max = np.max(np.real(np.linalg.eigvals(sc)))
    sc_norm = sc / l_max
    
    sg = rWWSimGroup(duration=180, TR=2.0, sc=sc_norm, do_fcd=False, do_fic=True, max_fic_trials=5, gof_terms=['+fc_corr'])
    sg.N = len(G_grid)
    sg.param_lists['G'] = G_grid
    
    for k, v in sg.default_params.items():
        if v is not None and sg.param_lists[k] is None:
            if k in sg.global_param_names:
                sg.param_lists[k] = np.full(sg.N, v, dtype=float)
            elif k in sg.regional_param_names:
                sg.param_lists[k] = np.full((sg.N, sg.nodes), v, dtype=float)
                
    # Run cuBNM simulation group
    sg.run()
    
    # Load individual task FC matrices
    mid_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_MID_taskFC.mat"))
    sst_mat = sio.loadmat(os.path.join(data_dir, f"{sub}_SST_taskFC.mat"))
    
    for cond in conditions:
        fc_indiv = (mid_mat if "MID" in cond else sst_mat)[cond][keep_indices, :][:, keep_indices]
        z_indiv = fc_indiv[triu]
        
        best_r = -1.0
        best_G = G_grid[0]
        
        for idx in range(len(G_grid)):
            fc_sim = sg.get_sim_fc(idx)
            z_pred = np.arctanh(np.clip(fc_sim, -0.9999, 0.9999))[triu]
            
            r_val, _ = pearsonr(z_pred, z_indiv)
            if r_val > best_r:
                best_r = r_val
                best_G = G_grid[idx]
                
        results.append({
            "subject": sub,
            "condition": cond,
            "optimal_G": round(best_G, 4),
            "pearson_r": round(best_r, 4)
        })
        print(f"Subject {sub} | Condition {cond} | Optimal G: {best_G:.2f} | Pearson r: {best_r:.4f}")

# 3. Save subject-level results to CSV
df_res = pd.DataFrame(results)
df_res.to_csv(os.path.join(output_dir, "rww_fitting_summary.csv"), index=False)
print("Finished rWW model GPU simulation! Summary saved to rww_fitting_summary.csv")
