
import pandas as pd
import os
# this function get the % change for any column by year and specified


def load_data_Areas():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "areaXclasse_CAATINGA_Col9.0.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print("=================================")
    dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)

    return dfAggBacia


dfAr = load_data_Areas()

print("table areas ", dfAr.shape)
print("colunas da tabela ", dfAr.columns)
print("list of models ", dfAr['Models'].unique())
print("list of version ", dfAr['version'].unique())