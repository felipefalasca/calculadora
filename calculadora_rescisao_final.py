
import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Calculadora de Custo de Rescisão", layout="wide")

# LOGO com nome sem espaço
st.image("logo_data4hr.png", width=240)

st.markdown("<h1 style='color:#7c3cda'>Calculadora de Custo de Rescisão</h1>", unsafe_allow_html=True)

if "resultado_total" not in st.session_state:
    st.session_state.resultado_total = {}

tab1, tab2 = st.tabs(["📝 Premissas", "📊 Resumo"])

with tab1:
    st.header("Premissas Gerais")
    col1, col2, col3 = st.columns(3)
    with col1:
        headcount = st.number_input("Headcount Ativo", value=1000)
        admissoes = st.number_input("Admissões em 2024", value=400)
        desligados_vol = st.number_input("Desligamentos Voluntários", value=200)
        desligados_invol = st.number_input("Desligamentos Involuntários", value=50)
        prazo_substituicao = st.number_input("Prazo Médio de Substituição (dias)", value=51)

    st.header("Verbas Rescisórias")
    col4, col5 = st.columns(2)
    with col4:
        assist_med = st.number_input("Assistência Médica", value=55)
        seguro_vida = st.number_input("Seguro de Vida", value=15)
        consignado = st.number_input("Consignado", value=40)
        outros = st.number_input("Outros", value=20)
    verba_media = assist_med + seguro_vida + consignado + outros

    st.header("Custos de Atração e Seleção")
    consultorias = st.number_input("Qtd vagas por consultoria", value=200)
    custo_vaga = st.number_input("Custo por vaga", value=500)
    orcamento_rs = st.number_input("Orçamento Time R&S", value=3000000)
    testes = st.number_input("Qtd Testes", value=200)
    val_teste = st.number_input("Valor por Teste", value=5)
    pesquisas = st.number_input("Qtd Pesquisas", value=200)
    val_pesq = st.number_input("Valor por Pesquisa", value=10)

    st.header("Outros Blocos")
    exames_adm = st.number_input("Qtd Exames ADM", value=80)
    val_exame = st.number_input("Valor por Exame ADM", value=60)

    horas_lider = st.number_input("Horas Liderança", value=800)
    jornada = st.number_input("Jornada Mensal", value=220)
    sal_lider = st.number_input("Salário Médio Liderança", value=7000)

    resultado_pronto = st.number_input("Resultado Colaborador Pronto", value=12000)
    resultado_admitido = st.number_input("Resultado Admitido Médio", value=7200)

    treinamentos = st.number_input("Qtd Treinamentos", value=5)
    val_treinamento = st.number_input("Valor Médio por Treinamento", value=235)
    investimento_treinamento = st.number_input("Investimento por Colaborador", value=1175)

    exames_dem = st.number_input("Qtd Exames DEM", value=4)
    val_exame_dem = st.number_input("Valor Exame DEM", value=32)

    outros_inv = st.number_input("Demais Investimentos por Colaborador", value=1635)

    # Cálculos principais
    verba_total = desligados_vol * verba_media
    atracao_total = (consultorias * custo_vaga) + orcamento_rs + (testes * val_teste + pesquisas * val_pesq)
    exame_adm_total = exames_adm * val_exame
    lideranca_total = horas_lider * (sal_lider / jornada)
    perda_aprend = (resultado_pronto - resultado_admitido) * desligados_vol
    treinamento_total = investimento_treinamento * desligados_vol
    perda_subst = (resultado_pronto / 30) * prazo_substituicao * desligados_vol
    exames_dem_total = exames_dem * val_exame_dem * desligados_vol
    outros_total = outros_inv * desligados_vol

    st.session_state.resultado_total = {
        "Verbas Rescisórias": verba_total,
        "Atração e Seleção": atracao_total,
        "Exames ADM": exame_adm_total,
        "Horas Liderança": lideranca_total,
        "Curva de Aprendizagem": perda_aprend,
        "Treinamento": treinamento_total,
        "Perda até Substituição": perda_subst,
        "Exames DEM": exames_dem_total,
        "Demais Investimentos": outros_total
    }

with tab2:
    st.header("Resumo Visual dos Custos Estimados")
    total_geral = sum(st.session_state.resultado_total.values())
    st.metric("Custo Total Estimado", f"R$ {total_geral:,.2f}")

    colunas = st.columns(3)
    for i, (label, valor) in enumerate(st.session_state.resultado_total.items()):
        with colunas[i % 3]:
            st.markdown(f"#### {label}")
            st.success(f"R$ {valor:,.2f}")

    st.markdown("---")
    if st.button("📄 Exportar Resumo em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Resumo de Custo de Rescisão - data4HR", ln=True, align="L")
        pdf.ln(5)

        for label, valor in st.session_state.resultado_total.items():
            pdf.cell(200, 8, txt=f"{label}: R$ {valor:,.2f}", ln=True)

        pdf.cell(200, 10, txt=f"Total Geral: R$ {total_geral:,.2f}", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        st.download_button(
            label="📥 Baixar PDF",
            data=buffer,
            file_name="resumo_rescisao_data4HR.pdf",
            mime="application/pdf"
        )
