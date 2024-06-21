
import pandas as pd
import os
# this function get the % change for any column by year and specified


def load_data_Areas():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "areaXclasse_CAATINGA_Col80.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), 
                                index_col=False) # , low_memory=False
    # print("=================================")
    print(dfAggBacia.columns)
    print(dfAggBacia.head())
    # dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    # dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)

    return dfAggBacia


dfAr = load_data_Areas()

print("table areas ", dfAr.shape)
print("colunas da tabela ", dfAr.columns)
print("list of models ", dfAr['Colacao'].unique())
# print("list of version ", dfAr['version'].unique())

print(dfAr[dfAr['Colacao'] == 'Col71'].shape)
print("coleção 7 = temos years ", len(dfAr[dfAr['Colacao'] == 'Col71']['year'].unique()))
print(dfAr[dfAr['Colacao'] == 'Col80'].shape)
print("coleção 8 temos years ", len(dfAr[dfAr['Colacao'] == 'Col80']['year'].unique()))
print(dfAr[dfAr['Colacao'] == 'Col80']['year'].unique())