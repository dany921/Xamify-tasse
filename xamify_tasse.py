
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Xamify Tasse", layout="centered")

# CSS migliorato con pulsanti celesti
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        color: #111827;
    }
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 10px;
    }
    h2 {
        text-align: center;
        color: #009999;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #00cccc !important;
        color: #ffffff !important;
        border: none;
        padding: 0.5em 2em;
        border-radius: 20px;
        font-weight: bold;
    }
    .entry-card {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .entry-left {
        display: flex;
        flex-direction: column;
        font-size: 15px;
    }
    .entry-amount {
        font-weight: bold;
        font-size: 18px;
        text-align: right;
        color: #00cccc;
    }
    .metric-box {
        background-color: #f1f5f9;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 14px;
        color: #6b7280;
    }
    .metric-value {
        font-size: 20px;
        font-weight: bold;
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)

st.image("xamify-logo.png", width=90)
st.markdown("## Xamify Tasse – Calcolatore Forfettario")

if "movimenti" not in st.session_state:
    st.session_state.movimenti = []
if "tab" not in st.session_state:
    st.session_state.tab = "Entrata"

col1, col2 = st.columns(2)
with col1:
    if st.button("Entrate"):
        st.session_state.tab = "Entrata"
with col2:
    if st.button("Spese"):
        st.session_state.tab = "Spesa"

with st.expander("➕ Aggiungi nuovo movimento"):
    with st.form("aggiungi"):
        tipo = st.selectbox("Tipo", ["Entrata", "Spesa"], index=0 if st.session_state.tab == "Entrata" else 1)
        cliente = st.text_input("Cliente / Causale")
        importo = st.number_input("Importo (€)", step=1.0, min_value=0.0)
        data = st.date_input("Data", value=datetime.today())
        if st.form_submit_button("Aggiungi"):
            st.session_state.movimenti.append({
                "tipo": tipo,
                "cliente": cliente,
                "importo": importo,
                "data": data
            })
            st.success("Movimento aggiunto!")

st.markdown(f"### 📋 Entrate registrate" if st.session_state.tab == "Entrata" else "### 📋 Spese registrate")

for i, m in reversed(list(enumerate([x for x in st.session_state.movimenti if x['tipo'] == st.session_state.tab]))):
    col1, col2 = st.columns([5,1])
    with col1:
        st.markdown(f'''
        <div class="entry-card">
            <div class="entry-left">
                <div><strong>{m['cliente']}</strong> – {m['data']}</div>
            </div>
            <div class="entry-amount">{'-' if m['tipo']=='Spesa' else '+'}{m['importo']:,.2f} €</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        if st.button("🗑", key=f"del_{i}"):
            st.session_state.movimenti.remove(m)
            st.experimental_rerun()

# Calcolo tasse
st.markdown("### 📊 Simulazione Fiscale")

COEFF = 0.40
IMPOSTA_5 = 0.05
INPS_FISSO = 2214
INPS_SOGLIA = 18415
INPS_VAR = 0.12

entrate = sum(x["importo"] for x in st.session_state.movimenti if x["tipo"] == "Entrata")
spese = sum(x["importo"] for x in st.session_state.movimenti if x["tipo"] == "Spesa")
reddito_imponibile = entrate * COEFF
eccedenza = max(0, reddito_imponibile - INPS_SOGLIA)
inps = INPS_FISSO + (eccedenza * INPS_VAR)
imposta = reddito_imponibile * IMPOSTA_5
tasse = inps + imposta
netto = entrate - spese - tasse

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Entrate</div><div class="metric-value">{entrate:,.2f} €</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><div class="metric-label">Spese</div><div class="metric-value">{spese:,.2f} €</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Tasse totali</div><div class="metric-value">{tasse:,.2f} €</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><div class="metric-label">Netto disponibile</div><div class="metric-value">{netto:,.2f} €</div></div>', unsafe_allow_html=True)
