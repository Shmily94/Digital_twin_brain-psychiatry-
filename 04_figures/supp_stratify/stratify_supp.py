"""Supplementary figure: NP profiles in the STRATIFY validation cohort.

Replaces the violin version with the box + all-individual-observations grammar
used throughout the main figures.

Cohort: 434 participants - 225 healthy controls and 209 patients
(MDD 104, AUD 98, psychosis 6, ADHD 1).  Panels a, c and d contrast HC with
MDD and with AUD separately; panel b contrasts HC with all 209 patients, so
its box is the union of the two patient boxes in a/c/d plus the 7 participants
with other diagnoses - that is why it carries the same warm patient tone.

Scores are residuals after regressing out sex, site and head motion
(pos_neg_np_stratify_resi_without_ed.csv).

Statistics: two-sided independent-samples Student t test (equal variance,
df = n1 + n2 - 2), Bonferroni-corrected over the three tests within each
measure.  This reproduces the published statistics exactly (Welch's test gives
a materially different value only for AUD in panel a: t = 4.14 vs 3.82).

Inputs : data/stratify_subject_level_n434.csv, data/stratify_group_tests.csv
Outputs: panels/figS_stratify_*.png|.pdf, panels/stratify_panel_manifest.csv
"""
import os, sys
import numpy as np, pandas as pd, matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'fig_color'))
from np_dtb_style import apply_np_style, panel, C, panel_title, LW
from supp_kit import saver, pt_edge, boxes

apply_np_style()
manifest = []
save = saver(os.path.join(HERE, 'panels'), manifest)
D = pd.read_csv(os.path.join(HERE, 'data', 'stratify_subject_level_n434.csv'))
T = pd.read_csv(os.path.join(HERE, 'data', 'stratify_group_tests.csv'))

COL = {'HC': C('hc'), 'MDD': C('mdd'), 'AUD': C('aud'), 'Patient': C('patient')}


def draw(letter, measure, groups, ylab, title):
    vals = [D.loc[D.panel_group == g, measure].values for g in groups]
    cols = [COL[g] for g in groups]
    fig, ax = plt.subplots(figsize=panel(46 + 16 * len(groups), 62))
    boxes(ax, list(range(len(groups))), vals, cols, width=.58, jitter=.19, s=3.2)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([f'{g}\n(n = {len(v)})' for g, v in zip(groups, vals)])
    ax.set_ylabel(ylab)
    ax.set_xlim(-.62, len(groups) - .38)
    lo = min(v.min() for v in vals); hi = max(v.max() for v in vals)
    span = hi - lo
    ax.set_ylim(lo - .05 * span, hi + (.13 + .115 * (len(groups) - 1)) * span)
    sub = T[T.panel == letter]
    for k, (_, r) in enumerate(sub.iterrows()):
        j = groups.index(r.group)
        y = hi + (.04 + .115 * k) * span
        ax.plot([0, 0, j, j], [y, y + .022 * span, y + .022 * span, y],
                color='0.35', lw=LW, clip_on=False)
        star = ('***' if r.p_bonf3 < .001 else '**' if r.p_bonf3 < .01
                else '*' if r.p_bonf3 < .05 else 'n.s.')
        ax.text(j / 2, y + .030 * span,
                f"$t$({int(r.df)}) = {r.t:.2f}, $P_{{Bonf}}$ = {r.p_bonf3:.3g}  {star}",
                ha='center', va='bottom', fontsize=6, color='0.25')
    panel_title(ax, title)
    fig.tight_layout()
    save(fig, f'figS_stratify_{letter}', 46 + 16 * len(groups), 62,
         'stratify_subject_level_n434.csv / stratify_group_tests.csv')


draw('a', 'Neg_NP', ['HC', 'MDD', 'AUD'],
     'Negative-profile score\n(residual)', 'Negative FC profile')
draw('b', 'Pos_NP', ['HC', 'Patient'],
     'Positive-profile score\n(residual)', 'Positive FC profile, all patients')
draw('c', 'Pos_NP', ['HC', 'MDD', 'AUD'],
     'Positive-profile score\n(residual)', 'Positive FC profile by diagnosis')
draw('d', 'NP factor', ['HC', 'MDD', 'AUD'],
     '12-edge NP factor score\n(residual)', 'NP factor')

# ---- e  symptom severity, the panel the main text cites but never showed -----
# Summed DAWBA band score (ADHD, conduct, eating, depression, anxiety, phobia).
# Patients: STRATIFY self-report (STRA_self_dawba.mat) - reproduces the archived
# means exactly (patients 19.271 +/- 10.868, MDD 21.922, AUD 16.427).  Controls
# are assigned to an assessment wave by the author's own lists (revision/
# STARTIFT_HC_subject_list_fu2.txt, 54 IDs; STARTIFY_HC_subject_list_fu3.txt,
# 123 IDs; the two lists do not overlap) and are scored at their designated
# wave only - no substitution across waves:
#   46  STRATIFY-recruited controls, scored from STRA_self_dawba.mat
#   46  on the FU2 list and scored at FU2 (Self_FU2_inter_exter.mat)
#  123  on the FU3 list and scored at FU3 (DAWBA_beha_symptoms_fu3.xlsx)
# = 215 controls, which is the n of the archived analysis; with 199 patients
# the pooled contrast has df = 412, matching the main text.  The 8 remaining
# FU2-list members have no FU2 score and are NOT carried over from FU3; 2
# further controls appear on neither list and have no DAWBA score at all.
# The archived control mean of 7.5395 is not reproduced by the summed six-band
# score from any of these files under any wave assignment - see Table S21.
#
# TEST: unlike panels a-d, this panel uses Welch's unequal-variance t test.  The
# summed band score is a right-skewed count and its variance scales with the
# mean, so the equal-variance assumption fails badly here (variance ratio 2.8-
# 3.1; Levene F = 33-49, all P < 1e-7), whereas in a-d the ratio is 1.1-1.3.
# Panels a-d keep Student's test because that is what reproduces the published
# NP statistics exactly.  Bonferroni over the three contrasts, as in a-d.

SY = pd.read_csv(os.path.join(HERE, 'data', 'stratify_symptom_subject_level.csv'))
SYT = pd.read_csv(os.path.join(HERE, 'data', 'stratify_symptom_tests.csv'))
SY['grp'] = np.where(SY.panel_group == 'HC', 'HC', SY.diagnosis)

groups = ['HC', 'MDD', 'AUD']
vals = [SY.loc[SY.grp == g, 'sym6_sum'].values for g in groups]
fig, ax = plt.subplots(figsize=panel(46 + 16 * len(groups), 62))
boxes(ax, list(range(3)), vals, [COL[g] for g in groups],
      width=.58, jitter=.19, s=3.2)
ax.set_xticks(range(3))
ax.set_xticklabels([f'{g}\nn = {len(v)}' for g, v in zip(groups, vals)])
ax.set_ylabel('Summed DAWBA band score')
hi = max(v.max() for v in vals); lo = min(v.min() for v in vals); span = hi - lo
ax.set_ylim(lo - .05 * span, hi + .36 * span)
for k, g in enumerate(['MDD', 'AUD']):
    r = SYT[SYT.group == g].iloc[0]
    j = groups.index(g)
    y = hi + (.04 + .115 * k) * span
    ax.plot([0, 0, j, j], [y, y + .022 * span, y + .022 * span, y],
            color='0.35', lw=LW, clip_on=False)
    ax.text(j / 2, y + .030 * span,
            f"Welch $t$({r.df:.1f}) = {r.t:.2f}, "
            f"$P_{{Bonf}}$ = {r.p_bonf3:.2g}  ***",
            ha='center', va='bottom', fontsize=6, color='0.25')
panel_title(ax, 'Symptom severity')
fig.tight_layout()
save(fig, 'figS_stratify_e', 46 + 16 * len(groups), 62,
     'stratify_symptom_subject_level.csv / stratify_symptom_tests.csv')

MF = pd.DataFrame(manifest)
MF.to_csv(os.path.join(HERE, 'panels', 'stratify_panel_manifest.csv'), index=False)
print(MF.to_string(index=False))
