"""Supplementary figure: PET-derived receptor availability in negative-profile
regions versus the rest of the Shen-268 parcellation.

Region set
----------
The 32 regions are the nodes of the 29-edge NEGATIVE PROFILE (MATLAB variable
`np_idx_29` in np_32_regions_permutation_test.mat).  They are a superset of the
19 nodes of the 12-edge NP factor, which is why they carry the negative-profile
colour (#6BAED6) and NOT the NP-factor blue (#0072B2) used in the main figures.
A 19-region version of the same test is available in p_permutation_test.mat and
yields 6 rather than 11 FDR-significant maps.

Statistics
----------
Unit of observation = one Shen-268 region.  For each of the 39 PET maps the test
statistic is the difference in mean regional value (negative-profile minus
non-profile).  The null is built by randomly reassigning the region labels
10,000 times while preserving group sizes (32 / 236); the two-sided P value is
(#|null| >= |observed| + 1) / (n_perm + 1).  P values are corrected across all
39 maps with Benjamini-Hochberg FDR; panels a-k are the 11 maps with q < 0.05.
Panel l shows all 39 maps so that the selection is visible.

Inputs : data/pet_permutation_39maps.csv, data/pet_regional_values_268x39.csv
Outputs: panels/figS_pet_*.png|.pdf, panels/pet_panel_manifest.csv
"""
import os, sys
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
sys.path.insert(0, os.path.join(HERE, '..'))
from np_dtb_style import apply_np_style, panel, C, panel_title, LW
from supp_kit import saver, fill, pt_edge, boxes
from fig_export import fig_to_pptx
import figA4_kit as PK          # the frozen type scale: 8 / 9 / 10 / 11 pt

apply_np_style()
manifest = []
save = saver(os.path.join(HERE, 'panels'), manifest)
ST = pd.read_csv(os.path.join(HERE, 'data', 'pet_permutation_39maps.csv'))
RV = pd.read_csv(os.path.join(HERE, 'data', 'pet_regional_values_268x39.csv'))

C_NP, C_OT = C('neg_profile'), C('non_np')
GRP = RV['group'].values == 'NP-related'
rng = np.random.default_rng(7)


def one_map(row, letter):
    col = row.map_file.replace('.nii.gz', '').replace('.nii', '')
    v = RV[col].values
    a, b = v[GRP], v[~GRP]
    fig, ax = plt.subplots(figsize=panel(52, 50))
    boxes(ax, [0, 1], [a, b], [C_NP, C_OT], width=.52, jitter=.17, s=3.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([f'Negative\nprofile\n(n = {len(a)})', f'Other\nregions\n(n = {len(b)})'])
    ax.set_ylabel('Regional PET value (a.u.)')
    ax.set_xlim(-.55, 1.55)
    lo, hi = min(v.min(), 0), v.max()
    ax.set_ylim(lo - .06 * (hi - lo), hi + .30 * (hi - lo))
    q = row.q_fdr
    ax.text(.5, .995, f"$\\Delta$ = {row['diff']:+.3g}, Hedges' $g$ = {row.hedges_g:.2f}\n"
                      f"$P_{{perm}}$ = {row.p_perm:.4f}, $q_{{FDR}}$ = {q:.3f}",
            transform=ax.transAxes, ha='center', va='top', fontsize=6, color='0.25',
            linespacing=1.25)
    panel_title(ax, row.label)
    fig.tight_layout()
    save(fig, f'figS_pet_{letter}', 52, 50,
         'pet_permutation_39maps.csv / pet_regional_values_268x39.csv')


sig = ST[ST.fdr_significant].reset_index(drop=True)
order = ['mGluR5_abp_hc73_smart.nii', 'mGluR5_abp_hc28_dubois.nii', 'mGluR5_abp_hc22_rosaneto.nii',
         '5HT2a_alt_hc19_savli.nii', '5HT2a_cimbi_hc29_beliveau.nii', '5HT2a_mdl_hc3_talbot.nii.gz',
         '5HT1a_cumi_hc8_beliveau.nii', '5HT1a_way_hc36_savli.nii',
         '5HT6_gsk_hc30_radhakrishnan.nii.gz', 'M1_lsn_hc24_naganawa.nii.gz',
         'CB1_FMPEPd2_hc22_laurikainen.nii']
sig = sig.set_index('map_file').loc[order].reset_index()
for k, (_, r) in enumerate(sig.iterrows()):
    one_map(r, 'abcdefghijk'[k])

# ---- panel l: all 39 maps, effect size with FDR status -----------------------
S = ST.sort_values(['receptor', 'map_index']).reset_index(drop=True)
L_W, L_H = 120, 215           # 39 rows at 8 pt need ~4.9 mm of pitch
fig, ax = plt.subplots(figsize=panel(L_W, L_H))
y = np.arange(len(S))[::-1]
for yy, (_, r) in zip(y, S.iterrows()):
    f = C_NP if r.fdr_significant else 'none'
    ax.plot([0, r.hedges_g], [yy, yy], color='0.75', lw=LW * .8, zorder=1)
    ax.scatter([r.hedges_g], [yy], s=26, facecolor=f, edgecolor=C_NP if r.fdr_significant else '0.45',
               linewidth=LW, zorder=3)
ax.axvline(0, color='0.35', lw=LW, zorder=2)
ax.set_yticks(y)
ax.set_yticklabels(S.label.values, fontsize=PK.TICK_PT)
ax.tick_params(axis='both', labelsize=PK.TICK_PT)
for t, s in zip(ax.get_yticklabels(), S.fdr_significant.values):
    t.set_color('0.15' if s else '0.45')
ax.set_ylim(-1, len(S))
ax.set_xlabel("Hedges' $g$ (negative profile \u2212 other regions)",
              fontsize=PK.LABEL_PT)
ax.set_title(f'All 39 PET maps ({int(S.fdr_significant.sum())} survive '
             f'FDR $q$ < 0.05)', fontsize=PK.LABEL_PT, loc='left', pad=3)
ax.scatter([], [], s=26, facecolor=C_NP, edgecolor=C_NP, linewidth=LW, label='$q$ < 0.05')
ax.scatter([], [], s=26, facecolor='none', edgecolor='0.45', linewidth=LW, label='n.s.')
ax.legend(loc='upper left', frameon=False, fontsize=PK.ANNOT_PT,
          handletextpad=.3, bbox_to_anchor=(.01, .99))
fig.tight_layout()
# the pptx text layer only registers with the raster when the background is
# NOT saved through savefig.bbox='tight' (see figA4_kit); do it BEFORE save(),
# which closes the figure
with mpl.rc_context({'savefig.bbox': None}):
    fig_to_pptx(fig, os.path.join(HERE, 'panels', 'figS_pet_l.pptx'), dpi=400)
save(fig, 'figS_pet_l', L_W, L_H, 'pet_permutation_39maps.csv', pptx=False)

MF = pd.DataFrame(manifest)
MF.to_csv(os.path.join(HERE, 'panels', 'pet_panel_manifest.csv'), index=False)
print(MF.to_string(index=False))
