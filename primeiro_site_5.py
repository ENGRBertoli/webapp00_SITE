# -*- coding: utf-8 -*-
"""primeiro site 5

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1O7DkynQ3PAy93ItDmYc058F2pRmUbOZ-
"""

import streamlit as st
import matplotlib.pyplot as plt
import pickle
import os

# Caminho do arquivo para salvar os dados
DATA_FILE = "balancas_data.pkl"

# Função para carregar os dados
def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as file:
            return pickle.load(file)
    return []

# Função para salvar os dados
def salvar_dados(dados):
    with open(DATA_FILE, "wb") as file:
        pickle.dump(dados, file)

# Lista para armazenar as balanças (carrega do arquivo)
balancas = carregar_dados()

# Função para obter a cor do status
def obter_cor_status(status):
    cores = {
        "Em produção": "orange",
        "Indisponível": "red",
        "Disponível para venda": "green",
        "Vendido": "blue"
    }
    return cores.get(status, "black")

# Função para exibir gráfico de barras horizontais
def Grafico_Barra_Status(Rotulos, Quantidades, Largura=10, Altura=7, Titulo_Grafico='Gráfico de Status'):
    fig, ax = plt.subplots(figsize=(Largura, Altura))
    colors = [obter_cor_status(r) for r in Rotulos]
    bars = ax.barh(Rotulos, Quantidades, color=colors)
    ax.set_xlabel('Quantidade')
    ax.set_ylabel('Status')
    ax.set_title(Titulo_Grafico)

    for bar, value in zip(bars, Quantidades):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}', ha='left', va='center')

    st.pyplot(fig)

# Função principal do app
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
        quantidade = st.number_input("Quantidade total:", min_value=0, step=1)
        if st.button("Adicionar"):
            nova_balanca = {
                "modelo": modelo,
                "quantidade_total": quantidade,
                "status_quantidades": {
                    "Em produção": quantidade,
                    "Indisponível": 0,
                    "Disponível para venda": 0,
                    "Vendido": 0
                }
            }
            balancas.append(nova_balanca)
            salvar_dados(balancas)  # Salva os dados no arquivo
            st.success(f"Balança '{modelo}' adicionada com quantidade total de {quantidade}.")

    elif menu == "Listar Balanças":
        st.subheader("Balanças cadastradas")
        if not balancas:
            st.warning("Nenhuma balança cadastrada.")
        else:
            for idx, balanca in enumerate(balancas):
                st.markdown(f"### Modelo: {balanca['modelo']}")
                st.write(f"**Quantidade Total:** {balanca['quantidade_total']}")

                # Ajustar quantidades por status
                for status, quantidade in balanca["status_quantidades"].items():
                    nova_quantidade = st.number_input(
                        f"Quantidade em '{status}' para {balanca['modelo']}:",
                        min_value=0,
                        max_value=balanca['quantidade_total'],
                        value=quantidade,
                        step=1,
                        key=f"{balanca['modelo']}_{status}"
                    )
                    balanca["status_quantidades"][status] = nova_quantidade

                # Verifica se a soma das quantidades por status é válida
                soma_quantidades = sum(balanca["status_quantidades"].values())
                if soma_quantidades > balanca["quantidade_total"]:
                    st.error(f"As quantidades excedem o total de {balanca['quantidade_total']}. Ajuste os valores.")
                elif soma_quantidades < balanca["quantidade_total"]:
                    st.warning(f"As quantidades somadas são menores que o total. Total esperado: {balanca['quantidade_total']}.")
                else:
                    salvar_dados(balancas)  # Salva alterações no arquivo
                    st.success(f"As quantidades para '{balanca['modelo']}' foram atualizadas.")

    elif menu == "Gráficos":
        st.subheader("Gráficos das balanças")
        if not balancas:
            st.warning("Nenhuma balança cadastrada para exibir nos gráficos.")
        else:
            for balanca in balancas:
                st.markdown(f"### Gráfico de Status para {balanca['modelo']}")
                Grafico_Barra_Status(
                    list(balanca["status_quantidades"].keys()),
                    list(balanca["status_quantidades"].values()),
                    Largura=10,
                    Altura=7,
                    Titulo_Grafico=f"Status do Modelo {balanca['modelo']}"
                )

if __name__ == "__main__":
    main()