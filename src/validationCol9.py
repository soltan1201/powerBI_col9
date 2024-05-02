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

# cache the dataset
@st.cache_data(ttl=3600)
def load_data_Acc():
    base_path = os.getcwd()
    base_path = os.path.join(base_path, 'dbase')
    nameTablesGlob = "regMetricsAccGlobalCol9.csv"        
    nameTablesBacia = "regMetricsAccBaciasCol9.csv"
    dfAccYY = pd.read_csv(os.path.join(base_path, nameTablesGlob))
    dfAccBacia = pd.read_csv(os.path.join(base_path,nameTablesBacia))

    colInts = [kk for kk in dfAccBacia.columns]
    # print("colunas listadas \n   ==> ",colInts)
    colInts.remove('Unnamed: 0')
    dfAccBacia = dfAccBacia[colInts]

    dfAccYY['Bacia'] = ['Caatinga'] * dfAccYY.shape[0]
    dfAccYY = dfAccYY[colInts]

    dfAcc = pd.concat([dfAccYY, dfAccBacia], ignore_index=True, axis=0)

    return dfAcc

def get_chart_Plot_plotlyX(dfAccur, nbacia= 741, nModel= "RF"):
    colunas = ["Accuracy","Accuracy_Bal","Precision","ReCall", "F1-Score","Jaccard"]
    dfTemp = dfAccur[(dfAccur["Bacia"] == nbacia) & (dfAccur["Models"] == nModel)]
    # print(dfTemp.head())
    fig = px.line(dfTemp, 
                x="Years", y=colunas,
                hover_data={"Years": "%Y"},
                title=  f'Accuracy metrics of basin {nbacia} with model {nModel} '.upper(),
                template="plotly_dark",
            )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y"
    )
    # fig.show()
    fig.layout.autosize = True
    return fig

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


# st.set_page_config(
#     page_title="Dashboard Validation colection 9", 
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state='collapsed'
# )
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    color: MediumSeaGreen;  
                    height: 10em;
                }
        </style>
        """, 
        unsafe_allow_html=True) 
# components
sidebarApp = st.sidebar

# headerApp = st.header("Dashboard Validation colection 9 ")
dash_1 = st.container()
dash_2 = st.container()
dash_3 = st.container()
dash_4 = st.container()

with sidebarApp:
    sidebarApp.header("Painel de Validação")
    mytextSide = "Este painel permite navegar entre \nos elementos de Accuracia, Áreas \ndas classes"
    sidebarApp.text(mytextSide)

    # create year filter drop down
    lstSelBa = ['bacia_' + str(kk) for kk in nameBacias]
    selected_Basin = st.selectbox("Selecionar Bacia ou Bioma", ['Caatinga'] + lstSelBa )
# st.markdown()


with dash_1:
    st.markdown("<h2 style='text-align: center;'>Dashboard Maps Validation </h2>", unsafe_allow_html=True)
    st.write("")

with dash_2:
    # 'Accuracy', 'Accuracy_Bal', 'Precision', 'ReCall', 'F1-Score', 'Jaccard'
    accMax = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Accuracy'].max() * 100
    accMin = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Accuracy'].min() * 100
    accMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Accuracy'].mean() * 100   

    col1,col2,col3 = st.columns(3)
    # with col1: 
    #     "##### Accuracy Mean" 
    #     "% " + millify(accMean, precision=2)
    col1.metric(label="Accuracy Mean", value= " %"+millify(accMean, precision=1))
    col2.metric(label="Accuracy Minimum", value= " %"+millify(accMin, precision=1))
    col3.metric(label="Accuracy Maximum", value= " %"+millify(accMax, precision=1))
    

    style_metric_cards(border_left_color="#DBF227")

# plots grp1
with  dash_3:
    ## Display the figure in Streamlit
    figPlot = get_chart_Plot_plotlyX(dataAcc, 'Caatinga', 'GTB')
    st.plotly_chart(figPlot)

#  Other Metrics
with  dash_4:
    preMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Precision'].mean() * 100
    reCMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['ReCall'].mean() * 100
    f1SMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['F1-Score'].mean() * 100
    jacMean = dataAcc[dataAcc['Bacia'] == 'Caatinga']['Jaccard'].mean() * 100

    col4,col5,col6,col7 = st.columns(4) # col5,col6,col7

    col4.metric(label="Precision Mean", value= " %"+millify(preMean, precision=1))
    col5.metric(label="ReCall Mean", value= " %"+millify(reCMean, precision=1))
    col6.metric(label="F1-Score Mean", value= " %"+millify(f1SMean, precision=2))
    col7.metric(label="Jaccard Mean", value= " %"+millify(jacMean, precision=2))