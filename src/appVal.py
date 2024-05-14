
import os
import streamlit as st
import numpy as np
import pandas as pd
from millify import millify
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
# import altair as alt
import ipywidgets
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
dict_colors = {}
for ii, cclass in enumerate(classes):
    dict_colors[dict_class[str(cclass)]] = colors[ii]
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
                (dfAccur["version"] == str(vers))
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
    fig.layout.autosize = True
    return fig

def get_plotBar_Acc_Disaggrements(dfAccur, nbacia= 741, nModel= "RF", vers= '5'):
    dfTemp = dfAccur[
                (dfAccur["Bacia"] == nbacia) & 
                (dfAccur["Models"] == nModel) &
                (dfAccur["version"] == str(vers))
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
        "alloc dis": 1
    }

    figAgg = go.Figure()
    for ncol in lstCol:
        figAgg.add_trace(go.Bar(
            x= dfTemp['Years'],
            y= dfTemp[ncol], # * dictsignoAgg[ncol]
            name= dictNameAgg[ncol],
            # orientation='h',
            marker_color= dictColorAgg[ncol],
            # text=[f'{kk}%' for kk in dfAgropercent[dfAgropercent['classe_Agro'] == nclase]['percent'].tolist()]
        ))
    nheight = 550
    nwidth = 700
    figAgg.update_layout(
        title_text='Histórico de Accuracia e Discordâncias',
        title_font_size= 28,
        barmode='stack',
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


def buildingPlots_Cruzando_Class(dfAccur, nbacia= 741, nModel= "RF", vers= '5', lstclass= [3,4,12]):

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
            height= 500, 
            width= 700, 
            title_text="Plot Áreas de classes " + tipoclase, 
            showlegend=True,
            legend= dict(
                        orientation="h", 
                        x= 0.01,  
                        y= -0.15, 
                        font=dict(
                            family="Courier",
                            size=24,
                            color="black"
                        ),
                    ),
    )

    return figPlotCr


# cache the dataset
@st.cache_data(ttl=3600)
def load_data_Acc(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"regMetricsAccs_{modelo_act}_Col9.csv"        
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

    dfAccYY['version'] = dfAccYY['version'].astype(str)
    dfAccYY['Bacia'] = dfAccYY['Bacia'].astype(str)

    # print(dfAccYY.head())
    return dfAccYY

def load_data_Aggrement(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"regAggrementsAcc_{modelo_act}_Col9.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print(dfAggBacia['Models'].unique())
    # print("=================================")
    dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)
    return dfAggBacia

def load_data_Areas(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = f"areaXclasse_CAATINGA_{modelo_act}_Col9.0.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
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

def load_MatrixConfution(nameBac, xvers, modelo_act, myear):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'conf_matrix')
    nameMC = f"CM_{nameBac}_{modelo_act}_{myear}_{xvers}.csv"
    pathTable = os.path.join(base_path, nameMC)
    print(" path table => ", pathTable)
    dfMC = pd.read_csv(pathTable)
    return dfMC


# print(dataAcc['Bacia'].unique())
# print("Bacia loaded == \n", dataAcc[dataAcc['Bacia'] == '744'].head())
modelos = ['RF', 'GTB']
posclass = ['Gap-fill', 'Spatial', 'Temporal', 'toExport']
dictModel = {
    'Random Forest': 'RF', 
    'Gradient Tree Boosting': 'GTB',
    'Gap-fill': 'Gap-fill', 
    'Spatial': 'Spatial', 
    'Temporal': 'Temporal', 
    'toExport': 'toExport'
}
vers = ['5', '6', '7', '9']
nameBacias = [
      '741', '7421','7422','744','745','746','751','752','763',  
      '753', '754','755','756','757','758','759','7621','7622',
      '764','765','766','767','771','772','773', '7741','7742',
      '776','76111','76116','7612','7613','7614','7615', '775', 
      '7616','7617','7618','7619'
]
# create year filter drop down
lstSelBa = ['bacia_' + str(kk) for kk in nameBacias]
modeloAct = 'RF'
baciaAct = "Caatinga"
versionAct = '5'
accCol8 = 75.4
discAloc = 17.0 
discQual = 7.6

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
                    (dataAggAc["version"] == str(versionAct))
            ]
        AccAct = dfSpec['global_accuracy'].mean()
        quantDis = dfSpec['quantity diss'].mean()
        allocDis = dfSpec['alloc dis'].mean()

        colAgg1,colAgg2,colAgg3 = st.columns(3)
        # with col1: 
        #     "##### Accuracy Mean" 
        #     "% " + millify(accMean, precision=2)
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
        st.write("Error de Omissão ")
        dfMatConf = load_MatrixConfution(baciaAct, versionAct, modeloAct, 2020)
        st.dataframe(dfMatConf)

elif optionAnalises == 'Area by class':
    print("updating model ", optionModel)
    modeloAct = dictModel[optionModel]
    baciaAct = selected_Basin.replace('bacia_', '').replace(" 🌵", "")
    versionAct = selected_Versions

    lstclass_part1 = [3,4,12,33]
    lstclass_part2 = [15,21,18,22]
    dataAreas = load_data_Areas(baciaAct, versionAct, modeloAct)
    # st.write("tenemos um analises aqui Area")
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
        # st.write("tenemos um analises aqui Area")
        figPlotClass = buildingPlots_Cruzando_Class(dataAreas, baciaAct, modeloAct, versionAct, lstclass_part1)
        st.plotly_chart(figPlotClass)

    with dash_4:
        # st.write("tenemos um analises aqui Area")
        figPlotClass = buildingPlots_Cruzando_Class(dataAreas, baciaAct, modeloAct, versionAct, lstclass_part2)
        st.plotly_chart(figPlotClass)
