import os
import pandas as pd



def load_data_Acc():

    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "regMetricsAccGlobalCol9.csv"        
    dfAccYY = pd.read_csv(os.path.join(base_path, nameTablesGlob))

    colInts = [kk for kk in dfAccYY.columns]
    print("colunas listadas \n   ==> ",colInts)
    colInts.remove('Unnamed: 0')
    dfAccYY = dfAccYY[colInts]
    print(dfAccYY['Models'].unique())
    print("dfAccYY ", dfAccYY.head())
    return dfAccYY


modelos = ['RF', 'GTB']
vers = ['5']
nameBacias = [
      '741', '7421','7422','744','745','746','751','752',  
      '753', '754','755','756','757','758','759','7621','7622','763',
      '764','765','766','767','771','772','773', '7741','7742','775',
      '776','76111','76116','7612','7613','7614','7615',  
      '7616','7617','7618','7619'
]
allBasin = nameBacias + ['7492','777','778']
nameBacias = [int(kk) for kk in nameBacias]
lstYear =  [kk for kk in range(1985, 2023)]

dataAcc = load_data_Acc()

print(dataAcc.head(6))
