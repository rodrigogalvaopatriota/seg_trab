from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route("/")
def index():
    # Ler o Excel
    df = pd.read_excel("result_geral.xlsx")

    # Garantir que a coluna dia seja data
    df["dia"] = pd.to_datetime(df["dia"])

    # Agrupar por dia e contar quantos first_name_telegram existem
    df_grouped = df.groupby("dia")["first_name_telegram"].count().reset_index()
    df_grouped.rename(columns={"first_name_telegram": "quantidade"}, inplace=True)

    # Criar gráfico interativo com Plotly
    fig = px.line(
        df_grouped,
        x="dia",
        y="quantidade",
        title="Quantidade de usuários por dia",
        labels={"dia": "Dia", "quantidade": "Quantidade"}
    )

    # Converter gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Renderizar página
    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
