"""Figure 3 | Model scale determines which inference a digital twin supports.

ONE FILE PER PANEL -> ./panels/ as .png (400 dpi), .pdf (vector) and .pptx
(editable text), each at its intended printed size.

  a  simulation error (MSE) of 12 individual twins across six model builds
  b  cross-scale similarity of the simulated baseline 12-edge NP profile
  c  run-to-run variability of each model build
  d  AMPA conductance sweep, 4 subjects   -- ORIGINAL panel, unchanged
  e  GABA-A conductance sweep, 4 subjects -- ORIGINAL panel, unchanged
  f  per-subject Delta NP after AMPA and GABA-A perturbation, across scales

Colours are the manuscript's own (../fig_color/np_dtb_style.py, USER_PALETTE):
AMPA #E1D09A, GABA-A #96B9AD, NP circuit #0072B2, reference grey #7F7F7F.
The fidelity panels (a-d) add one new hue in two tones for model family --
regional #8E7CC3, voxel #4C3F8C, ramp #6E5CA8 -- while the non-DTB benchmarks
stay in the reference grey.

    cd revision/text/figures/fig.3 && python fig3.py
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import (apply_np_style, panel, C, LW, TICK_PT, ANNOT_PT,
                          LABEL_PT, panel_title, enforce)
from fig_export import fig_to_pptx

D = os.path.join(HERE, 'fig3_data')
OPD = os.path.join(D, 'original_panels')
OUTD = os.path.join(HERE, 'panels')
os.makedirs(OUTD, exist_ok=True)
DPI = 400
apply_np_style()

a3 = pd.read_csv(f'{D}/fig3a_mse_per_subject.csv')
b3 = pd.read_csv(f'{D}/fig3c_cross_scale_similarity.csv', index_col=0)
wb = pd.read_csv(f'{D}/fig3b_wholebrain_fc_crossscale.csv')
d3 = pd.read_csv(f'{D}/fig3e_ampa_sweep.csv')
e3 = pd.read_csv(f'{D}/fig3f_gaba_sweep.csv')
f6 = pd.read_csv(f'{D}/fig3g_delta_np_six_models.csv')
c3 = pd.read_csv(f'{D}/fig3d_run_to_run_sd.csv')

MODELS = ['3m_268', '10m_268', '10m_1000', '10m', '100m', '1b']
BENCH = ['SAR', 'RWW']                     # non-DTB comparator models
MLAB = {'3m_268': '3 M\n268', '10m_268': '10 M\n268', '10m_1000': '10 M\n1000',
        '10m': '10 M\nvoxel', '100m': '100 M\nvoxel', '1b': '1 B\nvoxel',
        'SAR': 'SAR', 'RWW': 'rWW'}
SCALE_LAB = {k: MLAB[k] for k in MLAB}

# Seven DTB builds on three axes: simulated neuron count, the neuron count of
# the assimilated hyper-parameter set, and spatial resolution.  The two 10 M
# voxel builds differ ONLY in the hyper-parameters, so every panel that shows
# them carries the hyper-parameter row underneath the ticks.
BUILDS7 = ['3m_268', '10m_268', '10m_1000', '10m_own', '10m', '100m', '1b']
BLAB = {'3m_268': '3 M\n268', '10m_268': '10 M\n268', '10m_1000': '10 M\n1000',
        '10m_own': '10 M\nvoxel', '10m': '10 M\nvoxel', '100m': '100 M\nvoxel',
        '1b': '1 B\nvoxel', 'SAR': 'SAR', 'RWW': 'rWW'}
BHYP = {'3m_268': '3 M', '10m_268': '3 M', '10m_1000': '10 M\n1000',
        '10m_own': '10 M\nvoxel', '10m': '100 M', '100m': '100 M', '1b': '100 M',
        'SAR': '', 'RWW': ''}
BFAM = {**{k: 'regional' for k in ('3m_268', '10m_268', '10m_1000')},
        **{k: 'voxel' for k in ('10m_own', '10m', '100m', '1b')},
        'SAR': 'benchmark', 'RWW': 'benchmark'}
WBKEY = {'10m': '10m_voxel', '100m': '100m_voxel', '1b': '1b_voxel'}


def hyper_row(ax, keys, y=-.255):
    """Second tick row naming the assimilated hyper-parameter set."""
    tr = ax.get_xaxis_transform()
    ax.text(-.62, y, 'assimilated\nhyper-parameters', transform=tr, ha='right',
            va='top', fontsize=ANNOT_PT, color='0.35', clip_on=False)
    for i, k in enumerate(keys):
        if BHYP[k]:
            ax.text(i, y, BHYP[k], transform=tr, ha='center', va='top',
                    fontsize=ANNOT_PT, color='0.35', clip_on=False)


def block_bands(ax, keys, y, n_bench=0):
    """Vertical separators and the three block captions."""
    n_reg = sum(1 for k in keys if BFAM[k] == 'regional')
    n_dtb = sum(1 for k in keys if BFAM[k] != 'benchmark')
    ax.axvline(n_reg - .5, color='0.85', lw=LW, zorder=0)
    if n_bench:
        ax.axvline(n_dtb - .5, color='0.85', lw=LW, zorder=0)
    ax.text((n_reg - 1) / 2, y, 'regional models', ha='center', fontsize=ANNOT_PT,
            color=FAM['regional'])
    ax.text((n_reg + n_dtb - 1) / 2, y, 'voxel models', ha='center',
            fontsize=ANNOT_PT, color=FAM['voxel'])
    if n_bench:
        ax.text(n_dtb + (n_bench - 1) / 2, y, 'benchmarks', ha='center',
                fontsize=ANNOT_PT, color='0.35')
    return n_reg, n_dtb

DRUG = {'ampa': C('ampa'), 'gaba': C('gaba')}
# model family carries its own colour in the fidelity panels (a-d): one new hue
# (violet, unused elsewhere in the manuscript), two tones for the one ordered
# thing these panels vary -- spatial resolution.  Non-DTB comparators keep the
# reference grey, so grey still means "reference / not our model".
FAM = {'regional': C('model_regional'), 'voxel': C('model_voxel'),
       'benchmark': C('hc')}
FID = C('hc')          # neutral grey, still used for benchmark elements
SUBJ_MK = {'HC01': 'o', 'MDD': 's', 'AUD': '^'}
SUBJ_LS = {'HC01': (0, (2.6, 1.7)), 'MDD': '-', 'AUD': '-'}
SUBJ_OPEN = {'HC01': True, 'MDD': False, 'AUD': False}   # open = healthy control
DRUG_LAB = {'ampa': 'AMPA', 'gaba': 'GABA-A'}
manifest = []


def save(fig, stem, w_mm, h_mm, note):
    fig.savefig(f'{OUTD}/{stem}.png', dpi=DPI, bbox_inches='tight')
    fig.savefig(f'{OUTD}/{stem}.pdf', bbox_inches='tight')
    fig_to_pptx(fig, f'{OUTD}/{stem}.pptx', dpi=DPI)
    px = Image.open(f'{OUTD}/{stem}.png').size
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=h_mm,
                         png_px=f'{px[0]}x{px[1]}', dpi=round(px[0] / (w_mm / 25.4)),
                         source=note))
    plt.close(fig)


def export_original(src, stem, w_mm, note):
    im = Image.open(os.path.join(OPD, src))
    h_mm = w_mm * im.height / im.width
    im.save(f'{OUTD}/{stem}.png', dpi=(im.width / (w_mm / 25.4),) * 2)
    manifest.append(dict(panel=stem, printed_w_mm=w_mm, printed_h_mm=round(h_mm, 1),
                         png_px=f'{im.width}x{im.height}',
                         dpi=round(im.width / (w_mm / 25.4)), source=note))


def box_strip(ax, groups, values, colour, width=.52, jitter=.13, seed=0):
    """Box (white, black outline) with the per-subject points on top."""
    rng = np.random.default_rng(seed)
    bp = ax.boxplot(values, positions=np.arange(len(groups)), widths=width,
                    showfliers=False, patch_artist=True)
    for el in ('boxes', 'whiskers', 'caps', 'medians'):
        for art in bp[el]:
            art.set_linewidth(LW); art.set_color('black')
            if el == 'boxes':
                art.set_facecolor('white'); art.set_edgecolor('black')
    cols = colour if isinstance(colour, (list, tuple)) else [colour] * len(values)
    for i, v in enumerate(values):
        ax.scatter(i + rng.uniform(-jitter, jitter, len(v)), v, s=4.5,
                   facecolor=cols[i], edgecolor='none', alpha=.8, zorder=3)


# ------------------------------------------------- a  simulation error by build
# All seven DTB builds are scored against the SAME empirical reference,
# empirical_model_voxels (= emp_edge1-12 in simulation_results_wide_12subs.csv
# = real_fc_dtb_voxels), i.e. empirical FC recomputed from only the voxels the
# DTB simulates.  3 M/268 is the new run; the superseded 3 M run is not shown.
# The two benchmarks are DELIBERATELY left on their own empirical reference,
# the Shen-268 regional task FC they were fitted and scored against
# (<subj>_{MID,SST}_taskFC.mat + np_location.mat in sc-fc_prediction_model/).
# Re-scoring them against empirical_model_voxels is possible (SAR 0.0528,
# rWW 0.0824; see fig3a_benchmark_reference_check.csv) but would evaluate them
# on a target their coupling parameter was never optimised for, so the native
# reference is used.  The `empirical_reference` column records which is which.
AMOD = BUILDS7 + BENCH
W, H = 126, 56
fig, ax = plt.subplots(figsize=panel(W, H))
vals = [a3.loc[a3.model == m, 'mse'].values for m in AMOD]
box_strip(ax, AMOD, vals, [FAM[BFAM[m]] for m in AMOD])
top = max(a3.mse) * 1.30
ax.set_xticks(range(len(AMOD)))
ax.set_xticklabels([BLAB[m] for m in AMOD], fontsize=TICK_PT)
for t, m in zip(ax.get_xticklabels(), AMOD):
    t.set_color(FAM[BFAM[m]] if BFAM[m] != 'benchmark' else '0.35')
hyper_row(ax, AMOD)
ax.set_ylabel('Simulation error (MSE)')
ax.set_ylim(0, top)
block_bands(ax, AMOD, top * .90, n_bench=len(BENCH))
panel_title(ax, 'Simulation error against the model-voxel empirical reference '
                '(n = 12)')
enforce(fig); save(fig, 'fig3a', W, H, 'fig3a_mse_per_subject.csv')

# ------ b  cross-scale whole-brain FC fidelity (Suppl. Table S9, summary only)
# The supplementary table reports mean +/- s.d. across the 12 subjects, not
# per-subject values, so this panel shows exactly that and nothing more.
W, H = 126, 56
fig, ax = plt.subplots(figsize=panel(W, H))
COND = ['SST Stop Success', 'SST Stop Failure', 'MID Reward Antici.', 'MID Pos. Feedback']
CMK = {'SST Stop Success': 'o', 'SST Stop Failure': 's',
       'MID Reward Antici.': '^', 'MID Pos. Feedback': 'D'}
WBM = [WBKEY.get(m, m) for m in BUILDS7] + BENCH
WKEY = BUILDS7 + BENCH
xw = np.arange(len(WBM))
dx = np.linspace(-.20, .20, len(COND))
wfam = [BFAM[k] for k in WKEY]
for k, cond in enumerate(COND):
    sub = wb[wb.condition == cond].set_index('model').loc[WBM]
    for i, m in enumerate(WBM):          # colour by family, shape by condition
        col = FAM[wfam[i]]
        ax.errorbar(xw[i] + dx[k], sub.r_mean.iloc[i], yerr=sub.r_sd.iloc[i],
                    fmt=CMK[cond], color=col, markersize=2.6, lw=0,
                    elinewidth=LW, capsize=1.6, capthick=LW,
                    markerfacecolor='white', markeredgecolor=col,
                    markeredgewidth=LW, zorder=3)
n_reg_wb = 3
ax.set_xticks(xw)
ax.set_xticklabels([BLAB[k] for k in WKEY], fontsize=TICK_PT)
for t, f in zip(ax.get_xticklabels(), wfam):
    t.set_color(FAM[f] if f != 'benchmark' else '0.35')
hyper_row(ax, WKEY, y=-.30)
ax.set_ylabel("Whole-brain FC similarity (r)")
ax.set_ylim(0, .82)
block_bands(ax, WKEY, .78, n_bench=len(BENCH))
panel_title(ax, 'Whole-brain FC similarity: DTB builds vs benchmarks (mean ± s.d., n = 12)')
enforce(fig); save(fig, 'fig3b', W, H, 'fig3b_wholebrain_fc_crossscale.csv')

# --- b legend, exported on its own so it can be placed freely in the layout
figL, axL = plt.subplots(figsize=panel(76, 30))
axL.axis('off')
# legend handles are real errorbar containers, so each key shows the marker
# WITH its vertical error bar (as in the panel itself)
hL = [axL.errorbar([], [], yerr=[], fmt=CMK[c], color='black', markersize=2.6, lw=0,
                   elinewidth=LW, capsize=1.6, capthick=LW,
                   markerfacecolor='white', markeredgecolor='black',
                   markeredgewidth=LW) for c in COND]
# marker shape = task condition (black here, because in the panel the colour
# channel is spent on model family); the two family keys are shown as swatches
hF = [Line2D([], [], marker='s', linestyle='none', markersize=3.0,
             markerfacecolor=FAM[f], markeredgecolor=FAM[f])
      for f in ('regional', 'voxel', 'benchmark')]
axL.legend(hL + hF, COND + ['regional models', 'voxel models', 'benchmarks'],
           loc='center', ncol=2, fontsize=ANNOT_PT, handletextpad=.5,
           labelspacing=.5, columnspacing=1.2, borderpad=0, frameon=False)
enforce(figL); save(figL, 'fig3b_legend', 76, 30, 'legend for fig3b')

# --------------------------- c  cross-build similarity of the baseline NP profile
# Metric: a single SPEARMAN correlation over all 12 subjects x 12 edges = 144
# cells of the raw baseline NP values (no per-subject averaging, no Fisher-z,
# no standardisation).  Rank-based rather than Pearson because the builds have
# very different tail behaviour: the new 10 M voxel build has excess kurtosis
# 10.6 (one cell at z = +6.5), and its Pearson agreement with the 10 M/100 M
# build collapses from 0.21 to -0.04 when the five most extreme of the 144
# cells are dropped, whereas Spearman moves only 0.07 -> -0.02.  The two
# metrics rank the 21 off-diagonal pairs almost identically (rho = 0.96, max
# shift 0.14), so this choice does not manufacture the block structure; the
# Pearson matrix is kept alongside in
# fig3c_cross_scale_similarity_pearson.csv.  Repeat-averaged profiles are used wherever repeats
# exist (new 3 M, 10 M/268 and the archive voxel builds: 5 repeats each; the
# new 10 M voxel own-parameter build is a single run).
# Build identity: 10 M/1000 is the historical `10m_reg` scale in the newflow
# table (10 M originally had only the 1000-region regional version); 10 M/268
# is the later `regional` model in NP_12edges_10m_1000_10m_268_regional_modu.csv
# (where `coarse` denotes 1000 and `reg` denotes 268).
CLAB = {'3m_268': '3 M | 268', '10m_268': '10 M | 268', '10m_1000': '10 M | 1000',
        '10m_own': '10 M | voxel', '10m': '10 M | voxel', '100m': '100 M | voxel',
        '1b': '1 B | voxel'}
CHYP = {'3m_268': '3 M', '10m_268': '3 M', '10m_1000': '10 M/1000',
        '10m_own': '10 M vox', '10m': '100 M', '100m': '100 M', '1b': '100 M'}


def heat(mat, name, title, src):
    """Cross-build similarity heat map; identical rendering for every state."""
    W, H = 70, 62
    fig, ax = plt.subplots(figsize=panel(W, H))
    cmap = LinearSegmentedColormap.from_list('fidelity', ['#FFFFFF', C('model_mid')])
    cmap.set_bad('0.92')
    M = mat.values.astype(float)
    im = ax.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=0, vmax=1)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if np.isfinite(M[i, j]):
                ax.text(j, i, f'{M[i, j]:.2f}', ha='center', va='center',
                        fontsize=TICK_PT, color='white' if M[i, j] > .62 else 'black')
    labs = [f'{CLAB[m]}\nhyper {CHYP[m]}' for m in mat.columns]
    n_b = len(mat)
    ax.set_xticks(range(n_b)); ax.set_yticks(range(n_b))
    ax.set_xticklabels(labs, fontsize=TICK_PT, rotation=90)
    ax.set_yticklabels(labs, fontsize=TICK_PT)
    cfam = [BFAM[m] for m in mat.columns]
    for t, f in zip(ax.get_xticklabels(), cfam):
        t.set_color(FAM[f])
    for t, f in zip(ax.get_yticklabels(), cfam):
        t.set_color(FAM[f])
    ax.set_xticks(np.arange(-.5, n_b, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n_b, 1), minor=True)
    ax.grid(which='minor', color='0.40', linewidth=LW)
    for sp_ in ax.spines.values():
        sp_.set_visible(True); sp_.set_linewidth(LW); sp_.set_color('0.40')
    cb = fig.colorbar(im, ax=ax, fraction=.046, pad=.04, ticks=[0, .5, 1])
    cb.set_label("Spearman $\\rho$ (144 subject x edge cells)",
                 fontsize=ANNOT_PT, labelpad=1)
    cb.ax.tick_params(labelsize=TICK_PT, width=LW, length=1.6)
    cb.outline.set_linewidth(LW)
    panel_title(ax, title)
    enforce(fig)
    ax.tick_params(length=0, which='both')
    save(fig, name, W, H, src)


heat(b3, 'fig3c',
     'Builds agree with those sharing their hyper-parameters, not their scale',
     'fig3c_cross_scale_similarity.csv')
# The same metric applied to the PERTURBED states.  Negative entries are clipped
# to white by the shared 0-1 colour scale; the signed values are in the tables.
# All entries now use the full 144 cells; the counts are kept in
# fig3c_cross_scale_n_cells_*.csv as a check.
heat(pd.read_csv(f'{D}/fig3c_cross_scale_similarity_ampa.csv', index_col=0), 'fig3c_ampa',
     'After AMPA the hyper-parameter blocks loosen, most of all among the voxel builds',
     'fig3c_cross_scale_similarity_ampa.csv')
heat(pd.read_csv(f'{D}/fig3c_cross_scale_similarity_gaba.csv', index_col=0), 'fig3c_gaba',
     'After GABA-A the two 268-region builds become nearly interchangeable',
     'fig3c_cross_scale_similarity_gaba.csv')

# ------------------------------------------------- d  run-to-run variability
# s.d. of the summed NP factor across the five independent simulation repeats,
# averaged over the 12 twins.  The new 10 M voxel build (own hyper-parameters)
# was run once, so it has no repeat variability to show.
# It is therefore dropped from this panel entirely rather than shown as an
# empty slot: the panel compares run-to-run variability, and a build with one
# run has no value on that axis.
BUILDS_REP = [m for m in BUILDS7 if m != '10m_own']
W, H = 84, 54
fig, ax = plt.subplots(figsize=panel(W, H))
c3 = c3.set_index('model').loc[BUILDS_REP].reset_index()
x = np.arange(len(c3))
dcol = [FAM[BFAM[m]] for m in c3.model]
ax.bar(x, c3.run_sd_mean.fillna(0), width=.58,
       facecolor=[(*plt.matplotlib.colors.to_rgb(c), .35) for c in dcol],
       edgecolor=dcol, linewidth=LW, zorder=2)
for xi, m, sd, col in zip(x, c3.run_sd_mean, c3.run_sd_sd, dcol):
    if np.isfinite(m):
        ax.errorbar(xi, m, yerr=sd, fmt='none', ecolor=col, elinewidth=LW,
                    capsize=1.8, capthick=LW, zorder=3)
top = float((c3.run_sd_mean + c3.run_sd_sd).max()) * 1.22
ax.set_xticks(x); ax.set_xticklabels([BLAB[m] for m in c3.model], fontsize=TICK_PT)
for t, m in zip(ax.get_xticklabels(), c3.model):
    t.set_color(FAM[BFAM[m]])
hyper_row(ax, list(c3.model), y=-.28)
ax.set_ylabel('Run-to-run s.d. of summed NP')
ax.set_ylim(0, top)
block_bands(ax, list(c3.model), top * .93)
panel_title(ax, 'Run-to-run variability is lowest in the 1 B build')
enforce(fig); save(fig, 'fig3d', W, H, 'fig3d_run_to_run_sd.csv')

# ------------------- d, e  conductance sweeps, HC02 removed at author's request
# Same form as the original panels; subject colour now follows the group palette
# (grey = healthy control, orange = patient), the two patients separated by
# marker and line style rather than by a new hue.
# shared y range for the two sweeps, widened to whole units (matches the
# -2..2 range of the author's original panels)
ylo = np.floor(min(d3[d3.columns[1:]].values.min(), e3[e3.columns[1:]].values.min()))
yhi = np.ceil(max(d3[d3.columns[1:]].values.max(), e3[e3.columns[1:]].values.max()))
ylo, yhi = min(ylo, -2.0), max(yhi, 2.0)
ypad = 0.0
for stem, df_, xlab, ttl, wmm, dkey in [
        ('fig3e', d3, 'AMPA conductance',
         'AMPA up-regulation raises NP in both patients, lowers it in HC01', 62, 'ampa'),
        ('fig3f', e3, 'GABA-A conductance',
         'GABA-A up-regulation shifts NP less, and only in AUD', 62, 'gaba')]:
    levels = list(df_.columns[1:])
    xs = np.arange(len(levels))
    fig, ax = plt.subplots(figsize=panel(wmm, 46))
    for _, row in df_.iterrows():
        sname = row['subject']
        ax.plot(xs, row[levels].astype(float).values, color=DRUG[dkey],
                marker=SUBJ_MK[sname], markersize=2.8, lw=LW, ls=SUBJ_LS[sname],
                markerfacecolor='white' if SUBJ_OPEN[sname] else DRUG[dkey],
                markeredgecolor=DRUG[dkey], markeredgewidth=LW,
                label=sname, clip_on=False, zorder=3)
    ax.set_xticks(xs)
    ax.set_xticklabels(['baseline'] + [f'{float(v):g}' for v in levels[1:]],
                       rotation=45, ha='right', fontsize=TICK_PT)
    ax.set_xlabel(xlab); ax.set_ylabel('NP factor')
    ax.set_xlim(-.4, len(levels) - .6)
    ax.set_ylim(ylo - ypad, yhi + ypad)
    ax.set_yticks(np.arange(ylo, yhi + .01, 1.0))
    ax.legend(loc='best', fontsize=ANNOT_PT, handletextpad=.5, labelspacing=.25)
    panel_title(ax, ttl)
    enforce(fig); save(fig, stem, wmm, 46, f'{stem}_{"ampa" if stem == "fig3e" else "gaba"}_sweep.csv')

# ------------ g  Delta NP after perturbation, all SEVEN builds (n = 12 each)
# Delta is defined per build against that build's OWN baseline, using the
# modulation style the build was run in:
#   regional builds (3 M/268, 10 M/268, 10 M/1000) -> the `_r` conditions
#   voxel builds (10 M, 100 M, 1 B)                -> the plain conditions
#   new 3 M/268 run  -> manipu / manipu_gaba minus manipu_gaba_baseline, the
#                       baseline shipped inside the same perturbation file, so
#                       the difference is free of run-to-run drift (5-repeat mean)
#   new 10 M voxel (own hyper-parameters) -> the population run, single run
#   100 M -> perturbed from the archive wide table for 9 twins and from
#            orignial_3subs_perturb_100m_whole_brain_fc/ for HC01, MDD and AUD
#            (AMPA 0.0044; GABA-A 0.0040 applied on AMPA 0.0044; 5 repeats,
#            12 NP edges taken on the 217 axis via edge_definitions.csv),
#            baseline from the newflow table for all 12.  The three rows the
#            superseded table carried for these twins were (100 M perturbed)
#            minus the 3 M BASELINE, a cross-build subtraction, and are dropped.
# The superseded 3 M perturbation (mean Delta NP +0.97 under AMPA, +3.15 under
# GABA-A) is NOT shown; the new run gives -0.02 and +1.13 for the same twins.
gg = pd.read_csv(f'{D}/fig3g_delta_np_seven_models.csv')
W, H = 122, 56
fig, ax = plt.subplots(figsize=panel(W, H))
rng = np.random.default_rng(2)
off = {'ampa': -.18, 'gaba': .18}
for drug in ['ampa', 'gaba']:
    for i, m_ in enumerate(BUILDS7):
        v = gg[(gg.drug == drug) & (gg.model == m_)].delta.values
        ax.scatter(i + off[drug] + rng.uniform(-.06, .06, len(v)), v, s=13,
                   facecolor=DRUG[drug], edgecolor='none', alpha=.85, zorder=3)
        ax.hlines(v.mean(), i + off[drug] - .13, i + off[drug] + .13,
                  color='black', lw=LW, zorder=4)
ax.axhline(0, color='0.6', lw=LW, ls=(0, (2.6, 1.7)), zorder=1)
ax.set_xticks(range(len(BUILDS7)))
ax.set_xticklabels([BLAB[m_] for m_ in BUILDS7], fontsize=TICK_PT)
for t, m_ in zip(ax.get_xticklabels(), BUILDS7):
    t.set_color(FAM[BFAM[m_]])
hyper_row(ax, BUILDS7, y=-.27)
ax.set_ylabel('Δ NP  (perturbed − baseline)')
ax.set_xlim(-.55, len(BUILDS7) - .45)
ymax = float(gg.delta.max())
ax.set_ylim(float(gg.delta.min()) - .3, ymax * 1.28)
block_bands(ax, BUILDS7, ymax * 1.12)
handles = [Line2D([], [], marker='o', linestyle='none', markersize=4,
                  markerfacecolor=DRUG[d], markeredgecolor='none')
           for d in ['ampa', 'gaba']]
ax.legend(handles, [DRUG_LAB[d] for d in ['ampa', 'gaba']], loc='lower right',
          ncol=2, fontsize=ANNOT_PT, handletextpad=.4, columnspacing=1.0,
          frameon=False)
panel_title(ax, 'Only the two 268-region builds show a group-level increase, '
                'and only under GABA-A')
enforce(fig); save(fig, 'fig3g', W, H, 'fig3g_delta_np_seven_models.csv')


# ============================ assembled figure ==============================
# Panels placed at their TRUE printed size on a 180 mm page -- no rescaling, so
# the type inside every panel prints at the size it was drawn at.  Row heights
# are measured from the panel images rather than hard-coded.
import matplotlib.image as mpimg
PAGE_W, GAP_X, GAP_Y, TOP_PAD = 180.0, 8.0, 7.0, 3.0
ROWS = [[('fig3a', 110)], [('fig3b', 110)],
        [('fig3c', 62), ('fig3d', 86)],
        [('fig3e', 62), ('fig3f', 62)],
        [('fig3g', 110)]]

placed, y = [], TOP_PAD
for row in ROWS:
    x, row_h = 0.0, 0.0
    for stem, w_mm in row:
        im = mpimg.imread(f'{OUTD}/{stem}.png')
        h_mm = w_mm * im.shape[0] / im.shape[1]
        placed.append((stem, im, x, y, w_mm, h_mm))
        row_h = max(row_h, h_mm); x += w_mm + GAP_X
    y += row_h + GAP_Y
PAGE_H = y - GAP_Y + 2

figA = plt.figure(figsize=panel(PAGE_W, PAGE_H))
for stem, im, x_mm, y_mm, w_mm, h_mm in placed:
    axx = figA.add_axes([x_mm / PAGE_W, 1 - (y_mm + h_mm) / PAGE_H,
                         w_mm / PAGE_W, h_mm / PAGE_H])
    axx.imshow(im); axx.axis('off')
    figA.text(max(x_mm - 2.5, 0.3) / PAGE_W, 1 - (y_mm - 1.0) / PAGE_H, stem[-1],
              fontsize=LABEL_PT, fontweight='bold', va='bottom', ha='left')
figA.savefig(os.path.join(HERE, 'fig3_assembled.png'), dpi=DPI, bbox_inches='tight')
figA.savefig(os.path.join(HERE, 'fig3_assembled.pdf'), bbox_inches='tight')
plt.close(figA)
print('assembled %.0f x %.0f mm' % (PAGE_W, PAGE_H))

pd.DataFrame(manifest).to_csv(f'{OUTD}/panel_manifest.csv', index=False)
print(pd.DataFrame(manifest).to_string(index=False))
print('\na  MSE mean by model:',
      {m: round(float(a3.loc[a3.model == m, "mse"].mean()), 4) for m in MODELS})
print('c  same-hyper block means | baseline, AMPA, GABA-A:',
      [round(float(np.mean([m_.iloc[i_, j_] for i_ in range(7) for j_ in range(i_ + 1, 7)
                            if BHYP[BUILDS7[i_]] == BHYP[BUILDS7[j_]]])), 3)
       for m_ in (b3,
                  pd.read_csv(f'{D}/fig3c_cross_scale_similarity_ampa.csv', index_col=0),
                  pd.read_csv(f'{D}/fig3c_cross_scale_similarity_gaba.csv', index_col=0))])
print('d  run-to-run s.d.:', dict(zip(c3.model, c3.run_sd_mean)))
print('g  mean ΔNP by build:',
      f6.groupby(['drug', 'model']).delta.mean().round(3).to_dict())

# ------------------ i  assimilated-region BOLD fidelity, all seven builds
# Source: baseline同化区域BOLD_r总表.xlsx (3m_model_new_run/).  For each subject
# and task the simulated BOLD time course is correlated with the measured one
# within the assimilated regions (MID 51 / SST 47 Shen labels), averaged over
# the assimilated voxels.  Old batches are the mean of 5 repeats, the new
# 10 M voxel build a single run.  This is a fidelity measure ONE LEVEL ABOVE
# FC: it scores the signal the model was assimilated to reproduce, before any
# edge is formed, so it is the measure on which the fidelity reference should
# be chosen.
bi = pd.read_csv(f'{D}/fig3i_assimilated_bold_r.csv')
W, H = 112, 56
fig, ax = plt.subplots(figsize=panel(W, H))
MK = {'MID': 'o', 'SST': 's'}
rng = np.random.default_rng(5)
for i, m in enumerate(BUILDS7):
    col = FAM[BFAM[m]]
    sub = bi[bi.model == m]
    for tk in ('MID', 'SST'):
        v = sub[sub.task == tk].bold_r.values
        dx = -.16 if tk == 'MID' else .16
        ax.scatter(i + dx + rng.uniform(-.05, .05, len(v)), v, s=9, marker=MK[tk],
                   facecolor='white', edgecolor=col, linewidth=LW, zorder=3)
        ax.hlines(v.mean(), i + dx - .13, i + dx + .13, color=col, lw=LW * 1.6, zorder=4)
ax.set_xticks(range(len(BUILDS7)))
ax.set_xticklabels([BLAB[m] for m in BUILDS7], fontsize=TICK_PT)
for t, m in zip(ax.get_xticklabels(), BUILDS7):
    t.set_color(FAM[BFAM[m]])
hyper_row(ax, BUILDS7, y=-.28)
ax.set_ylabel('Assimilated-region BOLD $r$')
ax.set_ylim(.55, 1.0)
block_bands(ax, BUILDS7, .965)
hM = [Line2D([], [], marker=MK[t], linestyle='none', markersize=3,
             markerfacecolor='white', markeredgecolor='0.35', markeredgewidth=LW)
      for t in ('MID', 'SST')]
ax.legend(hM, ['MID', 'SST'], loc='lower right', ncol=2, fontsize=ANNOT_PT,
          handletextpad=.3, columnspacing=.9, frameon=False)
panel_title(ax, 'Assimilation fidelity is set by the hyper-parameter scale, '
                'not the simulated scale')
enforce(fig); save(fig, 'fig3i', W, H, 'fig3i_assimilated_bold_r.csv')
