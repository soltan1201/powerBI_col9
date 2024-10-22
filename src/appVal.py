
import os
from math import floor
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
# import altair as alt
import ipywidgets
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

classes = [3,4,12,15,18,21,22,29,33] # 
columnsInt = [
    'Forest Formation', 'Savanna Formation', 'Grassland', 'Pasture',
    'Agriculture', 'Mosaic of Uses', 'Non vegetated area', 'Rocky Outcrop', 'Water'
] # 
colors = [ 
    "#1f8d49", "#7dc975", "#d6bc74", "#edde8e", "#f5b3c8", 
    "#ffefc3", "#db4d4f",  "#FF8C00", "#0000FF"
] # 
# bacia_sel = '741'

dict_class = {
    '3': 'Forest Formation', 
    '4': 'Savanna Formation', 
    '12': 'Grassland', 
    '15': 'Pasture', 
    '18': 'Agriculture', 
    '21': 'Mosaic of Uses', 
    '22': 'Non vegetated area', 
    '29': 'Rocky Outcrop', 
    '33': 'Water'
}
dict_cobertura = {
    'Forest Formation': 3, 
    'Savanna Formation': 4, 
    'Grassland': 12, 
    'Pasture': 15, 
    'Agriculture': 18, 
    'Mosaic of Uses': 21, 
    'Non vegetated area': 22, 
    'Rocky Outcrop': 29, 
    'Water': 33
}
dict_classNat = {
    '3': 'Natural', 
    '4': 'Natural', 
    '12': 'Natural', 
    '15': 'Antrópico', 
    '18': 'Antrópico', 
    '21': 'Antrópico', 
    '22': 'Antrópico', 
    '29': 'Natural', 
    '33': 'Natural'
}
dict_ColorNat = {
    'Natural': '#32a65e',
    'Antrópico': '#FFFFB2',
}
dict_colors = {
    '3':  '#1f8d49', 
    '4':  '#7dc975', 
    '12': '#d6bc74', 
    '15': '#edde8e', 
    '18': '#f5b3c8', 
    '21': '#ffefc3', 
    '22': '#db4d4f', 
    '29': '#FF8C00', 
    '33': '#0000FF',
    'Forest Formation':  '#1f8d49', 
    'Savanna Formation':  '#7dc975', 
    'Grassland': '#d6bc74', 
    'Pasture': '#edde8e', 
    'Agriculture': '#f5b3c8', 
    'Mosaic of Uses': '#ffefc3', 
    'Non vegetated area': '#db4d4f', 
    'Rocky Outcrop': '#FF8C00', 
    'Water': '#0000FF',
}
dict_code_colors = {}
for ii, cclass in enumerate(classes):
    dict_code_colors[str(cclass)] = colors[ii]

dict_colors['Natural'] = '#32a65e'
dict_colors['Antrópico'] = '#FFFFB2'
dict_colors['cobertura'] = '#FFFFFF'



def get_chart_Plot_plotlyX(dfAccur, nbacia= 741, nModel= "RF", vers= '5'):
    # colunas = ["Accuracy","Accuracy_Bal","Precision","ReCall", "F1-Score","Jaccard"]
    colunas = ["Accuracy","Precision","ReCall","Jaccard"]
    # print("bacia = ", nbacia)
    dfTemp = dfAccur[
                (dfAccur["Bacia"] == nbacia) & 
                (dfAccur["Models"] == nModel) &
                (dfAccur["Version"] == str(vers))
            ]
    # print(dfTemp.head())
    fig = px.line(dfTemp, 
                x="Years", y=colunas,
                hover_data="Years",
                title=  f'Accuracy metrics of basin 🌵 {nbacia} 🌵 with model {nModel} '.upper(),
                template="plotly_dark",
            )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y"
    )
    # fig.show()
    fig.update_layout(
        width= 800,
        height = 450
    )
    fig.layout.autosize = True
    return fig

def get_plotBar_Acc_Disaggrements(dfAccur, nbacia= 741, nModel= "RF", vers= '5'):
    dfTemp = dfAccur[
                (dfAccur["Bacia"] == nbacia) & 
                (dfAccur["Models"] == nModel) &
                (dfAccur["Version"] == str(vers))
            ]
    
    lstCol = ["global_accuracy","quantity diss","alloc dis",]
    dictNameAgg = {
        "global_accuracy": 'Accuracia Media',
        "quantity diss": 'Discordância de alocação',
        "alloc dis": 'Discordância de quantidade'
    }
    dictColorAgg = {
        "global_accuracy": '#1b830d',
        "quantity diss": '#ffe454',
        "alloc dis": '#f93a39'
    }
    dictsignoAgg = {
        "global_accuracy": 1,
        "quantity diss": -1,
        "alloc dis": -1
    }

    figAgg = go.Figure()
    for ncol in lstCol:
        figAgg.add_trace(go.Bar(
            x= dfTemp['Years'],
            y= dfTemp[ncol] * dictsignoAgg[ncol], # 
            name= dictNameAgg[ncol],
            # orientation='h',
            marker_color= dictColorAgg[ncol],
            # text=[f'{kk}%' for kk in dfAgropercent[dfAgropercent['classe_Agro'] == nclase]['percent'].tolist()]
        ))
    nheight = 550
    nwidth = 850
    figAgg.update_layout(
        title_text='Histórico de Accuracia e Discordâncias',
        title_font_size= 28,
        barmode='relative',
        height= nheight,
        width= nwidth,
        xaxis=dict(
            title="Anos",
            tickangle=0,
            tickfont=dict(size=12),

        ),
        yaxis=dict(
            title="Porcentagem",
            tickfont=dict(size=12),
            showticklabels=True
        ),
        font= dict(size=20),
        legend= dict(orientation="h", x= 0.02,  y=-0.10)
    )
    
    return figAgg

def plotPieYear(dfAccur, nbacia= 741, nModel= "RF", vers= '5', yyear= 1985):
    
    dfTemp = dfAccur[
                (dfAccur["Bacia"] == nbacia) & 
                (dfAccur["Models"] == nModel) &
                (dfAccur["version"] == str(vers)) &
                (dfAccur["year"] == yyear)
            ]
    # print("mostrar os dados \n ", dfTemp.head(2))

    trace1 = go.Pie(
                values = dfTemp['area'],
                labels = dfTemp['classe'],
                hole= 0.7,
                # sort= False,
                direction='clockwise',
                textinfo= 'percent',
                textposition='inside',
                marker=dict(colors=dfTemp["cob_color"],
                              line=dict(color='#FFFFFF', width=1)),
                showlegend= False,
                # title= "Cobertura " + str(yyear)
               )
    fig2pie = go.FigureWidget(data=[trace1])          
    fig2pie.update_layout(
                    # title_font=dict(size=30),
                    autosize=True,
                    width=400,
                    height=400,
                    annotations=[dict(text=str(yyear), x=0.495, y=0.5, font_size=28, showarrow=False)]
                )

    return fig2pie


def buildingPlots_Cruzando_Class(dfAccur, nbacia= 741, nModel= "RF", vers= '5', lstclass= [3,4,12], myHeight= 510):

    tipoclase = "Natural"
    if 15 in lstclass:
        tipoclase= "Antrôpica"

    dfTemp = dfAccur[
                (dfAccur["Bacia"] == nbacia) & 
                (dfAccur["Models"] == nModel) &
                (dfAccur["version"] == str(vers))            
            ]
    
    figPlotCr = make_subplots(rows= 1, cols= 1)
    for cc, nclase in enumerate(lstclass):        
        # print(colors[cc], nclase)          
        figPlotCr.add_trace(
                go.Scatter(
                    x= dfTemp[dfTemp['classe'] == nclase]['year'], 
                    y= dfTemp[dfTemp['classe'] == nclase]['area'], 
                    marker_color= dict_colors[dict_class[str(nclase)]],
                    marker_symbol= 'star-open',
                    stackgroup='one',
                    name= dict_class[str(nclase)] 
                ),
                row= 1, col= 1
            )
        figPlotCr.update_xaxes(title_text= dict_class[str(nclase)], row= 1, col= 1)

        # dictPmtros['yaxis'] = dictPmtrosPlot

    # figPlotCr.update_layout(dictPmtros)
    figPlotCr.update_layout(
            height= myHeight, 
            width= 460, 
            title=dict(
                text=" Áreas de classes " + tipoclase, 
                font=dict(
                    size=20,
                    family="Courier New",
                ), 
                automargin=True, 
                yref='paper'
            ), 
            showlegend=True,
            legend= dict(
                        orientation="h", 
                        x= 0.01,  
                        y= -0.15, 
                        font=dict(
                            family="Courier New",
                            size=14,
                            color="white"
                        ),
                        # bgcolor = 'white'                    
                    ),
        )

    return figPlotCr

def buildingPlotErros(dfTemp):
    lstCC = [3, 4,12,21,22,33]
    total = dfTemp.iloc[:]

class getYearClassfromMC(object):
    dfCMgfpComision = None
    dfCMgfpOmision = None
    def __init__(self, dfCMgftmp):
        self.dfCMgftmp = dfCMgftmp.sort_index()
        self.dfCMgfpercent = None
        self.colunasClass = ['classes', '3', '4', '12', '21', '22', '33'] # '15', '18',
        # print("tabela dentro da classe")
        # print(self.dfCMgftmp.head())

    def changeAllCount_in_percentComission(self, row):
        nClass = row['classes']
        yyear = row['year']
        countTotal = row['Total']

        if nClass != 'Total':
            for col in self.colunasClass[1:] + ['Total']:            
                row[col] = round(row[col] / countTotal, 2) 
                if col != nClass:
                    row[col] = -1 * row[col]               
        return row

    def changeAllCount_in_percentOmission(self, row):
        nClass = row['classes']
        yyear = row['year']
        dfCMgftmpYY = self.dfCMgftmp[self.dfCMgftmp['year'] == yyear]
        # dfCMgftmpYY = dfCMgftmpYY.sort_values(by= ['classes'])
        if yyear == 1985:
            print("show table Matrix confution \n", dfCMgftmpYY.head(8) )
        # get the value of total by confusion matrix
        # valTotal = self.dfCMgftmp[(self.dfCMgftmp['year'] == yyear) & (self.dfCMgftmp['classes'] == 'Total')]['Total'].iloc[0]
        # print(f" class {nClass} | year {yyear} | valor Total {valTotal}")
        if nClass != 'Total':
            for col in self.colunasClass[1:] + ['Total']:
                valTotal = dfCMgftmpYY[dfCMgftmpYY['classes'] == 'Total'][col].iloc[0]
                row[col] = round(row[col] / valTotal, 2)
                if col != nClass:
                    row[col] = -1 * row[col]
        return row

    def makeCMpercent(self):
        self.dfCMgfpComision = self.dfCMgftmp.apply(self.changeAllCount_in_percentComission, axis= 1)
        self.dfCMgfpOmision = self.dfCMgftmp.apply(self.changeAllCount_in_percentOmission, axis= 1)
    
    # def get_matriz_Comission(self, row):
    #     nClass = row['classes']
    #     # print("classe ", nClass)
    #     if nClass not in ['Total']:
    #         pos = self.colunasClass[1:].index(nClass)
    #         for cc, col in enumerate(self.colunasClass[1:]):
    #             if cc < pos:
    #                 row[col] = 0
    #     return row

    # def get_matriz_Omission(self, row):
    #     nClass = row['classes']
    #     # print("classe ", nClass)
    #     if nClass not in ['Total']:
    #         pos = self.colunasClass[1:].index(nClass)
    #         for cc, col in enumerate(self.colunasClass[1:]):
    #             if cc > pos:
    #                 row[col] = 0
    #     return row

    # def getdataframeCommision(self):
    #     dfmatrixConfComision = self.dfCMgfpercent.apply(self.get_matriz_Comission, axis= 1)
    #     dfmatrixConfComision = dfmatrixConfComision.sort_index()
    #     return dfmatrixConfComision

    # def getdataframeOmmision(self):
    #     dfmatrixConfOmision = self.dfCMgfpercent.apply(self.get_matriz_Omission, axis= 1)
    #     dfmatrixConfOmision = dfmatrixConfOmision.sort_index()
    #     return dfmatrixConfOmision

def plot_graficos_erros_acc_ProdUser(dfErros, tipoErro, showLegend):
    colunasClass = ['3', '4', '12', '21', '22', '33']
    print("vendo a seleção por fila \n ")
    dfErros['classes'] = dfErros['classes'].astype(int)
    dfErros = dfErros.sort_values(by= ['classes'])
    print(dfErros[dfErros['classes'] == 4][colunasClass].to_numpy()[0])
    nHeight = 400
    figErro = go.Figure()
    for cc,colCC in enumerate(colunasClass):
        # print("show class ", colCC)
        figErro.add_trace(
            go.Bar(
                y= [dict_class[str(kk)] for kk in dfErros['classes'].to_list()],  # by= ['classe']
                x= dfErros[dfErros['classes'] == int(colCC)][colunasClass].to_numpy()[0],
                orientation='h',
                name= dict_class[colCC],
                marker= {'color': dict_code_colors[colCC]},
                customdata=dfErros[colCC],
                hovertemplate = "Class: %{y}<br>Erro:%{customdata}%<br><br><extra></extra>"
            )
        )
    if showLegend:
        nHeight = 440
    figErro.update_layout(
        title= {
            'text': tipoErro,
            'font': dict(size=16),
            'yref': 'paper',
            'x': 0.2,
            # 'y': 0.98
        },
        barmode='relative',
        height=nHeight,
        width= 500,
        yaxis_autorange='reversed',
        bargap=0.01,
        showlegend=showLegend,
        legend= dict(
                    orientation="h",
                    x= 0.10,
                    y= -0.15,
                    font=dict(
                        family="Courier",
                        size=12,
                        color="white"
                    ),
                ),
    )
    figErro.update_xaxes(range=[-1,1])
    if showLegend:
        figErro.update_yaxes(title='', visible=False, showticklabels=True)
    # fig.update_yaxes(ticktext = [dict_class[kk] for kk in colunasClass])
    return figErro

def getValuesMaxMin(dftemporal):
    colunasClass = ['3', '4', '12', '21','22', '33'] #  '15', '18',
    maximo = np.max(dftemporal[colunasClass].to_numpy())
    minimo = np.min(dftemporal[colunasClass].to_numpy())
    return maximo, minimo


def plotMultipleCoberturas(df_Areatmp):
    coluna = 3
    dictPmtros = {
            'height': 800,
            'width': 800,
            'template':'plotly_white'
        }
    nRowplot = int(len(lstclass) / coluna) + 1
    figPlotC = make_subplots(rows= nRowplot, cols= coluna)

    for cc, nclase in enumerate(lstclass):
        kcol = cc % coluna
        krow = int(cc / coluna)
        # print(cc, krow, kcol)
        # print(colors[cc], nclase)

        figPlotC.add_trace(
                go.Scatter(
                    x= df_Areatmp[df_Areatmp['classe'] == nclase]['year'],
                    y= df_Areatmp[df_Areatmp['classe'] == nclase]['area'],
                    marker_color= colors[cc],
                    marker_symbol= 'star-open',
                    fill='tonexty',
                    name= dict_class[str(nclase)]
                ),
                row=krow + 1, col= kcol + 1
            )
        figPlotC.update_xaxes(title_text=dict_class[str(nclase)], row= krow + 1, col= kcol + 1)
        if cc < 1:
            mkey = 'yaxis'
        else:
            mkey = 'yaxis' + str(cc + 1)
        # dictPmtros[mkey] = dictPmtrosPlot[str(nclase)]

    figPlotC.update_layout(dictPmtros)
    figPlotC.update_layout(
                height=800,
                width=1600,
                # title_text= "bacia ",
                showlegend= True,
                legend= dict(
                            orientation="h",
                            x= 0.01,
                            y= -0.05,
                            font=dict(
                                family="Courier",
                                size=24,
                                color="black"
                            ),
                            # yanchor="bottom"
                        ),
            )

    figPlotC.show()
    

def plot_graficoAccuracyErrobyClass(dfErrosClass, typeErro):
    colunasClass = ['3', '4', '12', '21','22', '33'] #  '15', '18', 
    # print("matriz erroi \n ", dfErrosClass)
    valmax, valmin = getValuesMaxMin(dfErrosClass)
    print(f"minimum and maximum values {valmin} e {valmax}")
    figQ = make_subplots(rows= 1, cols= 1)
    for cc, nclase in enumerate(colunasClass):
        figQ.add_trace(
                go.Bar(
                    x= dfErrosClass['year'].astype(dtype=str),
                    y= dfErrosClass[nclase],
                    marker_color= dict_code_colors[str(nclase)],
                    name= dict_class[str(nclase)],
                    customdata= [dict_class[str(nclase)]] * dfErrosClass[nclase].shape[0],
                    hovertemplate = "Class: <b>%{customdata}</b><br>Year: <b>%{x}</b><br>Erro Class: <b>%{y}</b><br><extra></extra>"
                ),
                row= 1, col= 1
            )
        figQ.update_xaxes(title_text= dict_class[str(nclase)], row= 1, col= 1)

    figQ.update_layout(
                barmode='relative',
                height=600,
                width=850,
                title_text=f"Percent of Accuracy | Erros {typeErro}" ,
                showlegend=True,
                legend= dict(
                            orientation="h",
                            x= 0.0,
                            y= -0.15,
                            font=dict(
                                family="Courier",
                                size=14,
                                color="white"
                            ),
                            # yanchor="bottom"
                        ),
        )
    figQ.update_yaxes(
            title=f'Percent Erro {typeErro}/Accuracy', 
            visible=True, 
            showticklabels=True,
            range=[valmin - 0.05, valmax + 0.05 ]
            )
    figQ.update_xaxes(title='Years', visible=True, showticklabels=True)
    return figQ


def get_interval_to_plot(df_Cobert, lstColunas):
    pmtroDict = {}
    colunasClass = ['3', '4', '12', '21', '22', '29', '33']
    for cobert in colunasClass:
        maxVal = df_Cobert[cobert].max()
        minVal = df_Cobert[cobert].min()
        amp = maxVal - minVal
        intervalo = int(amp / 5)
        ampDown = minVal * 0.35
        ampUp = maxVal * 0.20

        # print("cobertura=> ", cobert, " | Min ", minVal ,  ' | max ', maxVal, ' | Amp ', amp, " | interval ", intervalo)
        maxVal += ampUp
        if ampDown > 0:
            minVal -= ampDown
        else:
            minVal += ampDown
        amp = maxVal - minVal
        intervalo = int(amp / 5)
        # print(" ----> cobertura=> ", cobert, " | Min ", minVal ,  ' | max ', maxVal, ' | Amp ', amp, " | interval ", intervalo)
        dict_temp = {'range': [minVal, maxVal], 'dtick': intervalo,}
        pmtroDict[cobert] = dict_temp

    return pmtroDict

def plot_graficoSeparateCover(df_AreaPlot, dfAreasCol8, dfAreasCol7, nbacia= 741, nModel= "RF", vers= '5'):
    dictPmtros = {
        'height': 1200,
        'width': 800,
        'template':'plotly_white'
    }    
    dfTempCol9 = df_AreaPlot[
                (df_AreaPlot["Bacia"] == nbacia) & 
                (df_AreaPlot["Models"] == nModel) &
                (df_AreaPlot["version"] == str(vers))            
            ]
    dfTempCol8 = dfAreasCol8[dfAreasCol8["Bacia"] == nbacia ]
    dfTempCol7 = dfAreasCol7[dfAreasCol7["Bacia"] == nbacia ]
    
    # print(f"dados {nbacia} -- {nModel} --- {vers}")
    # print("table Col9 \n", dfTempCol9.head())
    # print("table Col8 \n", dfTempCol8.head())
    # print("table Col71 \n", dfTempCol7.head())

    listClass = [3, 4, 12, 21, 22, 29, 33]
    figPlotCov = make_subplots(rows= 4, cols= 2)
    for cc, nclase in enumerate(listClass):        
        krow = floor(cc/ 2)
        kcol = cc % 2        
        print('index ', cc, " classe = ", nclase, " color = ", dict_colors[str(nclase)])
        figPlotCov.add_trace(
                    go.Bar(
                        x= dfTempCol9[dfTempCol9['classe'] == nclase]['year'],
                        y= dfTempCol9[dfTempCol9['classe'] == nclase]['area'],
                        marker_color= dict_colors[str(nclase)],
                        # marker_symbol= 'star-open',
                        # fill='tonexty',
                        name= dict_class[str(nclase)]
                        ),
                        row = krow + 1, col= kcol + 1
                )
        figPlotCov.add_trace(
            go.Scatter(
                x= dfTempCol8[dfTempCol8['classe'] == nclase]['year'],
                y= dfTempCol8[dfTempCol8['classe'] == nclase]['area'],
                marker_color= "#dbdfdf",
                name="Área col 8"
            ),
            row = krow + 1, col= kcol + 1
        )
        figPlotCov.add_trace(
                go.Scatter(
                x= dfTempCol7[dfTempCol7['classe'] == nclase]['year'],
                y= dfTempCol7[dfTempCol7['classe'] == nclase]['area'],
                marker_color= "#eaf439",
                name= "Área Col 7.1"
                ),
                row = krow + 1, col= kcol + 1
            )
        # print("passou por aqui")
        # print(dict_class[str(nclase)]) 
        figPlotCov.update_xaxes(title_text= dict_class[str(nclase)], row= krow + 1, col= kcol + 1)
    #     figPlot.update_layout(yaxis_range=[-4,4])
        if cc < 1:
            mkey = 'yaxis'
        else:
            mkey = 'yaxis' + str(cc + 1)

        # dictPmtros[mkey] = dictPmtrosPlot[col]

    # print(dictPmtros)
    # figPlot.update_layout(dictPmtros)
    # print("entrou a plot")
    figPlotCov.update_layout(height=1500, width=1000, title_text="Plot Area Bioma/Bacia {}".format(nbacia), showlegend=False)
    return figPlotCov


def plot_AggrementsAreasTwoColections(dfAreaAgg, nomeCobert, nomeBacia):
    valorClass = dict_cobertura[nomeCobert]
    dfTemp = dfAreaAgg[
        (dfAreaAgg["classe"] == valorClass) &
        (dfAreaAgg["bacia"] == nomeBacia)]
    # print(f'know aggrements of area class {valorClass} \n', dfTemp.head())
    
    lstCol = [1,2,3]
    dict_name_aggrement = {
            '1': '<b> concordance </b>',
            '2': '<b> concordance in 9.0 </b>',
            '3': '<b> concordance in 8.0 </b>'
        }

    dict_Ccolor_aggrement = {
                '1': '#808080',
                '2': '#0000FF',
                '3': '#FF0000'
            }
    figAggAr = go.Figure()
    for nClass in lstCol:
        figAggAr.add_trace(go.Bar(
            x= dfTemp[dfTemp['aggrement'] == nClass]['year'],
            y= dfTemp[dfTemp['aggrement'] == nClass]['area'] , # 
            name= dict_name_aggrement[str(nClass)],
            # orientation='h',
            marker_color= dict_Ccolor_aggrement[str(nClass)],
            # text=[f'{kk}%' for kk in dfAgropercent[dfAgropercent['classe_Agro'] == nclase]['percent'].tolist()]
        ))
    nheight = 550
    nwidth = 850
    figAggAr.update_layout(
        title_text=f'Histórico de Discordâncias entre Areas da classe {nomeCobert}',
        title_font_size= 20,
        barmode='stack',
        height= nheight,
        width= nwidth,
        xaxis=dict(
            title="Anos",
            tickangle=0,
            tickfont=dict(size=12),

        ),
        yaxis=dict(
            title="Área em hectares",
            tickfont=dict(size=12),
            showticklabels=True
        ),
        font= dict(size=20),
        legend= dict(orientation="h", x= 0.02,  y=-0.10)
    )
    
    return figAggAr, dfTemp

# cache the dataset
@st.cache_data(ttl=3600)


def load_data_Aggrement_Area(xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    # areaAggrements_toExport_vers_9_Col9.0.csv
    nameTablesGlob = f"areaAggrements_{modelo_act}_vers_{xvers}_Col9.0.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False)
    print("show aggrements Area ", dfAggBacia.head())
    # print(dfAggBacia['Models'].unique())
    # print("=================================")
    dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    dfAggBacia['bacia'] = dfAggBacia['bacia'].astype(str)
    return dfAggBacia


def load_data_AreasColectionBefore():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlobC80 = "areaXclasse_CAATINGA_Col80_red.csv"    
    nameTablesGlobC71 = "areaXclasse_CAATINGA_Col71_red.csv"  
    dfAggBacia80 = pd.read_csv(os.path.join(base_path, nameTablesGlobC80), 
                                index_col=False) 
    dfAggBacia71 = pd.read_csv(os.path.join(base_path, nameTablesGlobC71), 
                                index_col=False)
    # print("=================================")
    print("columns from DataFrame Areas Col8 were \n", dfAggBacia80.columns)
    lstColsImp = ['area', 'classe', 'year', 'Bacia']
    return dfAggBacia80[lstColsImp], dfAggBacia71[lstColsImp]

def load_data_Areas(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    # areaXclasse_CAATINGA_GTB_vers_5_Col9.0.csv
    nameTablesGlob = f"areaXclasse_CAATINGA_{modelo_act}_vers_{xvers}_Col9.0.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print("lista de colunas ", dfAggBacia.columns)
    # print(dfAggBacia.head(3))
    # print("=================================")
    dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)

    colInts = [kk for kk in dfAggBacia.columns]
    # print("colunas listadas \n   ==> ",colInts)
    if 'Unnamed: 0' in colInts:
        colInts.remove('Unnamed: 0')
    dfAggBacia = dfAggBacia[colInts]
    dfAggBacia = dfAggBacia[(dfAggBacia['Bacia'] == nameBac) & (
                                dfAggBacia['version'] == xvers)]
    return dfAggBacia

def load_data_Aggrement(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"regAggrementsAcc_{modelo_act}_vers_{xvers}_Col9.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print(dfAggBacia['Models'].unique())
    # print("=================================")
    dfAggBacia['Version'] = dfAggBacia['Version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)
    return dfAggBacia

def load_data_Acc(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"regMetricsAccs_{modelo_act}_vers_{xvers}_Col9.csv"        
    dfAccYY = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print("=================================")
    # print("", dfAccYY.head())
    colInts = [kk for kk in dfAccYY.columns]
    # print("colunas listadas \n   ==> ",colInts)
    colInts.remove('Unnamed: 0')
    dfAccYY = dfAccYY[colInts]
    # lstIndex = ['Accuracy', 'Accuracy_Bal', 'Precision', 'ReCall', 'F1-Score', 'Jaccard']
    # for colInd in lstIndex:
    #     dfAccYY[colInd] = dfAccYY[colInd].apply(lambda x: round(x * 100, 0))

    dfAccYY['Version'] = dfAccYY['Version'].astype(str)
    dfAccYY['Bacia'] = dfAccYY['Bacia'].astype(str)

    # print(dfAccYY.head())
    return dfAccYY

def load_table_ConfusionMatrix(modelo_act, nversAct):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"Matrices_Confusion_model_{modelo_act}_vers_{nversAct}.csv"
    print(f"loading tabela => {nameTablesGlob}")
    pathTable = os.path.join(base_path, nameTablesGlob)
    dfMCg = pd.read_csv(pathTable)
    allColunas = [kk for kk in dfMCg.columns]
    allColunas.remove('Unnamed: 0')
    dfMCg = dfMCg[allColunas]
    dfMCg = dfMCg.sort_values(by=['year','classes'])
    dfMCg['version'] = dfMCg['version'].astype(str)    
    return dfMCg

def load_MatrixConfution(nameBac, xvers, modelo_act, myear):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'conf_matrix')
    nameMC = f"CM_{nameBac}_{modelo_act}_{myear}_{xvers}.csv"
    pathTable = os.path.join(base_path, nameMC)
    # print(" path table => ", pathTable)
    dfMC = pd.read_csv(pathTable, index_col=0)
    dfMC = dfMC[['3', '4', '12', '21', '22','33', 'Total']]
    print(dfMC.columns)
    print("arquivo Matrix Confo unique \n ", dfMC.head(10))

    return dfMC



# print(dataAcc['Bacia'].unique())
# print("Bacia loaded == \n", dataAcc[dataAcc['Bacia'] == '744'].head())
modelos = ['RF', 'GTB']
posclass = [
    'Gap-fill', 'Spatial', 'Temporal', 'Frequency','toExport','Gap-fillV2',
    'SpatialV2St1', 'FrequencyV2nat', 'FrequencyV2natUso','SpatialV2St3',
    'TemporalV2J3','SpatialV3St1','TemporalV3J3','TemporalV3J4','TemporalV3J5',
    'FrequencyV3St2', 'FrequencyV3St1','SpatialV3su'
]
dictModel = {
    'Random Forest': 'RF', 
    'Gradient Tree Boosting': 'GTB',
    'Gap-fill': 'Gap-fill', 
    'Spatial': 'Spatial', 
    'SpatialV2': 'SpatialV2',
    'Temporal': 'Temporal', 
    'toExport': 'toExport',
    'Frequency': 'Frequency',
    'Gap-fillV2': 'Gap-fillV2',
    'SpatialV2St1': 'SpatialV2St1', 
    'FrequencyV2nat': 'FrequencyV2nat', 
    'FrequencyV2natUso': 'FrequencyV2natUso',
    'SpatialV2St3': 'SpatialV2St3',
    'TemporalV2J3': 'TemporalV2J3',
    'SpatialV3St1': 'SpatialV3St1',
    'TemporalV3J3': 'TemporalV3J3',
    'TemporalV3J4': 'TemporalV3J4',
    'TemporalV3J5': 'TemporalV3J5',
    'FrequencyV3St2': 'FrequencyV3St2',
    'FrequencyV3St1': 'FrequencyV3St1',
    'SpatialV3su': 'SpatialV3su'
}
vers = ['5', '9', '10',  '13', '15', '16', '17','18', '20', '21', '22', '25'] #  '6', '7', '11', '12',
nameBacias = [
      '741', '7421','7422','744','745','746','751','752','763',  
      '753', '754','755','756','757','758','759','7621','7622',
      '764','765','766','767','771','772','773', '7741','7742',
      '776','76111','76116','7612','7613','7614','7615', '775', 
      '7616','7617','7618','7619'
]
# create year filter drop down
lstSelBa = ['bacia_' + str(kk) for kk in nameBacias]
modeloAct = 'GTB'
baciaAct = "SpatialV2"
versionAct = '15'
accCol8 = 75.4
discAloc = 17.0 
discQual = 7.6
st.set_page_config(page_title="Dashboard Maps Validation", page_icon="📈", layout="wide", initial_sidebar_state='collapsed')
dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()
dash_5 = st.container()
# dash_4 = st.container()
with dash_1:
    st.markdown("<h2 style='text-align: center;'>Dashboard Maps Validation </h2>", unsafe_allow_html=True)
    st.write("")

# components
sidebarApp = st.sidebar
with sidebarApp:
    sidebarApp.header("📈  Painel de Validação ")

optionPost = st.sidebar.radio(
                    "selecionar tipo Classificação",
                    ('Class...', 'Pos-Class...'),
                    horizontal= True
                )
optionAnalises = st.sidebar.selectbox(
                    "seleciona Analises",
                    ('Accuracy', 'Area by class') # , 'Aggrement'
                )
if optionPost == 'Class...':
    optionModel = st.sidebar.selectbox(
                    "seleciona Modelo",
                    ('Random Forest', 'Gradient Tree Boosting' )
                )
else:
    optionModel = st.sidebar.selectbox(
                    "seleciona Filtro pos-classificação",
                    posclass
                )
selected_Basin = st.sidebar.selectbox(
                    "Selecionar Bacia ou Bioma", 
                    ['Caatinga 🌵'] + lstSelBa 
                )
selected_Versions = st.sidebar.selectbox("Selecionar Versão", vers)

# if optionModel:
#     modeloAct = dictModel[optionModel]
# if selected_Basin:
#     baciaAct = selected_Basin.replace('bacia_', '')
# if selected_Versions:
#     versionAct = selected_Versions

if optionAnalises == 'Accuracy':          

    modeloAct = dictModel[optionModel]
    baciaAct = selected_Basin.replace('bacia_', '').replace(" 🌵", "")
    versionAct = selected_Versions

    dataAcc = load_data_Acc(baciaAct, versionAct, modeloAct)
    dataAggAc = load_data_Aggrement(baciaAct, versionAct, modeloAct)

    # print(f"tenemos uma analises aqui de  Accuracy para os dados {modeloAct}| {baciaAct} | {versionAct}")
    # st.write(f"tenemos uma analises aqui de  Accuracy para os dados {modeloAct}| {baciaAct} | {versionAct}")
    
    # 'Accuracy', 'Accuracy_Bal', 'Precision', 'ReCall', 'F1-Score', 'Jaccard'
    accMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Accuracy'].mean() * 100
    preMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Precision'].mean() * 100
    reCMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['ReCall'].mean() * 100 

    with dash_3:
        col1,col2,col3 = st.columns(3)
        with col1: 
            st.metric(
                label="Accuracy Mean", 
                value= str(round(accMean, 2)) + " %",
                delta= round(accMean - accCol8, 2)
            )
        with col2:
            st.metric(
                label="Precision Mean", 
                value= str(round(preMean, 2)) + " %"
            )
        with col3:
            st.metric(
                label="ReCall Mean", 
                value= str(round(reCMean, 2)) + " %",
            )

    # dataAggAc
    with dash_2:
        dfSpec = dataAggAc[
                    (dataAggAc["Bacia"] == baciaAct) & 
                    (dataAggAc["Models"] == modeloAct) &
                    (dataAggAc["Version"] == str(versionAct))
            ]
        AccAct = dfSpec['global_accuracy'].mean()
        quantDis = dfSpec['quantity diss'].mean()
        allocDis = dfSpec['alloc dis'].mean()

        colAgg1,colAgg2,colAgg3 = st.columns(3)
        with colAgg1: 
            st.metric(
                label="Accuracia", 
                value= str(round(AccAct, 2)) + " %",
                delta= round(AccAct - accCol8, 2)   
            )
        with colAgg2:
            st.metric(
                label="Discordância de alocação", 
                value= str(round(quantDis, 2)) + " %",
                # menor erro de quantidade é melhor
                delta= round(discQual - quantDis, 2)  
                
            )
        with colAgg3:
            st.metric(
                label="Discordância de quantidade", 
                value= str(round(allocDis, 2)) + " %",
                # menor erro de allocação é melhor
                delta= round(discAloc - allocDis, 2)
            )
        ## Display the figure in Streamlit
        figPlotAgg =get_plotBar_Acc_Disaggrements(dataAggAc, baciaAct, modeloAct, versionAct)
        st.plotly_chart(figPlotAgg)
        
    # plots grp1
    with dash_4:        
        ## Display the figure in Streamlit
        figPlot = get_chart_Plot_plotlyX(dataAcc, baciaAct, modeloAct, versionAct)
        st.plotly_chart(figPlot)

    with dash_5:
        optionMatConf = st.radio(
                    "visualização por tabela",
                    ('Matriz Confusão', '📊 gráficos de omissão | comissão '),
                    horizontal= True
                )
        if optionMatConf == 'Matriz Confusão':
            colInfo1, colInfo2 = st.columns(2)
            st.write(" Matriz de Confussão")
            with colInfo1:
                yyearSel = st.slider("Selecione o ano ", 1985, 2022)
            with colInfo2:
                st.write("")
            # print("year selecionado ", yyearSel)
            dfMatConf = load_MatrixConfution(baciaAct, versionAct, modeloAct, yyearSel)
            st.dataframe(dfMatConf)
        else:
            dfMatConf = load_table_ConfusionMatrix(modeloAct, versionAct) 
            # print("show if table loaded correctly >>> ", dfMatConf.shape)
            # print(f" bacia selecionada {baciaAct} | version selecionada {versionAct}")
            print("lst of version ", dfMatConf['version'].unique())
            print("lst of columns ", dfMatConf.columns)
            lstColunas = ['classes', '3', '4', '12', '21', '22', '33', 'Total', 'bacia', 'model', 'version', 'year']
            dfMatConf = dfMatConf[lstColunas]
            print("ver as colunas \n", dfMatConf)
            dfMatConf = dfMatConf.dropna(how='all')  
            dfMatConf['21'] = dfMatConf['21'].astype(int)

            dfCMgf = dfMatConf[(dfMatConf['bacia'] == baciaAct) & (dfMatConf['version'] == versionAct)]
            # dfCMgf = dfMatConf[dfMatConf['bacia'] == baciaAct]
            # print("shape filtered bacia and version >>> ", dfCMgf.shape)
            # st.write(f"tabela de Erros {dfCMgf.shape}")
            print(dfMatConf[(dfMatConf['bacia'] == baciaAct) & (dfMatConf['version'] == versionAct) & (dfMatConf['year'] == 1985)])
            processMCyearBasin = getYearClassfromMC(dfMatConf[(dfMatConf['bacia'] == baciaAct) & (dfMatConf['version'] == versionAct)])
            processMCyearBasin.makeCMpercent()
            print("process matrix Conf " )
            dfOmision = processMCyearBasin.dfCMgfpOmision
            dfOmision = dfOmision.sort_values(by='classes')
            print(dfOmision[dfOmision['year'] == 1985])
            dfComision = processMCyearBasin.dfCMgfpComision
            dfComision = dfComision.sort_values(by='classes')
            print(dfComision.head(8))

            colInfo1, colInfo2 = st.columns(2)
            with colInfo1:
                yyearSel = st.slider("Selecione o ano ", 1985, 2022)                
            with colInfo2:
                st.write(" ")
            # print("year selecionado ", yyearSel)
            colErro1, colErro2 = st.columns(2)
            with colErro1:
                plotOmission = plot_graficos_erros_acc_ProdUser(dfOmision[dfOmision['year'] == yyearSel].iloc[:-1], f"ERRO OMISSÂO | ACCURACY PRODUTOR >> {yyearSel}", False)
                st.plotly_chart(plotOmission)
            
            with colErro2:
                # print("size of table to plot ", dfComision[dfComision['year'] == 1985].iloc[:-1].shape)
                # print(dfComision[dfComision['year'] == 1985].iloc[:-1])
                plotComission =plot_graficos_erros_acc_ProdUser(dfComision[dfComision['year'] == yyearSel].iloc[:-1], f"ERRO COMISSÂO | ACCURACY USER >> {yyearSel}", True)
                st.plotly_chart(plotComission)

            colInfo1, colInfo2 = st.columns(2)
            selected_Classe = st.selectbox(
                    "Selecionar cobertura", columnsInt )
            # print("classe selecionada ", selected_Classe)
            # print(dict_cobertura[selected_Classe])
            # print(dfOmision.head())
            # dfOmision['classes']
            plotErroTimeSerieOmi = plot_graficoAccuracyErrobyClass(dfOmision[dfOmision['classes'] == str(dict_cobertura[selected_Classe])], 'Omissão')
            st.plotly_chart(plotErroTimeSerieOmi)
            plotErroTimeSerieComi = plot_graficoAccuracyErrobyClass(dfComision[dfComision['classes'] == str(dict_cobertura[selected_Classe])], 'Comissão')
            st.plotly_chart(plotErroTimeSerieComi)

elif optionAnalises == 'Area by class':
    print("updating model ", optionModel)
    modeloAct = dictModel[optionModel]
    baciaAct = selected_Basin.replace('bacia_', '').replace(" 🌵", "")
    versionAct = selected_Versions
    dfAreaC80, dfAreaC71 = load_data_AreasColectionBefore()    

    # print("table Col8 \n", dfAreaC80)
    # print("table Col71 \n", ddfAreaC71)    

    lstclass_part1 = [3,4,12,33]
    lstclass_part2 = [15,21,18,22]
    try:
        dataAreas = load_data_Areas(baciaAct, versionAct, modeloAct)
        # st.write("tenemos um analises aqui Area")
        print(dataAreas.head(6))
        with dash_2:
            colAr1, colAr2 = st.columns(2)

            with colAr1:
                # st.write("gráfico ano 1985")
                print(f"dataAreas => baciaAct {baciaAct} | modeloAct {modeloAct} | versionAct {versionAct} | 1985")
                figPlotPie85 =  plotPieYear(dataAreas, baciaAct, modeloAct, versionAct, 1985)
                st.plotly_chart(figPlotPie85)

            with colAr2:
                # st.write("gráfico ano 2021")
                figPlotPie23 =  plotPieYear(dataAreas, baciaAct, modeloAct, versionAct, 2021)
                st.plotly_chart(figPlotPie23)

        with dash_3:
            colArBar1, colArBar2 = st.columns(2)
            with colArBar1:
                # st.write("tenemos um analises aqui Area")
                figPlotClassLeft = buildingPlots_Cruzando_Class(dataAreas, baciaAct, modeloAct, versionAct, lstclass_part1)
                st.plotly_chart(figPlotClassLeft)
            with colArBar2:
                # st.write("tenemos um analises aqui Area")
                figPlotClassRigth = buildingPlots_Cruzando_Class(dataAreas, baciaAct, modeloAct, versionAct, lstclass_part2, 495)
                st.plotly_chart(figPlotClassRigth)
        
        with dash_4:       
            # st.write("tenemos um analises aqui Area")
            nameImage = 'images/palettesCollectionsbefore.png'
            st.image(nameImage,  width = 450)
            # df_AreaPlot, dfAreasCol8, dfAreasCol7, nbacia= 741, nModel= "RF", vers= '5'
            figPlotallCols = plot_graficoSeparateCover(dataAreas, dfAreaC80, dfAreaC71 ,baciaAct,  modeloAct, versionAct)
            st.plotly_chart(figPlotallCols)

        if versionAct not in ['11', '12']:
            print("we have to print plot")
            dfAreaAgg = load_data_Aggrement_Area(versionAct, modeloAct)
            print("table Area Aggrements  \n", dfAreaAgg.head())
            with dash_5:
                st.write("tenemos um analises aquide concordancia de Area")
                nameImage = 'images/paletaAggrements_black.png'
                st.image(nameImage,  width = 500)  # caption='maps aggrements area palette'
                selected_ClasseAr = st.selectbox(
                        "Selecionar cobertura", columnsInt )
                print("cobertura = " + selected_ClasseAr)
                figPlotAggArea, dfTempCov =  plot_AggrementsAreasTwoColections(dfAreaAgg, selected_ClasseAr, baciaAct)
                if dfTempCov.shape[0] > 0:
                    st.plotly_chart(figPlotAggArea)
                else:
                    st.write(f"tenemos temos algo errado na classe  {selected_ClasseAr}")
    except:
        st.write(" Sorry we don´t have data with parameter ") 