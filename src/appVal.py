
import os
import streamlit as st
import numpy as np
import pandas as pd
from millify import millify
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
import altair as alt
import plotly.express as px
import plotly.graph_objects as go


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
    
    lstCol = ["quantity diss","alloc dis","global_accuracy",]
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


# cache the dataset
@st.cache_data(ttl=3600)
def load_data_Acc():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "regMetricsAccGlobalCol9.csv"        
    nameTablesBacia = "regMetricsAccBaciasCol9.csv"
    dfAccYY = pd.read_csv(os.path.join(base_path, nameTablesGlob))
    dfAccBacia = pd.read_csv(os.path.join(base_path,nameTablesBacia))
    # print("=================================")
    # print("", dfAccBacia.head())

    colInts = [kk for kk in dfAccBacia.columns]
    # print("colunas listadas \n   ==> ",colInts)
    colInts.remove('Unnamed: 0')
    dfAccBacia = dfAccBacia[colInts]

    dfAccYY['Bacia'] = ['Caatinga'] * dfAccYY.shape[0]
    dfAccYY = dfAccYY[colInts]
    
    dfAcc = pd.concat([dfAccYY, dfAccBacia], ignore_index=True, axis=0)
    dfAcc['version'] = dfAcc['version'].astype(str)
    dfAcc['Bacia'] = dfAcc['Bacia'].astype(str)
    return dfAcc

def load_data_Aggrement():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "regAggrementsAccGlobalCol9.csv"    
    dfAggBacia = pd.read_csv(os.path.join(base_path, nameTablesGlob))
    # print("=================================")
    colInts = [kk for kk in dfAggBacia.columns]
    # print("colunas listadas \n   ==> ",colInts)
    # colInts.remove('Unnamed: 0')
    dfAggBacia = dfAggBacia[colInts]

    dfAggBacia['version'] = dfAggBacia['version'].astype(str)
    dfAggBacia['Bacia'] = dfAggBacia['Bacia'].astype(str)
    return dfAggBacia

dataAcc = load_data_Acc()
dataAggAc = load_data_Aggrement()
# print(dataAcc['Bacia'].unique())
# print("Bacia loaded == \n", dataAcc[dataAcc['Bacia'] == '744'].head())
modelos = ['RF', 'GTB']
dictModel = {
    'Random Forest': 'RF', 
    'Gradient Tree Boosting': 'GTB'
}
vers = ['5', '6', '7']
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
# 'Accuracy', 'Accuracy_Bal', 'Precision', 'ReCall', 'F1-Score', 'Jaccard'
accMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Accuracy'].mean() * 100
preMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Precision'].mean() * 100
reCMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['ReCall'].mean() * 100 

dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()
with dash_1:
    st.markdown("<h2 style='text-align: center;'>Dashboard Maps Validation </h2>", unsafe_allow_html=True)
    st.write("")

# components
sidebarApp = st.sidebar
with sidebarApp:
    sidebarApp.header("📈  Painel de Validação ")


optionAnalises = st.sidebar.selectbox(
                    "seleciona Analises",
                    ('Accuracy', 'Area by class') # , 'Aggrement'
                )
optionModel = st.sidebar.selectbox(
                    "seleciona Modelo",
                    ('Random Forest', 'Gradient Tree Boosting' )
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
    # print(f"tenemos uma analises aqui de  Accuracy para os dados {modeloAct}| {baciaAct} | {versionAct}")
    # st.write(f"tenemos uma analises aqui de  Accuracy para os dados {modeloAct}| {baciaAct} | {versionAct}")
    
    with dash_2:
        col1,col2,col3 = st.columns(3)
        # with col1: 
        #     "##### Accuracy Mean" 
        #     "% " + millify(accMean, precision=2)
        col1.metric(label="Accuracy Mean", value= millify(accMean, precision=1) + " %")
        col2.metric(label="Precision Mean", value= millify(preMean, precision=1) + " %")
        col3.metric(label="ReCall Mean", value= millify(reCMean, precision=1) + " %")

    # plots grp1
    with  dash_3:
        ## Display the figure in Streamlit
        figPlot = get_chart_Plot_plotlyX(dataAcc, baciaAct, modeloAct, versionAct)
        st.plotly_chart(figPlot)

    # dataAggAc
    with dash_3:
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
        colAgg1.metric(label="Accuracia", value= millify(AccAct, precision=2) + " %")
        colAgg2.metric(label="Discordância de alocação", value= millify(quantDis, precision=2) + " %")
        colAgg3.metric(label="Discordância de quantidade", value= millify(allocDis, precision=2) + " %")

    with dash_4:
         ## Display the figure in Streamlit
        figPlotAgg =get_plotBar_Acc_Disaggrements(dataAggAc, baciaAct, modeloAct, versionAct)
        st.plotly_chart(figPlotAgg)

elif optionAnalises == 'Area by class':   
    st.write("tenemos um analises aqui Area")