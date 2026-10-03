"""NP-DTB manuscript colour tokens (Woo-lab derived). See np_dtb_palette.csv."""

PALETTE = {
    'exc_ampa': '#FB6A4A',  # Virtual AMPA up-regulation
    'exc_ketamine': '#A50F15',  # Ketamine session
    'exc_restore': '#FCAE91',  # AMPA restoration index
    'exc_similarity': '#FDD9C8',  # AMPA-state similarity
    'inh_gaba': '#47C0E1',  # Virtual GABA-A up-regulation
    'inh_midazolam': '#1A7A96',  # Midazolam session
    'inh_restore': '#A9DEEE',  # GABA-A restoration index
    'unp_baseline': '#757575',  # Simulated baseline (unperturbed)
    'unp_placebo': '#C5D0D2',  # Placebo / saline session
    'unp_null': '#F4F4F4',  # Shuffled-parameter / chance null
    'circ_neg29': '#FAC66D',  # Negative NP profile (29 edges)
    'circ_np12': '#C99A46',  # NP factor (12 edges)
    'circ_mid6': '#9A6F20',  # MID-only NP formulation (6 edges)
    'circ_nonnp': '#E3DAC1',  # Non-NP / rest of brain
    'pos_prof34': '#819D98',  # Positive NP profile (34 edges)
    'alt_mdd_net': '#A58B77',  # Depression-specific CPM network
    'alt_wholebrain': '#DDBFAA',  # Whole-brain parcellated connectome
    'hlth_hc': '#99B77C',  # Healthy controls
    'hlth_norm': '#C9E7AB',  # Control reference band / normalisation arrow
    'clin_highsymp': '#E9D5FF',  # High-symptom (IMAGEN)
    'clin_aud': '#CAADEF',  # AUD
    'clin_patients': '#A98DCD',  # Patients (pooled)
    'clin_mdd': '#8A6BB1',  # MDD
    'bench_sar': '#B7AA82',  # SAR benchmark model
    'bench_rww': '#5F5434',  # reduced Wong-Wang benchmark
    'scale_3m': '#E2E2E2',  # 3 M neurons (regional)
    'scale_10m': '#B8B8B8',  # 10 M neurons
    'scale_100m': '#8C8C8C',  # 100 M neurons
    'scale_1b': '#585858',  # 1 B neurons
    'scale_5b': '#262626',  # 5 B neurons
    'coh_imagen': '#475666',  # IMAGEN (discovery, n=1,050)
    'coh_imagen_fu3': '#7F98AD',  # IMAGEN follow-up (n=85)
    'coh_stratify': '#5981A1',  # STRATIFY / ESTRA (n=427)
    'coh_pharm_hv': '#A2BACD',  # Healthy-volunteer pharma (n=27)
    'coh_pharm_clin': '#D5EEFE',  # Clinical ketamine cohort (n=41)
    'task_mid': '#856A4F',  # Monetary Incentive Delay (MID)
    'task_sst': '#637B89',  # Stop-Signal Task (SST)
    'task_eft': '#96B59D',  # Emotional Face Task (EFT)
    'sym_int': '#80435E',  # Internalising symptoms
    'sym_ext': '#B67F49',  # Externalising symptoms
}

FAMILY = {
    'Excitatory (glutamatergic)': ['exc_ampa', 'exc_ketamine', 'exc_restore', 'exc_similarity'],
    'Inhibitory (GABAergic)': ['inh_gaba', 'inh_midazolam', 'inh_restore'],
    'Unperturbed': ['unp_baseline', 'unp_placebo', 'unp_null'],
    'NP circuit (lower FC = more symptoms)': ['circ_neg29', 'circ_np12', 'circ_mid6', 'circ_nonnp'],
    'Positive profile (higher FC = more symptoms)': ['pos_prof34'],
    'Secondary circuits': ['alt_mdd_net', 'alt_wholebrain'],
    'Health / group severity': ['hlth_hc', 'hlth_norm', 'clin_highsymp', 'clin_aud', 'clin_patients', 'clin_mdd'],
    'Benchmark models': ['bench_sar', 'bench_rww'],
    'Model resolution (ordinal)': ['scale_3m', 'scale_10m', 'scale_100m', 'scale_1b', 'scale_5b'],
    'Cohorts': ['coh_imagen', 'coh_imagen_fu3', 'coh_stratify', 'coh_pharm_hv', 'coh_pharm_clin'],
    'Task context': ['task_mid', 'task_sst', 'task_eft'],
    'Symptom domains (reserve)': ['sym_int', 'sym_ext'],
}

SCALE_RAMP = ['#E2E2E2', '#B8B8B8', '#8C8C8C', '#585858', '#262626']
NP_NESTING = ['#FAC66D', '#C99A46', '#9A6F20']
SEVERITY   = ['#E9D5FF', '#CAADEF', '#A98DCD', '#8A6BB1']

HOT  = ['#FFF2CC', '#FFCC00', '#FF6600', '#FF0000', '#A50F15']   # brain overlay, positive statistic
COLD = ['#E3F5FB', '#55A8FF', '#47C0E1', '#209ABA', '#0B5E8C']   # brain overlay, negative statistic
FC_DIVERGING = ['#2F4F4A', '#819D98', '#D5E0DC', '#F4F2EE', '#FAE3B0', '#C99A46', '#6E4A00']   # signed FC / dFC, centre at 0

def cmap(name):
    """name in {"hot","cold","fc"} -> LinearSegmentedColormap"""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list(name, {"hot":HOT,"cold":COLD,"fc":FC_DIVERGING}[name])

MARKER = {"MID": "o", "SST": "s", "EFT": "^"}
PROVENANCE = {"simulated": dict(), "empirical": dict(markerfacecolor="white", fillstyle="none")}
RESPONSE = {"increase": "^", "decrease": "v"}  # filled vs open
