
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
    '25': 'Non vegetated area', 
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
    # 'Non vegetated area': 22, 
    'Non vegetated area': 25, 
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
    '25': 'Antrópico', 
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
    '25': '#db4d4f', 
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
dictModel = {
    'Gradient Tree Boosting': 'GTB',
    'Gap-fill': 'GF', 
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
    'Temporal J3': 'TPJ3',
    'Temporal J4': 'TPJ4',
    'Temporal J5': 'TPJ5',
    'FrequencyV3St2': 'FrequencyV3St2',
    'FrequencyV3St1': 'FrequencyV3St1',
    'SpatialV3su': 'SpatialV3su',
    'Corretion Florest': 'CO',
    'Corretion Grassland': 'GAGr'
}

vers = ['1','2','3','4']
nameBacias = [
    '7754', '7581', '7625', '7584', '751', '7614', 
    '752', '7616', '745', '7424', '773', '7612', '7613', 
    '7618', '7561', '755', '7617', '7564', '761111', '761112', 
    '7741', '7422', '76116', '7761', '7671', '7615', '7411', 
    '7764', '757', '771', '7712', '766', '7746', '753', '764', 
    '7541', '7721', '772', '7619', '7443', '765', '7544', '7438', 
    '763', '7591', '7592', '7622', '746'
] 


def load_data_Acc(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbaseS2')
    nameTablesGlob = f"regMetricsAccs_{modelo_act}_vers_{xvers}_ColS2.csv"        
    dfAccYY = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    print("=================================")
    print("", dfAccYY.head(9))
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


def load_data_Aggrement(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbaseS2')
    nameTablesGlob = f"regAggrementsAcc_{modelo_act}_vers_{xvers}_ColS2.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    # print(dfAggBacia['Models'].unique())
    # print("=================================")
    dfAggBacia['Version'] = dfAggBacia['Version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)
    return dfAggBacia


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

def load_data_AreasColectionBefore():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbaseS2')
    nameTablesGlobC90 = "areaXclasse_CAATINGA_Col90_red.csv"   
    nameTablesGlobC80 = "areaXclasse_CAATINGA_Col80_red.csv"    
    nameTablesGlobC71 = "areaXclasse_CAATINGA_Col71_red.csv"  
    dfAggBacia90 = pd.read_csv(os.path.join(base_path, nameTablesGlobC90), 
                                index_col= False) 
    dfAggBacia80 = pd.read_csv(os.path.join(base_path, nameTablesGlobC80), 
                                index_col= False) 
    dfAggBacia71 = pd.read_csv(os.path.join(base_path, nameTablesGlobC71), 
                                index_col= False)
    # print("=================================")
    print("columns from DataFrame Areas Col8 were \n", dfAggBacia80.columns)
    print("columns from DataFrame Areas Col9 were \n", dfAggBacia90.columns)
    lstColsImp = ['area', 'classe', 'year', 'Bacia']
    return dfAggBacia90[lstColsImp], dfAggBacia80[lstColsImp], dfAggBacia71[lstColsImp]


def load_data_Areas(nameBac, xvers, modelo_act):
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbaseS2')
    # areaXclasse_CAATINGA_GTB_vers_5_Col9.0.csv
    nameTablesGlob = f"areaXclasse_CAATINGA_{modelo_act}_vers_{xvers}_ColS2.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob), index_col=False, low_memory=False)
    print("lista de colunas ", dfAggBacia.columns)
    print(dfAggBacia.head(3))
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



def plot_graficoSeparateCover(df_AreaPlot, dfAreasCol9, dfAreasCol8, dfAreasCol7, nbacia= '741', nModel= "GTB", vers= '1'):
    dictPmtros = {
        'height': 1200,
        'width': 800,
        'template':'plotly_white'
    }    
    dfTempColS2 = df_AreaPlot[
                (df_AreaPlot["Bacia"] == nbacia) & 
                (df_AreaPlot["Models"] == nModel) &
                (df_AreaPlot["version"] == str(vers))            
            ]
    dfTempCol9 = dfAreasCol9[dfAreasCol9["Bacia"] == nbacia ]
    dfTempCol8 = dfAreasCol8[dfAreasCol8["Bacia"] == nbacia ]
    dfTempCol7 = dfAreasCol7[dfAreasCol7["Bacia"] == nbacia ]
    
    print(f"dados {nbacia} -- {nModel} --- {vers}")
    print("table Col Sentinel \n", dfTempColS2.head())
    print("table Col9 \n", dfTempCol9.head())
    print("table Col8 \n", dfTempCol8.head())
    print("table Col71 \n", dfTempCol7.head())

    listClass = [3, 4, 12, 21, 25, 33]
    figPlotCov = make_subplots(rows= 3, cols= 2)
    for cc, nclase in enumerate(listClass):        
        krow = floor(cc/ 2)
        kcol = cc % 2        
        print('index ', cc, " classe = ", nclase, " color = ", dict_colors[str(nclase)])
        figPlotCov.add_trace(
                    go.Bar(
                        x= dfTempColS2[dfTempColS2['classe'] == nclase]['year'],
                        y= dfTempColS2[dfTempColS2['classe'] == nclase]['area'],
                        marker_color= dict_colors[str(nclase)],
                        # marker_symbol= 'star-open',
                        # fill='tonexty',
                        name= dict_class[str(nclase)]
                        ),
                        row = krow + 1, col= kcol + 1
                )
        figPlotCov.add_trace(
            go.Scatter(
                x= dfTempCol9[dfTempCol9['classe'] == nclase]['year'],
                y= dfTempCol9[dfTempCol9['classe'] == nclase]['area'],
                marker_color= "#FF0000",
                name="Área col 90"
            ),
            row = krow + 1, col= kcol + 1
        )
        figPlotCov.add_trace(
            go.Scatter(
                x= dfTempCol8[dfTempCol8['classe'] == nclase]['year'],
                y= dfTempCol8[dfTempCol8['classe'] == nclase]['area'],
                marker_color= "#dbdfdf",
                name="Área col 90"
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


# create year filter drop down
lstSelBa = ['bacia_' + str(kk) for kk in nameBacias]
modeloAct = 'GTB'
optionModel = 'Gradient Tree Boosting'
posclass = [
    'Gradient Tree Boosting','Gap-fill','Corretion Florest',
    'Temporal J3', 'Temporal J4', 'Temporal J5','Corretion Grassland'
    ]
accCol8 = 75.4
discAloc = 17.0 
discQual = 7.6
st.set_page_config(page_title="Dashboard Maps Validation", page_icon="📈", layout="wide", initial_sidebar_state='collapsed')
dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()
dash_5 = st.container()

with dash_1:
    st.markdown("<h2 style='text-align: center;'>Dashboard Maps Validation </h2>", unsafe_allow_html=True)
    st.write("")

# components
sidebarApp = st.sidebar
with sidebarApp:
    sidebarApp.header(" Painel de Validação Coleção S2 📈")

optionAnalises = st.sidebar.selectbox(
                    "seleciona o tipo de Analises",
                    ('Accuracy', 'Area by class') # , 'Aggrement'
                )
optionModel = st.sidebar.selectbox(
                    "seleciona modelo ou Filtro pos-classificação",
                    posclass
                )
selected_Basin = st.sidebar.selectbox(
                    "Selecionar Bacia ou Bioma", 
                    ['Caatinga 🌵'] + lstSelBa 
                )
selected_Versions = st.sidebar.selectbox("Selecionar Versão", vers)


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


elif optionAnalises == 'Area by class':
    print("updating model ", optionModel)
    modeloAct = dictModel[optionModel]
    baciaAct = selected_Basin.replace('bacia_', '').replace(" 🌵", "")
    versionAct = selected_Versions
    dfAreaC90, dfAreaC80, dfAreaC71 = load_data_AreasColectionBefore()    
    
    print("table Col9 \n", dfAreaC90)
    print("table Col8 \n", dfAreaC80)
    print("table Col71 \n", dfAreaC71)    

    lstclass_part1 = [3,4,12,33]
    lstclass_part2 = [15,21,18,25]

    try:
        dataAreas = load_data_Areas(baciaAct, versionAct, modeloAct)
        st.write("tenemos um analises aqui Area")
        print(dataAreas.head(6))
        print()

        with dash_2:
            colAr1, colAr2 = st.columns(2)

            with colAr1:
                # st.write("gráfico ano 1985")
                print(f"dataAreas => baciaAct {baciaAct} | modeloAct {modeloAct} | versionAct {versionAct} | 1985")
                figPlotPie85 =  plotPieYear(dataAreas, baciaAct, modeloAct, versionAct, 2016)
                st.plotly_chart(figPlotPie85)

            with colAr2:
                # st.write("gráfico ano 2021")
                figPlotPie23 =  plotPieYear(dataAreas, baciaAct, modeloAct, versionAct, 2023)
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
            figPlotallCols = plot_graficoSeparateCover(dataAreas, dfAreaC90, dfAreaC80, dfAreaC71 ,baciaAct,  modeloAct, versionAct)
            st.plotly_chart(figPlotallCols)

    except:
        st.write(" Sorry we don´t have data with parameter ") 