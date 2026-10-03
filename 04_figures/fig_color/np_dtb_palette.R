# NP-DTB manuscript colour tokens (Woo-lab derived).

np_pal <- c(
  exc_ampa = "#FB6A4A",
  exc_ketamine = "#A50F15",
  exc_restore = "#FCAE91",
  exc_similarity = "#FDD9C8",
  inh_gaba = "#47C0E1",
  inh_midazolam = "#1A7A96",
  inh_restore = "#A9DEEE",
  unp_baseline = "#757575",
  unp_placebo = "#C5D0D2",
  unp_null = "#F4F4F4",
  circ_neg29 = "#FAC66D",
  circ_np12 = "#C99A46",
  circ_mid6 = "#9A6F20",
  circ_nonnp = "#E3DAC1",
  pos_prof34 = "#819D98",
  alt_mdd_net = "#A58B77",
  alt_wholebrain = "#DDBFAA",
  hlth_hc = "#99B77C",
  hlth_norm = "#C9E7AB",
  clin_highsymp = "#E9D5FF",
  clin_aud = "#CAADEF",
  clin_patients = "#A98DCD",
  clin_mdd = "#8A6BB1",
  bench_sar = "#B7AA82",
  bench_rww = "#5F5434",
  scale_3m = "#E2E2E2",
  scale_10m = "#B8B8B8",
  scale_100m = "#8C8C8C",
  scale_1b = "#585858",
  scale_5b = "#262626",
  coh_imagen = "#475666",
  coh_imagen_fu3 = "#7F98AD",
  coh_stratify = "#5981A1",
  coh_pharm_hv = "#A2BACD",
  coh_pharm_clin = "#D5EEFE",
  task_mid = "#856A4F",
  task_sst = "#637B89",
  task_eft = "#96B59D",
  sym_int = "#80435E",
  sym_ext = "#B67F49"
)

np_scale_ramp <- unname(np_pal[c("scale_3m","scale_10m","scale_100m","scale_1b","scale_5b")])
np_nesting    <- unname(np_pal[c("circ_neg29","circ_np12","circ_mid6")])
np_severity   <- unname(np_pal[c("clin_highsymp","clin_aud","clin_patients","clin_mdd")])
np_hot  <- c("#FFF2CC", "#FFCC00", "#FF6600", "#FF0000", "#A50F15")
np_cold <- c("#E3F5FB", "#55A8FF", "#47C0E1", "#209ABA", "#0B5E8C")
np_fc   <- c("#2F4F4A", "#819D98", "#D5E0DC", "#F4F2EE", "#FAE3B0", "#C99A46", "#6E4A00")

# usage: scale_fill_manual(values = np_pal[c("unp_baseline","exc_ampa","inh_gaba")])
