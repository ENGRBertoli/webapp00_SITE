import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Lista para armazenar as balanças
balancas = []

def Grafico_Pizza(Rotulos, Quantias, Legenda, posExplode=0, LocLEG="upper left", Larg=8, Alt=5, Titulo_Grafico='Gráfico de Pizza', Titulo_legenda='Legenda'):
    fig, ax = plt.subplots(figsize=(Larg, Alt))
    explode = [0.1 if i == posExplode else 0 for i in range(len(Rotulos))]
    ax.pie(Quantias, explode=explode, labels=Legenda, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Garantir que o gráfico seja um círculo
    ax.set_title(Titulo_Grafico)
    ax.legend(title=Titulo_legenda, loc=LocLEG, bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig)

def Grafico_Barra_Horizontal(Rotulos, Quantias, Largura=8, Altura=5, Titulo_Grafico='Gráfico de Barra', Titulo_x='Quantidade', Titulo_y='Modelos'):
    fig, ax = plt.subplots(figsize=(Largura, Altura))
    bars = ax.barh(Rotulos, Quantias, color='skyblue')
    ax.set_ylabel(Titulo_y)
    ax.set_xlabel(Titulo_x)
    ax.set_title(Titulo_Grafico)
    for bar, value in zip(bars, Quantias):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}', ha='left', va='center')
    st.pyplot(fig)

def main():
    st.set_page_config(
        page_title="Painel de Gestão de Balanças",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Painel de Gestão de Fabricação de Balanças")
    
    # Menu lateral
    menu = st.sidebar.radio("Escolha uma opção:", ["Adicionar Balança", "Listar Balanças", "Gráficos"])
    
    if menu == "Adicionar Balança":
        st.subheader("Adicionar uma nova balança")
        modelo = st.text_input("Modelo da balança:")
        quantidade = st.number_input("Quantidade:", min_value=0, step=1)
        if st.button("Adicionar"):
            nova_balanca = {"modelo": modelo, "quantidade": quantidade, "status": "Em produção"}
            balancas.append(nova_balanca)
            st.success(f"Balança '{modelo}' adicionada com quantidade {quantidade}.")
    
    elif menu == "Listar Balanças":
        st.subheader("Balanças cadastradas")
        if not balancas:
            st.warning("Nenhuma balança cadastrada.")
        else:
            for balanca in balancas:
                st.write(f"**Modelo:** {balanca['modelo']} | **Quantidade:** {balanca['quantidade']} | **Status:** {balanca['status']}")

    elif menu == "Gráficos":
        st.subheader("Gráficos das balanças")
        if not balancas:
            st.warning("Nenhuma balança cadastrada para exibir nos gráficos.")
        else:
            modelos = [b["modelo"] for b in balancas]
            quantidades = [b["quantidade"] for b in balancas]

            col1, col2 = st.columns(2)
            with col1:
                Grafico_Pizza(modelos, quantidades, modelos, 0, "upper left", 8, 5, Titulo_Grafico="Distribuição de Balanças", Titulo_legenda="Modelos")
            with col2:
                Grafico_Barra_Horizontal(modelos, quantidades, Largura=8, Altura=5, Titulo_Grafico="Estoque de Balanças", Titulo_x="Quantidade", Titulo_y="Modelos")

if __name__ == "__main__":
    main()
