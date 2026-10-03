# Figure legends

## Conventions applied throughout

Unless a panel states otherwise, the following hold in every legend below.

**Error indicators.** Box plots show the median (centre line), the 25th–75th percentiles
(box) and the most extreme observation within 1.5 × IQR of the box (whiskers); every
individual observation is overplotted, so no observation is hidden. Bar and point plots
labelled "mean ± s.d." show the arithmetic mean with the sample standard deviation;
"mean ± s.e.m." shows the standard error of the mean; "95% CI" is the Student-*t*
interval on the mean or, for correlations, the Fisher-*z* interval. Shaded bands around
regression lines are 95% confidence bands for the conditional mean. Violin outlines are
Gaussian kernel density estimates (Scott's rule) and carry no inferential meaning.

**Statistical tests.** All tests are **two-sided**. Independent-group comparisons use
Welch's *t* test (unequal variances not assumed equal) with Welch–Satterthwaite degrees
of freedom, accompanied by the Mann–Whitney *U* test as a distribution-free check.
Within-subject comparisons use the **paired** *t* test with the Wilcoxon signed-rank test
as a check; pairing is on subject identity and is stated explicitly in each panel.
Three-group comparisons use one-way ANOVA with post-hoc pairwise tests. Effect sizes are
Cohen's *d* for independent groups, Hedges' *g* where sample sizes are unequal, Cohen's
*d*z for paired designs, and partial η² for ANOVA terms. Correlations are Pearson unless
Spearman is named. Permutation *P* values are the proportion of the null distribution at
or beyond the observed statistic and are therefore **one-sided by construction**; the
number of permutations is given in each case.

**Multiple-comparison correction.** The correction is named per panel. Benjamini–Hochberg
FDR (reported as *q*) is used for families of exploratory tests; Bonferroni is used for
the small pre-specified families in the head-motion analyses (Supplementary Fig. S5,
Supplementary Tables S25–S26). Where no correction was applied, *P* values are labelled
**uncorrected** in the legend.

**Software.** Python 3.11; SciPy 1.x (`ttest_ind`, `ttest_rel`, `ttest_1samp`,
`mannwhitneyu`, `wilcoxon`, `pearsonr`, `spearmanr`, `f_oneway`, `levene`,
`kruskal`, `chi2_contingency`), statsmodels (OLS, nested-model *F* tests, ANCOVA,
`multipletests`), scikit-learn (*k*-means, PLS regression, cross-validation).

**Unit of observation.** Stated in every panel. Three units occur: one subject
(most panels), one subject × task session (Fig. 3i), and one subject × edge cell
(Fig. 3c).

---

## Figure 1 — Study design and modelling framework

Schematic overview of the cohorts, the task-evoked functional-connectivity analysis, the
individualised digital-twin-brain (DTB) assimilation procedure and the in-silico
perturbation protocol. No data are plotted and no statistical test is performed; sample
sizes shown in the schematic are defined in Figs. 2–5 and in Methods.

---

## Figure 2 — A transdiagnostic negative-psychopathology connectivity profile

**a. Symptom prediction from task-evoked connectivity.** Heat map of connectome-based
predictive-modelling (CPM) accuracy, expressed as the Spearman correlation between
cross-validated predicted and observed symptom scores, for six DAWBA symptom domains
(rows: ADHD, CD, ED, SP, GAD, DEP) × six task conditions (columns). Unit of observation:
one subject; the plotted value is a single cross-validated ρ per cell, so no error bar is
defined. Values range 0.00–0.25 (largest: SP under SST stop-failure, ρ = 0.25). *Note for
the authors: this panel is reproduced unchanged from the original analysis; the
permutation P values and the permutation count for each cell must be inserted here from
that analysis — they are not contained in the source table `fig2a_cpm_rho.csv` and were
therefore not recomputed.*

**b. Anatomical layout of the two profiles.** Network-level edge counts of the negative
profile (29 edges, left) and the positive profile (34 edges, right), summarised as a
network × network count matrix over 11 canonical networks. Descriptive; no test.

**c. Negative-profile connectivity by diagnosis (STRATIFY).** Box plots with all subjects
overplotted. Unit of observation: one subject. *n* = 427 (healthy controls 225; patients
202, comprising MDD 104 and AUD 98). Healthy controls +0.381 ± 1.396, patients
−0.113 ± 1.259 (mean ± s.d.). Two-sided Welch's *t* test, unpaired, independent groups:
*t* = 3.850, df = 425.0, *P* = 1.36 × 10⁻⁴, Cohen's *d* = 0.371; Mann–Whitney
*P* = 7.07 × 10⁻⁵. Single pre-specified comparison, no correction applied.

**d. Circos plot of the NP-factor edges.** The 12 cortico-subcortical edges of the NP
factor drawn between their 19 nodes, coloured by canonical network assignment.
Descriptive; no test.

**e. NP factor by diagnosis (STRATIFY).** Box plots with all subjects overplotted, and
the marginal kernel density on the right. Unit of observation: one subject. *n* = 427
(HC 225, patients 202). Healthy controls +0.138 ± 0.879, patients −0.140 ± 0.817
(mean ± s.d.). Two-sided Welch's *t* test, unpaired: *t* = 3.395, df = 424.5,
*P* = 7.51 × 10⁻⁴, Cohen's *d* = 0.328; Mann–Whitney *P* = 3.53 × 10⁻⁴. Single
pre-specified comparison, no correction applied.

**f. Per-edge group difference.** Cohen's *d* (healthy − patient) for each of the 12
NP-factor edges; error bars are 95% confidence intervals on *d*. Unit of observation: one
subject; *n* = 427 per edge. Two-sided independent-samples *t* tests, one per edge,
corrected across the 12 edges by Benjamini–Hochberg FDR. Five edges survive correction:
E1 *t* = 3.20, *d* = 0.310, *P* = 1.48 × 10⁻³, *q* = 5.91 × 10⁻³; E2 *t* = 3.02,
*d* = 0.293, *P* = 2.70 × 10⁻³, *q* = 8.10 × 10⁻³; E3 *t* = 3.78, *d* = 0.366,
*P* = 1.80 × 10⁻⁴, *q* = 2.15 × 10⁻³; E7 *t* = 2.46, *d* = 0.239, *P* = 1.41 × 10⁻²,
*q* = 3.39 × 10⁻²; E10 *t* = 3.30, *d* = 0.320, *P* = 1.06 × 10⁻³, *q* = 5.91 × 10⁻³.
E5 (*P* = 0.036) and E11 (*P* = 0.041) are nominally significant but do not survive FDR
(both *q* = 0.071); E4, E6, E8, E9 and E12 are not significant. Degrees of freedom are
425 for every edge.

**Source data:** `fig2a_cpm_rho.csv`, `fig2b_network_neg.csv`, `fig2b_network_pos.csv`,
`fig2c_profile_scores.csv`, `fig2d_circos_matrix.csv`, `fig2d_nodes.csv`,
`fig2e_edge_group_difference.csv`. A cohort/covariate sensitivity analysis accompanying
panel f is tabulated in `fig2f_sensitivity_cohort_covariates.csv` (three cohort
definitions × two covariate schemes; the number of FDR-surviving edges ranges 4–7).

---

## Figure 3 — Multiscale validation of the digital twin brain

Seven DTB builds are compared. They differ on three independent axes — the number of
**simulated** neurons, the neuron count of the **assimilated hyper-parameter** set, and
the **spatial resolution** of the simulation target — and every panel carries a second
tick row naming the assimilated hyper-parameter set, because the two 10 M voxel builds
are identical on the other two axes. Builds: 3 M / 268 (hyper 3 M), 10 M / 268
(hyper 3 M), 10 M / 1000 (hyper 10 M-1000), 10 M / voxel (hyper 10 M voxel), 10 M / voxel
(hyper 100 M), 100 M / voxel (hyper 100 M), 1 B / voxel (hyper 100 M). Build identity
follows `baseline同化区域BOLD_r总表.xlsx`, sheet `口径与来源`: `10m_reg` is the
10 M / 1000 build and `regional` is the 10 M / 268 build. In every panel, colour encodes
model family (regional vs voxel) and never encodes any other variable; benchmarks are
grey.

**a. NP-edge simulation error.** Box plots with all 12 twins overplotted. Unit of
observation: one subject. *n* = 12 per build. The plotted quantity is the mean squared
error between the simulated and the measured 12-edge NP profile. All seven DTB builds are
scored against a single empirical reference, `empirical_model_voxels` (empirical FC
recomputed from only the voxels the DTB simulates; identical to `real_fc_dtb_voxels` and
to `emp_edge1-12`, *r* = 1.0000). Builds with repeats are the mean of 5 independent
simulation repeats; the 10 M voxel build with its own hyper-parameters was run once.
Mean MSE: 10 M voxel (hyper 100 M) 0.0498; 100 M 0.0589; 3 M / 268 0.0649; 1 B 0.0655;
10 M / 268 0.0718; 10 M voxel (own hyper) 0.0958; 10 M / 1000 0.0975. Two-sided paired
*t* tests across the 12 twins (pairing on subject): 10 M vs 1 B Δ = −0.0157,
*P* = 0.001 (Wilcoxon *P* = 0.001); 10 M vs 100 M Δ = −0.0092, *P* = 0.041; 100 M vs 1 B
Δ = −0.0065, *P* = 0.060; 3 M / 268 vs 1 B Δ = −0.0006, *P* = 0.957; 3 M / 268 vs
10 M / 268 Δ = −0.0069, *P* = 0.338; df = 11 throughout. These are exploratory pairwise
comparisons and are reported **uncorrected**. The two benchmarks, SAR (0.0698) and rWW
(0.1010), are **deliberately scored against a different empirical reference** — the
Shen-268 regional task FC against which their coupling parameters were fitted — and are
therefore not on the same scale as the DTB columns; the `empirical_reference` column of
the source table records which reference each row uses. Re-scoring the benchmarks against
`empirical_model_voxels` gives SAR 0.0528 and rWW 0.0824
(`fig3a_benchmark_reference_check.csv`).

**b. Whole-brain FC similarity.** Mean ± s.d. across the 12 twins of the Pearson
correlation between simulated and measured whole-brain FC (23,436 upper-triangular edges
among 217 nodes), separately for the four task conditions (marker shape). Unit of
observation: one subject × condition; *n* = 12 per point. Descriptive; no inferential
test is performed on this panel. Voxel builds with 100 M hyper-parameters reach
*r* = 0.57–0.63, the regional builds 0.12–0.52, and the 10 M voxel build with its own
hyper-parameters 0.05–0.10; benchmarks SAR 0.20–0.28 and rWW 0.13–0.17. The values for
the three archive voxel builds were independently recomputed from
`new10m_simulated_FC_12subs_with_empirical.mat` and reproduce the tabulated values to
four decimal places.

**c. Cross-build similarity of the baseline NP profile.** 7 × 7 matrix of **Spearman**
rank correlations computed over all 12 subjects × 12 edges = **144 subject × edge cells**
of the raw baseline NP values (no per-subject averaging, no Fisher-*z*, no
standardisation). Unit of observation: one subject × edge cell; *n* = 144 per matrix
entry. Descriptive; no *P* values are attached, because the 21 off-diagonal entries are
not independent. Spearman rather than Pearson is used because the builds differ markedly
in tail behaviour: the 10 M voxel own-hyper-parameter build has excess kurtosis 10.6 (one
cell at *z* = +6.5), and its Pearson agreement with the 10 M / 100 M build falls from
0.21 to −0.04 when the five most extreme of the 144 cells are removed, whereas Spearman
moves only from 0.07 to −0.02. The two metrics rank the 21 off-diagonal pairs almost
identically (ρ = 0.96, maximum shift 0.14), so the choice does not create the block
structure; the Pearson matrix is provided as source data. Builds sharing an assimilated
hyper-parameter set agree (3 M hyper pair ρ = 0.89; 100 M hyper block ρ = 0.87–0.93),
builds sharing only their simulated scale do not (ρ = 0.06–0.52).

**d. Run-to-run variability.** Bars are the mean across the 12 twins of the
within-subject standard deviation of the summed NP factor across 5 independent simulation
repeats; error bars are the s.d. of that quantity across the 12 twins. Unit of
observation: one subject. *n* = 12 subjects × 5 repeats per build. Descriptive; no test.
1 B 0.125 ± 0.041; 100 M 0.287 ± 0.135; 10 M / 268 0.316 ± 0.152; 10 M voxel
0.327 ± 0.263; 3 M / 268 0.373 ± 0.232; 10 M / 1000 0.448 ± 0.226. The 10 M voxel
own-hyper-parameter build was run once and has no repeat variability; its position is
labelled "single run (no repeats)" rather than plotted as zero.

**e, f. Conductance sweeps in three twins.** NP factor as a function of AMPA conductance
(e; 9 settings, 0.0020–0.0052) and GABA-A conductance (f; 5 settings, 0.0020–0.0040) in
three individual twins (HC01, MDD, AUD), with each twin's own baseline marked. Unit of
observation: one subject × conductance setting; *n* = 3 twins. **Descriptive only; no
statistical test is performed and none is appropriate at *n* = 3.**

**g. Perturbation-induced ΔNP across builds.** Individual twins (points) and the group
mean (horizontal bar) for the change in summed NP factor after AMPA and after GABA-A
perturbation, in **all seven builds**. Unit of observation: one subject; *n* = 12 per
build × perturbation. Two-sided one-sample *t* tests against zero, df = 11, corrected
across the 14 tests by Benjamini–Hochberg FDR.
*AMPA:* 10 M voxel +0.609, *t* = 2.348, *P* = 0.039, *q* = 0.135; 10 M / 268 +0.583,
*t* = 2.142, *P* = 0.055, *q* = 0.155; 100 M +0.440, *t* = 1.928, *P* = 0.080,
*q* = 0.176; 1 B +0.368, *t* = 1.468, *P* = 0.170, *q* = 0.298; 10 M / 1000 +0.040,
*t* = 0.097, *P* = 0.925, *q* = 0.946; 3 M / 268 (new run) −0.017, *t* = −0.069,
*P* = 0.946, *q* = 0.946; 10 M voxel with its own hyper-parameters −0.337, *t* = −1.043,
*P* = 0.319, *q* = 0.447. **No build survives correction under AMPA.**
*GABA-A:* 10 M / 268 +1.159, *t* = 10.20, *P* = 6.09 × 10⁻⁷, *q* = 8.52 × 10⁻⁶,
*d*z = 2.943; 3 M / 268 (new run) +1.131, *t* = 7.858, *P* = 7.74 × 10⁻⁶,
*q* = 5.42 × 10⁻⁵, *d*z = 2.268; 100 M +0.369, *t* = 2.959, *P* = 0.013, *q* = 0.061;
10 M / 1000 +0.399, *t* = 0.788, *P* = 0.447, *q* = 0.570; 10 M voxel +0.341,
*t* = 1.871, *P* = 0.088, *q* = 0.176; 1 B +0.271, *t* = 1.353, *P* = 0.203, *q* = 0.316;
10 M voxel own hyper-parameters −0.141, *t* = −0.632, *P* = 0.540, *q* = 0.630.
**Only the two 268-region builds survive correction, and only under GABA-A.**
GABA-A perturbation is applied **on top of** the AMPA perturbation, not to the
unperturbed baseline.
*Delta definition, which differs by build and must be stated:* each build is compared
with its **own** baseline in the modulation style it was run in — the regional builds
(3 M / 268, 10 M / 268, 10 M / 1000) use the `_r` conditions, the voxel builds the plain
conditions; the new 3 M run uses `manipu` and `manipu_gaba` minus the
`manipu_gaba_baseline` shipped inside the same perturbation file (5-repeat mean), so the
difference carries no run-to-run drift; the new 10 M voxel build is a single run from the
population simulation.
*Change from the superseded 3 M run:* with the discarded 3 M data this panel showed
+0.967 under AMPA (*P* = 1.2 × 10⁻³) and +3.146 under GABA-A (*P* = 4.9 × 10⁻⁷) for the
3 M / 268 build. **The new run gives −0.017 and +1.131 for the same twins**, i.e. the AMPA
effect in the regional build disappears and the GABA-A effect falls to the level of the
10 M / 268 build (+1.131 vs +1.159), which the two builds now match closely. Any
main-text statement that the group-level AMPA increase is present in every build must be
revised.

**i. Assimilated-region BOLD fidelity.** Pearson correlation between the simulated and
the measured BOLD time course within the assimilated regions (MID: 51 Shen labels; SST:
47 Shen labels), averaged across the assimilated voxels. Unit of observation: **one
subject × task session**; each build contributes 12 subjects × 2 tasks = 24 points, shown
individually with the group mean as a horizontal bar. Builds with repeats are the mean of
5 repeats; the 10 M voxel own-hyper-parameter build is a single run. Means: 10 M / 268
0.9134; 3 M / 268 0.9132; 1 B 0.8972; 100 M 0.8958; 10 M voxel (hyper 100 M) 0.8916;
10 M voxel (own hyper) 0.7740; 10 M / 1000 0.6858. Two-sided **paired** *t* tests,
pairing on subject × task, *n* = 24, df = 23, reported **uncorrected** as a
pre-specified ordered set: 1 B vs 100 M Δ = +0.0014, *P* = 9.3 × 10⁻³; 1 B vs 10 M
Δ = +0.0056, *P* = 2.3 × 10⁻³; 100 M vs 10 M Δ = +0.0042, *P* = 0.019; 3 M / 268 vs 1 B
Δ = +0.0159, *P* = 2.3 × 10⁻⁷; 10 M vs 10 M own-hyper Δ = +0.1175, *P* = 6.2 × 10⁻¹¹;
10 M own-hyper vs 10 M / 1000 Δ = +0.0882, *P* = 1.0 × 10⁻⁷. Within the 100 M
hyper-parameter family the ordering 10 M < 100 M < 1 B is monotone and every step is
significant, but the differences are small (≤ 0.006); the difference between 3 M / 268
and 10 M / 268 is −0.0002 (95% CI −0.0003 to −0.0001), i.e. statistically resolvable but
numerically negligible, and should be read as **equivalence**, not as a difference.

**Source data:** `fig3a_mse_per_subject.csv`, `fig3a_benchmark_reference_check.csv`,
`fig3b_wholebrain_fc_crossscale.csv`, `fig3c_cross_scale_similarity.csv` (Spearman,
plotted), `fig3c_cross_scale_similarity_pearson.csv`, `fig3c_metric_comparison.csv`,
`fig3d_run_to_run_sd.csv`, `fig3d_run_to_run_sd_per_subject.csv`, `fig3e_ampa_sweep.csv`,
`fig3f_gaba_sweep.csv`, `fig3g_delta_np_seven_models.csv` (plotted), `fig3g_delta_np_stats_by_model.csv`,
`fig3g_delta_np_six_models.csv` (superseded six-build version), `fig3i_assimilated_bold_r.csv`,
`fig3i_bold_r_paired_tests.csv`.

---

## Figure 4 — Virtual perturbation stratifies individuals

Cohort: *n* = 288 (healthy controls 69, high-symptom 89, patients 130) after excluding
two subjects with mean framewise displacement > 0.5 mm. GABA-A perturbation is always
applied **on top of** the AMPA perturbation.

**a–d. Group differences in NP factor under four conditions.** Box plots with all
subjects overplotted; unit of observation: one subject; *n* = 288 (69 / 89 / 130).
One-way ANOVA across the three groups, F(2, 285), followed by pairwise two-sided
independent *t* tests corrected across the three pairwise comparisons within each panel by
Benjamini–Hochberg FDR (reported as *q*).
**a, measured NP factor:** *F* = 8.203, *P* = 3.44 × 10⁻⁴; HC vs high-symptom
*P* = 0.016, *q* = 0.024; HC vs patient *P* = 6.8 × 10⁻⁵, *q* = 2.04 × 10⁻⁴;
high-symptom vs patient *P* = 0.147, *q* = 0.147.
**b, simulated baseline:** *F* = 9.223, *P* = 1.31 × 10⁻⁴; HC vs high-symptom
*P* = 0.944, *q* = 0.944; HC vs patient *P* = 1.04 × 10⁻³, *q* = 1.57 × 10⁻³;
high-symptom vs patient *P* = 3.40 × 10⁻⁴, *q* = 1.02 × 10⁻³.
**c, after AMPA:** *F* = 0.952, *P* = 0.387; no pairwise comparison survives
(*q* = 0.44–0.76).
**d, after AMPA + GABA-A:** *F* = 0.851, *P* = 0.428; no pairwise comparison survives
(*q* = 0.55–0.74).

**e. Healthy-control versus patient separation across the four conditions.** Kernel
density estimates of the NP factor in the two extreme groups, with the standardised
group difference beneath. Unit of observation: one subject; *n* = 199 (HC 69,
patients 130; the high-symptom group is excluded from this contrast by design).
Two-sided independent-samples *t* tests, one per condition, reported **uncorrected** as
four pre-specified contrasts: measured *d* = 0.618 (95% CI 0.320–0.916), *t* = 4.111,
*P* = 6.8 × 10⁻⁵; simulated baseline *d* = 0.531 (0.234–0.827), *t* = 3.362,
*P* = 1.04 × 10⁻³; after AMPA *d* = 0.179 (−0.114 to 0.471), *t* = 1.194, *P* = 0.235;
after GABA-A *d* = 0.047 (−0.245 to 0.339), *t* = 0.329, *P* = 0.742. df = 197 throughout.

**f. Bidirectional response pattern.** Each subject's change in NP factor under AMPA
plotted against the change under GABA-A, classified as "both up" (increased under both
perturbations) or "any down". Unit of observation: one subject; *n* = 288. Counts: both
up 229 (79.5%), any down 59 (20.5%); 234 of 288 (81.2%) increase under AMPA and 282 of
288 (97.9%) under GABA-A. Descriptive classification; **no statistical test is applied to
this split, because the grouping is defined by the sign of the plotted quantity and any
group contrast on it would be circular.**

**g. MID-network connectivity under the same split.** Summed FC across the six MID edges,
at simulated baseline and after each perturbation, for the two response groups defined in
panel f. Unit of observation: one subject; *n* = 288 (both up 229, any down 59). The
grouping is defined on the 12-edge NP factor and the plotted quantity is the 6-edge MID
sum, so these contrasts are **not** circular. Two-sided one-sample *t* tests against zero
within group and two-sided Welch's *t* test between groups, unpaired, reported
**uncorrected**. Simulated baseline: both up −0.313 ± 0.584 (*t* = −8.119,
*P* = 2.93 × 10⁻¹⁴), any down +0.223 ± 0.514 (*t* = 3.339, *P* = 1.47 × 10⁻³); between
groups Δ = −0.537, *t* = −6.949, *P* = 3.78 × 10⁻¹⁰, Hedges' *g* = −0.941, Mann–Whitney
*P* = 5.64 × 10⁻⁹. Change after AMPA: both up +0.698 (*t* = 18.67, *P* = 7.74 × 10⁻⁴⁸),
any down +0.005 (*t* = 0.090, *P* = 0.929, i.e. indistinguishable from zero); between
groups *t* = 10.19, *P* = 9.96 × 10⁻¹⁸, *g* = 1.279, Mann–Whitney *P* = 3.37 × 10⁻¹⁵.
Change after GABA-A: both up +1.119 (*t* = 16.71, *P* = 1.86 × 10⁻⁴¹), any down +0.644
(*t* = 4.706, *P* = 1.61 × 10⁻⁵); between groups *t* = 3.117, *P* = 2.47 × 10⁻³,
*g* = 0.465, Mann–Whitney *P* = 3.21 × 10⁻³.

**h. Symptom differences between response groups.** Unit of observation: one subject.
Two-sided Mann–Whitney *U* tests with Hedges' *g* and its 95% CI; correction by
Benjamini–Hochberg FDR **within each symptom family separately**.
*DAWBA (7 tests: 6 bands + the 6-band sum; n = 284, split as in panel f: 227 both-up /
57 any-down):* only the eating-disorder band survives — *g* = −0.454 (95% CI −0.747 to
−0.162), *U* = 5127, *P* = 3.55 × 10⁻³, *q* = 0.025. ADHD *g* = 0.187, *P* = 0.201,
*q* = 0.471; the remaining bands and the 6-band sum *P* ≥ 0.202. *(An alternative split
on the sign of the AMPA response alone — 232 up / 52 down — is tabulated in
`fig4h_dawba_stats.csv` and gives the same single survivor with a larger effect,
eat *g* = −0.545, U = 4568, P = 9.88 × 10⁻⁴, q = 6.9 × 10⁻³; the panel and this legend
use the both-up / any-down split so that the symptom analysis matches the response
grouping defined in panel f.)*
*SDQ items (26 tests, n = 287: 228 up / 59 down):* **no item survives FDR**; the two
smallest raw *P* values are `sfriend` (*g* = −0.331, *U* = 5966, *P* = 0.026) and
`sattends` (*g* = −0.315, *U* = 5614, *P* = 0.029), both *q* = 0.374.
*SDQ composites (9 tests):* no composite survives (minimum *q* = 0.58; the peer-problems
subscale has *P* = 0.021 uncorrected, *q* = 0.636, and *P* = 0.156 after adjustment for
sex, site and head motion).
*Multivariate summary:* PLS-DA on 26 SDQ items, 2 components, cross-validated AUC = 0.542;
adding the 6 DAWBA bands AUC = 0.583 (permutation *P* = 0.068, one-sided by construction),
falling to 0.555 (*P* = 0.17) after adjustment for sex, site and head motion. First
canonical correlation between 32 behavioural measures and the three brain measures
*r* = 0.459 (permutation *P* = 0.020), falling to 0.419 (*P* = 0.178) after the same
adjustment. Sex is associated with the response pattern (χ²(1) = 5.53, *P* = 0.019;
logistic likelihood-ratio χ²(1) = 4.76, *P* = 0.029 adjusting for site, head motion and
group); site is not (χ²(7) = 10.49, *P* = 0.162).

**i. Paired within-subject perturbation effects.** Before-after plot of every subject,
with the group mean. Unit of observation: one subject; *n* = 288. Two-sided **paired**
*t* tests (pairing on subject), df = 287, with the Wilcoxon signed-rank test as a check;
four pre-specified comparisons, reported **uncorrected**. NP factor, AMPA: mean change
+0.777 ± 0.933, 234/288 (81.2%) increased, *t* = 14.14, *P* = 8.43 × 10⁻³⁵,
Wilcoxon *P* = 1.19 × 10⁻²⁸, *d*z = 0.833. NP factor, GABA-A: +2.736 ± 1.713, 282/288
(97.9%) increased, *t* = 27.11, *P* = 4.04 × 10⁻⁸¹, Wilcoxon *P* = 1.52 × 10⁻⁴⁸,
*d*z = 1.597. MID summed FC, AMPA: +0.556 ± 0.609, 239/288 (83.0%), *t* = 15.49,
*P* = 9.39 × 10⁻⁴⁰, *d*z = 0.913. MID summed FC, GABA-A: +1.022 ± 1.038, 243/288 (84.4%),
*t* = 16.71, *P* = 2.91 × 10⁻⁴⁴, *d*z = 0.985.

**j. Baseline dependence of the perturbation response.** Change plotted against baseline
(left), against the average of baseline and perturbed value (Oldham's method, centre), and
perturbed value against baseline with the identity line (right). Unit of observation: one
subject; *n* = 288. The naive baseline-versus-change correlation is mathematically
biased by shared measurement error, so the Oldham correlation and the regression of the
perturbed value on the baseline are reported alongside it. AMPA: naive *r* = −0.819
(*P* = 7.38 × 10⁻⁷¹), Oldham *r* = −0.467 (*P* = 5.44 × 10⁻¹⁷), slope of perturbed on
baseline 0.156 (95% CI 0.087–0.225), two-sided *t* test of the slope against 1
*t* = −24.11, df = 286, *P* = 7.38 × 10⁻⁷¹; variance ratio (perturbed / baseline) = 0.375,
i.e. AMPA perturbation **compresses** between-subject spread. GABA-A: naive *r* = −0.240
(*P* = 3.94 × 10⁻⁵), Oldham *r* = +0.589 (*P* = 3.1 × 10⁻²⁸), slope 0.546 (0.332–0.760),
*t* = −4.176, *P* = 3.94 × 10⁻⁵; variance ratio = 3.676, i.e. GABA-A perturbation
**expands** spread. All correlations are two-sided Pearson, reported uncorrected.

**Source data:** `fig4_subject_level_n288.csv`, `fig4ad_group_stats.csv`,
`fig4e_effect_size.csv`, `fig4_paired_np_mid_n288.csv`, `fig4i_paired_stats.csv`,
`fig4j_baseline_change_stats.csv`, `fig4_mid_by_np_grouping_n288.csv`,
`fig4_mid_pattern_subject_n288.csv`, `fig4h_sdq_stats.csv` (both-up / any-down split, plotted),
`fig4h_ampa_sdq_stats.csv` (AMPA-sign split, not plotted),
`fig4_sdq_composite_stats.csv`,
`fig4h_dawba_pattern_stats.csv` (both-up / any-down split, plotted),
`fig4h_dawba_stats.csv` (AMPA-sign split, not plotted),
`fig4_dawba_domains_n284.csv`, `fig4h_multivariate_and_demographics.csv`.

---

## Figure 5 — In-silico perturbation maps onto in-vivo pharmacology and prognosis

**a. Response subgroups in the healthy pharmacological cohort.** NP factor under placebo,
ketamine and midazolam in 27 healthy volunteers, each receiving all three infusions in a
randomised cross-over design. Unit of observation: one subject. Subgroups were defined by
*k*-means clustering (*k* = 2) on the two change scores (ketamine − placebo,
midazolam − placebo), giving 19 "increasers" and 8 "decreasers". **The clustering is
unsupervised with respect to the sign of any single change score and is not defined by
group membership, so subsequent contrasts on these subgroups are not circular.**

**b. Drug-induced change by subgroup.** Change from placebo under ketamine and under
midazolam. Unit of observation: one subject; *n* = 27 (19 / 8). Two-sided one-sample *t*
tests against zero within subgroup and two-sided Welch's *t* test between subgroups
(unpaired); six comparisons, reported **uncorrected**. Ketamine: increasers +0.276,
*t* = 2.597, df = 18, *P* = 0.018; decreasers −0.656, *t* = −3.921, df = 7,
*P* = 5.74 × 10⁻³; between subgroups Δ = 0.932, *t* = 4.703, *P* = 4.15 × 10⁻⁴.
Midazolam: increasers +0.342, *t* = 2.582, df = 18, *P* = 0.019; decreasers −0.813,
*t* = −4.154, df = 7, *P* = 4.27 × 10⁻³; between subgroups Δ = 1.155, *t* = 4.887,
*P* = 2.52 × 10⁻⁴.

**c. Placebo baseline by subgroup.** NP factor under placebo. Unit of observation: one
subject; *n* = 27 (19 / 8). Two-sided Welch's *t* test, unpaired: Δ = −0.668,
*t* = −4.015, *P* = 1.53 × 10⁻³. Single comparison, uncorrected.

**d. Ketamine response in patients versus controls.** Change in NP factor from placebo to
the ketamine state. Unit of observation: one subject; *n* = 36 (MDD 22, HC 14).
**The grouping is by diagnosis, not by response, so these contrasts are not circular.**
Two-sided tests, uncorrected. One-sample *t* against zero: MDD +0.732, *t* = 1.766,
df = 21, *P* = 0.092; HC −1.151, *t* = −1.879, df = 13, *P* = 0.083 — **neither group
differs from zero on its own**. Between groups: Δ = 1.883, Welch *t* = 2.546,
*P* = 0.018. The claim of opposite response direction rests on the between-group test
alone and this should be stated in the main text.

**e. Placebo baseline in patients versus controls.** Unit of observation: one subject;
*n* = 36 (MDD 22, HC 14). Two-sided Welch's *t* test, unpaired: Δ = −1.104, *t* = −2.262,
*P* = 0.034. Single comparison, uncorrected.

**f. Connectivity change versus symptom change in MDD.** Change in NP factor plotted
against change in the first principal component of symptom scores, both residualised on
their own baseline value. Unit of observation: one subject; *n* = 22. Two-sided Pearson
correlation: *r* = −0.426, df = 20, *P* = 0.048. Shaded band is the 95% confidence band
of the regression line. Single comparison, uncorrected; note that *P* is marginal.

**g. Similarity to the AMPA-perturbed twin versus clinical improvement.** Similarity
between each patient's post-ketamine state and their own AMPA-perturbed digital twin,
residualised on age, sex, infusion order and mean framewise displacement, plotted against
change in MADRS. Unit of observation: one subject; *n* = 22. Two-sided Spearman
correlation: ρ = −0.558, *P* = 6.91 × 10⁻³ by permutation of the outcome (5,000
permutations; the permutation *P* is one-sided by construction). Single comparison,
uncorrected.

**h1. Added-variable plot for the AMPA restoration index.** Residual FU3 symptom change
plotted against the residual AMPA index, both after regressing out four baseline
behavioural scores. Unit of observation: one subject; *n* = 85. Partial Pearson
correlation *r* = 0.242, df = 79, *P* = 0.026, two-sided.

**h2. Incremental variance explained.** ΔR² when the AMPA or the GABA-A index is added to
each of two covariate sets, with the corresponding permutation null distributions
(violins; 5,000 permutations of the outcome, refitting **both** the reduced and the full
model on the same permuted outcome, so that the null is on the increment and not on the
total R²). Unit of observation: one subject; *n* = 85.
*Over four baseline behavioural scores (reduced R² = 0.185):* AMPA ΔR² = 0.0477,
*F*(1, 79) = 4.912, *P* = 0.030, permutation *P* = 0.050; GABA-A ΔR² = 0.0206,
*F*(1, 79) = 2.054, *P* = 0.156, permutation *P* = 0.196.
*Over baseline measured NP connectivity (reduced R² = 0.152):* AMPA ΔR² = 0.0502,
*F*(1, 82) = 5.151, *P* = 0.026, permutation *P* = 0.039; GABA-A ΔR² = 0.0426,
*F*(1, 82) = 4.335, *P* = 0.041, permutation *P* = 0.063.
The full model with baseline behaviour and the AMPA index explains R² = 0.233,
*F*(5, 79) = 4.800, *P* = 6.97 × 10⁻⁴. **The specificity of the AMPA index over the
GABA-A index is therefore only partial: it holds over baseline behaviour but not over
baseline connectivity.** Permutation *P* values are one-sided by construction. These are
four pre-specified nested-model tests reported **uncorrected**.

**h3–h6. The four bivariate relationships quoted in the main text.** Unit of observation:
one subject; *n* = 85; two-sided Pearson correlations with 95% CIs, uncorrected.
h3, AMPA index versus FU3 symptom change adjusted for baseline measured NP:
partial *r* = 0.243 (0.032–0.434), *P* = 0.025. h4, the same relationship unadjusted:
*r* = 0.264 (0.053–0.451), *P* = 0.015. h5, AMPA index versus baseline measured NP
connectivity: *r* = 0.105 (−0.111 to 0.311), *P* = 0.340. h6, AMPA index versus baseline
symptoms: *r* = −0.156 (−0.357 to 0.059), *P* = 0.153. Panels h5 and h6 are included to
show that the index is **not** explained by either baseline quantity.

**b_pattern, c_pattern (supplementary versions of b and c).** The same healthy cohort
regrouped by the Fig. 4 rule — increased under both drugs (*n* = 8) versus decreased under
either (*n* = 19) — rather than by *k*-means. **The change contrasts under this rule are
definitionally circular, because the grouping is the sign of the change being tested, and
are therefore plotted without *P* values.** Only the placebo-level contrast is
non-circular: both-up −0.315 ± 0.310 versus any-down +0.133 ± 0.499, Welch *t* = −2.827,
*P* = 0.010, Hedges' *g* = −0.987, Mann–Whitney *P* = 0.029 (two-sided, uncorrected).
Descriptive change values under this rule, given without inference: ketamine +0.586
versus −0.247; midazolam +0.718 versus −0.302.

**Source data:** `fig5_healthy_n27.csv`, `fig5_healthy_n27_with_pattern.csv`,
`fig5_healthy_pattern_rule_n27.csv`, `fig5_mdd_hc_n36.csv`, `fig5_panel_stats.csv`,
`fig5f_np_symptom_resid_MDD_n22.csv`, `fig5g_state_similarity_MDD_n22.csv`,
`fig5h_longitudinal_n85.csv`, `fig5h_added_variable_n85.csv`, `fig5h_increments.csv`,
`fig5h_increment_nulls.csv`, `fig5h_model_stats.csv`,
`fig5h_paragraph_scatters_n85.csv`, `fig5h_paragraph_scatter_stats.csv`,
`fig5_which_tests_are_reportable.csv` (a per-panel audit of which contrasts are circular
and which are reportable).

---

## Supplementary Figure S1 — Reproducibility of the assimilation procedure

**a.** The six reward-task NP edges from five independent assimilation runs of the same
healthy subject at the 100 M scale, plotted run by run. Unit of observation: one run ×
edge; *n* = 5 runs × 6 edges = 30 values. **b.** Edge-wise agreement between runs.
**c.** Between-edge (signal) versus between-run (noise) standard deviation.
Reliability of the edge profile across runs: ICC(3,1) = 0.9951 (two-way mixed, runs
fixed, single measurement) and ICC(2,1) = 0.9942 (two-way random, absolute agreement).
Mean between-run profile correlation *r* = 0.996 (range 0.990–0.998) across the 10 run
pairs. Between-edge s.d. 0.169 versus mean between-run s.d. 0.012, a signal-to-noise
ratio of **13.8-fold in s.d. and 189-fold in variance**. Descriptive reliability
analysis; no null-hypothesis test is performed. **Scope limitation: repeats exist only
for the MID edges and only for one subject, so this quantifies run-to-run stability of
the assimilation, not between-subject generalisability.** *Note for the authors: the
existing caption's "13-fold / 171-fold" should be updated to 13.8-fold / 189-fold.*

## Supplementary Figure S2 — Generalisation to held-out task trials

**a, b.** Trial-to-subject similarity matrices for the empirical BOLD and for the
simulated data. **c.** Identification margin per trial. Unit of observation: one held-out
trial; 4 subjects (HC03, HC04, AUD02, MDD02) × 6 emotional-face-task trials = 24 trials.
Identification accuracy: empirical 23/24 = 95.8% (the single error is
`AUD02_happy_trial4`); simulated, without re-assimilation, 24/24 = 100%. The
identification margin (self-similarity minus the best other-subject similarity) is
0.163 empirical versus 0.197 simulated; two-sided **paired** *t* test across the 24
trials (pairing on trial): *t* = 2.293, df = 23, *P* = 0.031. Single pre-specified
comparison, uncorrected. **Accuracy itself is not tested against chance, as 24 trials
from 4 subjects give too coarse a null; the margin test is the inferential result.**

## Supplementary Figure S3 — Robustness to the conductance setting

**a.** Group-level ΔNP at three AMPA settings (0.0040, 0.0044 original, 0.0048) and three
GABA-A settings (0.0035, 0.0040 original, 0.0045). Unit of observation: one subject;
*n* = 288, df = 287. Two-sided one-sample *t* tests against zero, all six significant:
AMPA 0.0040 mean +1.541 (95% CI 1.298–1.785), *d* = 0.731, *t* = 12.41,
*P* = 1.35 × 10⁻²⁸; AMPA 0.0044 +0.777 (0.669–0.885), *d* = 0.833, *t* = 14.14,
*P* = 8.43 × 10⁻³⁵; AMPA 0.0048 +1.361 (1.104–1.618), *d* = 0.612, *t* = 10.38,
*P* = 1.20 × 10⁻²¹; GABA-A 0.0035 +3.168 (2.919–3.417), *d* = 1.470, *t* = 24.94,
*P* = 8.09 × 10⁻⁷⁴; GABA-A 0.0040 +2.735 (2.538–2.933), *d* = 1.597, *t* = 27.11,
*P* = 4.04 × 10⁻⁸¹; GABA-A 0.0045 +2.778 (2.529–3.027), *d* = 1.290, *t* = 21.89,
*P* = 3.70 × 10⁻⁶³. Error bars are 95% CIs on the mean. Reported uncorrected; all six
would survive any correction.
**b.** Proportion of responders by diagnostic group at each setting; unit of observation:
one subject; *n* = 288 (69 / 89 / 130). χ² test of independence across the three groups,
2 df, one test per setting, uncorrected. **Responder stratification by group holds only
on the AMPA side:** AMPA 0.0040 HC 78.3% / high-symptom 79.8% / patient 93.1%,
χ² = 11.23, *P* = 3.64 × 10⁻³; AMPA 0.0044 75.4 / 70.8 / 91.5%, χ² = 17.00,
*P* = 2.04 × 10⁻⁴; AMPA 0.0048 69.6 / 61.8 / 87.7%, χ² = 20.70, *P* = 3.19 × 10⁻⁵. The
GABA-A side is at ceiling (94–99% responders in every group) and shows no group
difference: χ² = 1.654, *P* = 0.437; χ² = 0.659, *P* = 0.719; and *P* = 0.50 at the
strongest setting.
**c.** Consistency of the individual response across settings. Two-sided Pearson and
Spearman correlations, *n* = 288, uncorrected. Within-knob agreement is substantial —
AMPA pairs *r* = 0.394–0.549 (all *P* < 4 × 10⁻¹²), GABA-A pairs *r* = 0.695–0.903 (all
*P* < 10⁻⁴²) — whereas across-knob agreement is weak (*r* = −0.051 to 0.305). **An
individual's response magnitude is therefore reproducible within a perturbation type but
does not transfer between AMPA and GABA-A.**

## Supplementary Figure S4 — Bidirectionality in the emotional face task

**a, b, c.** Baseline and post-perturbation connectivity in the emotional
face-evaluation (EFT) network and in the 12-edge NP profile, for three individual twins
(HC01, MDD, AUD; HC02 was excluded at the authors' request). Unit of observation: one
subject; *n* = 3. **Descriptive only — no statistical test is performed or appropriate at
*n* = 3, and no error bar is defined for a single simulation per subject per condition.**
EFT network, AMPA: HC01 −0.656, MDD +1.071, AUD +0.858 (two up, one down). EFT network,
GABA-A: all three increase (+1.972, +0.633, +0.857). On the 12-edge NP profile the same
three twins split two up / one down under **both** perturbations, with HC01 the decreaser
in each case. Bidirectionality in the EFT network is therefore observed under AMPA only.

## Supplementary Figure S5 — Head motion

Unit of observation: one subject; *n* = 288 (HC 69, high-symptom 89, patient 130). Motion
is summarised as mean framewise displacement (FD, mm).
**a. Motion by group.** HC 0.128 ± 0.049 mm (median 0.120), high-symptom
0.142 ± 0.070 (0.129), patient 0.138 ± 0.076 (0.109). One-way ANOVA *F*(2, 285) = 0.844,
*P* = 0.431; Kruskal–Wallis χ²(2) = 2.276, *P* = 0.320; Levene's test of equal variances
*F*(2, 285) = 1.671, *P* = 0.190; HC versus all others Welch *t* = −1.478, *P* = 0.141,
Cohen's *d* = −0.17, Mann–Whitney *P* = 0.772. All two-sided, uncorrected. **Motion does
not differ across diagnostic groups.**
**b. Motion versus the NP measures.** Six two-sided Pearson correlations between FD and
the six NP quantities, corrected by **Bonferroni across the six measures** (α/6 =
0.00833; FDR is not reported). Measured NP factor *r* = 0.155 (95% CI 0.041–0.266),
*P* = 8.24 × 10⁻³, *P*_Bonferroni = 0.049; simulated NP *r* = 0.127 (0.012–0.240),
*P* = 0.031, *P*_Bonf = 0.184; after AMPA *r* = 0.149 (0.034–0.260), *P* = 0.011,
*P*_Bonf = 0.067; after GABA-A *r* = 0.268 (0.157–0.372), *P* = 4.1 × 10⁻⁶,
*P*_Bonf < 0.001; ΔNP (AMPA) *r* = −0.035 (−0.150 to 0.081), *P* = 0.554,
*P*_Bonf = 1.000; ΔNP (GABA-A) *r* = 0.204 (0.090–0.312), *P* = 5.05 × 10⁻⁴,
*P*_Bonf = 0.003. **ΔNP after AMPA — the quantity behind the main inferences — is the one
measure with no motion association at all**, whereas the measured NP factor is weakly but
detectably motion-associated (*P*_Bonf = 0.049, i.e. only just below threshold; the
conclusion is sensitive to the definition of the correction family and this should be
stated). *Correction for the authors: the manuscript sentence "mean framewise
displacement did not differ across diagnostic groups and was not associated with either
NP scores or perturbation-induced changes" is only half true in the corrected data — the
group half holds, the association half does not.*
**c. Per-edge motion correlations.** Twelve two-sided Pearson correlations between FD and
each measured NP edge, *n* = 288, Bonferroni-corrected across the 12 edges. **No edge is
motion-related:** |*r*| ≤ 0.104, smallest raw *P* = 0.078 (edge 12), smallest
*P*_Bonferroni = 0.939. Only the 12-edge sum reaches significance, and only marginally
(panel b).
**d. Group effect with and without motion adjustment.** Partial η² of the group term in a
one-way model and in the same model with FD added as a covariate, for the six NP
measures; *n* = 288, df = (2, 285) without FD and (2, 284) with FD. Measured NP
6.04 → 6.78%; simulated NP 9.23 → 9.27%; after AMPA 1.48 → 1.54%; after GABA-A
0.88 → 0.77%; ΔNP (AMPA) 5.08 → 5.06%; ΔNP (GABA-A) 0.62 → 0.61%. **Maximum shift
0.74 percentage points and no change in which effects are significant**, so adjusting for
motion does not alter the group effects. *P* values are Bonferroni-corrected across the
six measures and are given in `TableS26_group_effect_motion_adjustment_corrected_n288.csv`.

## Supplementary Figure S6 — A depression-specific network

Unit of observation: one subject; *n* = 141 (HC 69, MDD 72); 27 edges.
**a1–a4. Group difference under four conditions.** Two-sided independent *t* tests with
adjustment for covariates, df = 136, uncorrected across the four pre-specified
conditions. Measured: HC 1.299 ± 1.821 versus MDD 0.089 ± 1.108, adjusted difference
1.252 (95% CI 0.755–1.748), *t* = −4.983, *P* = 1.87 × 10⁻⁶, unadjusted Cohen's
*d* = 0.807 (0.464–1.150). Simulated baseline: 0.742 ± 1.563 versus −0.257 ± 0.856,
adjusted difference 1.089 (0.669–1.510), *t* = −5.127, *P* = 9.93 × 10⁻⁷, *d* = 0.797.
After AMPA: 0.679 ± 0.763 versus 0.506 ± 0.795, adjusted difference 0.127 (−0.132 to
0.386), *t* = −0.967, *P* = 0.335, *d* = 0.222 — **the group difference is abolished**.
After GABA-A: 3.796 ± 2.436 versus 2.442 ± 2.740, adjusted difference 1.247 (0.361–2.134),
*t* = −2.782, *P* = 6.17 × 10⁻³, *d* = 0.522 — **the group difference persists**.
**b, c, d. Within-subject perturbation effects.** Two-sided **paired** *t* tests
(pairing on subject), *n* = 141. Simulated versus AMPA: mean change +0.359 ± 1.404,
94/141 (66.7%) increased, *t* = 3.035, df = 140, *P* = 2.87 × 10⁻³; with covariate
adjustment *t* = 2.339, df = 137, *P* = 0.021. Simulated versus GABA-A: +2.873 ± 2.639,
124/141 (87.9%) increased, *t* = 12.93, df = 140, *P* = 1.21 × 10⁻²⁵; adjusted
*t* = 5.235, df = 137, *P* = 6.05 × 10⁻⁷. Both perturbations raise depression-network
connectivity, but only AMPA removes the diagnostic difference.

## Supplementary Figure S7 — Whole-brain extent of the perturbation effects

Unit of observation: one subject; *n* = 288; 23,436 upper-triangular edges among 217
nodes, in each of four task conditions.
**a. Extent of significant modulation.** Number and percentage of edges with a
significant paired change, by contrast and condition. Two-sided paired *t* tests, one per
edge, df = 287, corrected across the 23,436 edges by Benjamini–Hochberg FDR. AMPA versus
baseline: 69.5–83.2% of edges significant depending on condition; AMPA + GABA-A versus
baseline: 82.8–89.7%; the incremental GABA-A contrast: 72.2–89.6%.
**b. Effect-size distribution.** Distribution of |*d*z| over the significant edges. The
median |*d*z| is 0.315–0.402 for AMPA versus baseline and 0.454–0.592 for
AMPA + GABA-A versus baseline; only 15.9–31.2% of edges exceed |*d*z| = 0.5 under AMPA.
**The very large number of significant edges reflects statistical power at *n* = 288, not
a large per-edge effect**, and an effect-size floor should be applied before the extent is
described in words.
**c. Network-pair summary.** Signed percentage of significantly changed edges per
canonical network pair. Descriptive; the per-pair counts are tabulated in
`SuppTable_WB_network_pair_summary_n288.csv` (540 rows: 4 conditions × 3 contrasts ×
45 network pairs).

## Supplementary Figure S8 — Edge-level direction of the perturbation response (1 B build)

Unit of observation: one subject; *n* = 12 twins; 12 NP edges. Concordance between the
sign of each subject's edge-level change and the sign of the group-level change, tested
against the chance expectation of 6 of 12 edges with a two-sided one-sample *t* test,
df = 11, with the Wilcoxon signed-rank test as a check; two comparisons, uncorrected.
AMPA: group mean ΔNP +0.368, 6 of 12 edges change in the group-level direction, mean
7.33 ± 0.98 concordant edges per subject (61.1%), *t* = 4.690, *P* = 7 × 10⁻⁴, Wilcoxon
*P* = 3.9 × 10⁻³. GABA-A: group mean +0.271, 7 of 12 edges, mean 8.25 ± 1.60 concordant
edges (68.8%), *t* = 4.864, *P* = 5 × 10⁻⁴, Wilcoxon *P* = 1.0 × 10⁻³. The largest single
edge accounts for only 21.6% (AMPA) and 22.0% (GABA-A) of a subject's total absolute
change, and a median of 3.4 and 3.1 edges respectively are required to account for half
of it, i.e. **the response is distributed across the profile rather than driven by one
edge.**

---

## Items requiring author input before submission

1. **Fig. 2a** — permutation *P* values and permutation count for each CPM cell are not in
   the source table and must be supplied from the original analysis.
2. **Fig. 5d** — the panel title "opposite response direction" is supported only by the
   between-group test; neither group differs from zero individually.
3. **Supplementary Fig. S1** — update the existing caption's "13-fold / 171-fold" to
   13.8-fold / 189-fold.
4. **Supplementary Fig. S5** — the manuscript sentence about motion must be rewritten; the
   "not associated with NP scores" half does not hold in the corrected data.
5. **Fig. 5h2** — the previously reported permutation *P* = 0.0006 was computed on the
   full model's total R², not on the increment; the correct increment permutation *P* is
   0.050.
6. **Fig. 3g** — the new 3 M run removes the group-level AMPA effect in the regional
   build (+0.97, *P* = 0.0012 → −0.02, *P* = 0.95) and reduces the GABA-A effect
   (+3.15 → +1.13). Every main-text and SI sentence built on the old 3 M perturbation
   numbers needs rewriting.
7. **Figure numbering** — Fig. 5's longitudinal panel is now h1/h2 with h3–h6 as
   supplementary; all in-text references need renumbering.
