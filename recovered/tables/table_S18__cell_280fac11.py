# Verbatim archive of an interactive execution-log cell. Nothing removed, nothing reformatted.
# table            : table_S18
# cell id          : 280fac11-f90a-44c7-87d6-4d75ed1b1c0e
# frame id         : b194cd74-5255-435a-9c1e-206638f9adae
# timestamp        : 2026-09-29 10:12:04 UTC (epoch-ms 1790676724668)
# conda env        : python
# produced         : loads fig4_subject_level_n288.csv as the Table S18 input
# ----------------------------------------------------------------------------


F4='/Users/yunman/Desktop/submission/revision/Code/reproducibility_package/04_figures/fig.4/fig4_data/'
d=pd.read_csv(F4+'fig4_subject_level_n288.csv')
print(d.shape, list(d.columns))
print(d.head(4).to_string())
print('\nsite values:', d.site.value_counts().to_dict())
print('sex values:', d.sex.value_counts().to_dict())
print('\nfiles in fig4_data with grouping:', [os.path.basename(p) for p in glob.glob(F4+'*group*')])
