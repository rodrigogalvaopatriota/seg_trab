import pandas as pd
from datetime import datetime
import streamlit as st
import altair as alt
import os

      
class Dashboard:

    def __init__(self):
        
        #self.df = TreatDataFrame()
        self.df = df = pd.read_excel(f'result_geral.xlsx')
        self.df['den'] = 1
    
    
    
    def grafico_barras_prioridade_diaDaSemanaAbertura(self,data_chart,nome_x,nome_y):
        #nome_x = 'prioridade_ba'
        # Criar gráfico de barras com Altair
        bars = (
            #alt.Chart(data_menos_500)
            
            alt.Chart(data_chart)
            .mark_bar()
            .encode(
                x=alt.X(
                    f"{nome_x}:N",
                    sort=alt.EncodingSortField("den", op="sum", order="descending"),
                    #sort=alt.EncodingSortField("quantidade", op="sum", order="descending"),
                    title=f"{nome_x}",
                ),
                y=alt.Y(
                    "den:Q", title="dia",
                    sort=alt.EncodingSortField("den", op="count", order="descending"),
                    #text=alt.Text("den:Q", aggregate="sum", format=".0f")
                    
                
                ),
                color=f"{nome_y}:N",
                tooltip=[
                    alt.Tooltip(f"{nome_y}:N", title=f"{nome_y}"),
                    alt.Tooltip("den:Q", title="dia"),
                    #alt.Tooltip("percentual:Q", title="Percentual (%)", format=".2f"),  # Mostrar o percentual
                ],
            )
            .properties(
                width=3000,
                #title="Quantidade de Colaboradores por Coordenador e Status de Distância",
            )
        )
        
        # Adicionar os rótulos de percentual
        text = (
            
            alt.Chart(data_chart)
            .mark_text(dy=-10, size=10, color="black")  # Ajusta a posição e aparência do texto
            .encode(
                x=alt.X("prioridade_ba:N"),
                #y=alt.Y("den:Q"),
               

                y=alt.Y("den:Q", aggregate="sum"),
                text=alt.Text("den:Q", aggregate="sum", format=".0f"),
                detail=f"{nome_y}:N"
                #text=alt.Text("percentual:Q", format=".1f"), #  Formatar percentual com uma casa decimal
            )
        )
        
        # Combinar as barras e os rótulos no gráfico
        chart = bars + text
        #chart = bars
        return chart

    def grafico_barras(self,data_chart):

         # Criar o gráfico de barras
        chart = alt.Chart(data_chart).mark_bar(color='steelblue').encode(
            x=alt.X("dia:N", sort='-y', title="dia"),
            y=alt.Y("den:Q", title="Contagem de dias"),
            tooltip=["dia", "den"]
        ).properties(
            width=800,  # Largura do gráfico
            height=400,  # Altura do gráfico
            title="Soma de dias"
        )
        return chart


    def grafico_barras_(self, data_chart):
        bars = (
            alt.Chart(data_chart)
            .mark_bar()
            .encode(
                x=alt.X("prioridade_ba:N", title="Prioridade"),
                xOffset="nome_dia_abertura:N",  # <--- Essa linha é o segredo para barras lado a lado
                y=alt.Y("den:Q", title="Quantidade de Prioridades"),
                color="nome_dia_abertura:N",
                tooltip=[
                    alt.Tooltip("nome_dia_abertura:N", title="Dia da Semana Abertura"),
                    alt.Tooltip("den:Q", title="Quantidade"),
                ],
            )
            .properties(width=3000)
        )

        return bars

    
    def streamlit(self):
              
        st.set_page_config(
            page_title="Contagem postagem telegram",
            page_icon="📊",
            layout="wide",  # Alternativas: 'centered' ou 'wide'
        )

        st.image(
                    "ico.jpg",  # Caminho para a imagem
                    width=100,
                    #use_container_width=False,
                
                )

        with st.sidebar:
                
                filter_coordenador = st.multiselect(
                    "Escolha os coordenadores",
                    self.df["first_name_telegram"].unique(),
                    default=self.df["first_name_telegram"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_dia = st.multiselect(
                    "Escolha dias",
                    self.df["dia"].unique(),
                    default=self.df["dia"].unique()  # Seleciona todos os status por padrão
                    
                )

                filter_mes = st.multiselect(
                    "Escolha os meses",
                    self.df["mes"].unique(),
                    default=self.df["mes"].unique()  # Seleciona todos os status por padrão
                    
                )

                
        
        if not filter_coordenador:
                st.error("Por favor, selecione pelo menos um filtro.")

        else:
             # Filtrar os dados com base nas seleções
                df_filter_prioridade = self.df[
                    
                    (self.df["first_name_telegram"].isin(filter_coordenador))&
                    (self.df["dia"].isin(filter_dia))&
                    (self.df["mes"].isin(filter_mes))
                   
                    #(df_resultado_coord_area["Coordenador de campo"].isin(filter_coord_campo))
                ]
         #dia da semana
        #regiao
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e Região</p>', unsafe_allow_html=True)
        chart_regiao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='regiao')
        st.altair_chart(chart_regiao, use_container_width=True)
        #uf
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e UF</p>', unsafe_allow_html=True)
        chart_uf = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='uf')
        st.altair_chart(chart_uf, use_container_width=True)
        #dia da semana
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e dia da semana</p>', unsafe_allow_html=True)
        chart_diaSemana = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='nome_dia_abertura')
        st.altair_chart(chart_diaSemana, use_container_width=True)
        #descriçaõ
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e descricao</p>', unsafe_allow_html=True)
        chart_descricao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='breve_descr_problema')
        st.altair_chart(chart_descricao, use_container_width=True)
        #Cos
        st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e cos</p>', unsafe_allow_html=True)
        chart_cos = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='Cos')
        st.altair_chart(chart_cos, use_container_width=True)
        #Est.
        #st.markdown('<p style="font-size:30px; font-weight:bold;">Prioridade e estação</p>', unsafe_allow_html=True)
        #chart_estacao = self.grafico_barras_prioridade_diaDaSemanaAbertura(data_chart=df_filter_prioridade,nome_x='prioridade_ba',nome_y='Est.')
        #st.altair_chart(chart_estacao, use_container_width=True)
        
        
       
        st.dataframe(df_filter_prioridade, width=4000) 

       

 
def main():
    
    
    execute = Dashboard()
    execute.streamlit()
    
  
    
   

if __name__=='__main__':
    main()

    #streamlit run ponto_st.py