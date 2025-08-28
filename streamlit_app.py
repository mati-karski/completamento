import io, re, streamlit as st
from typing import List
from pypdf import PdfReader
from streamlit_pdf_reader import pdf_reader
from openai import OpenAI
import logging


from utils.prompt_utils import build_system_prompt, build_user_prompt
from utils.pdf_utils import extract_text_from_pdf
from utils.llm_utils import get_llm_config, make_client, call_model
from utils.text_utils import count_words, estimate_tokens, filter_valid_cloze_lines


# ---------------- Config & costanti ----------------
MAX_TOKENS = 2048

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- Client (OpenAI SDK) ----------------
api_key, model = get_llm_config()

# ---------------- UI ----------------
#from PIL import Image
# Loading Image using PIL
#im = Image.open('/content/App_Icon.png')
# Adding Image to web app
#st.set_page_config(page_title="Surge Price Prediction App", page_icon = im)

st.set_page_config(
    page_title="Generatore cloze da PDF",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Elimina main menu, footer e icona anchor
st.markdown("""
    <style>
        a.header-anchor {
            display: none !important;
        }
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("Impostazioni generazione")
    st.markdown("Crea automaticamente esercizi cloze da slide PDF 🧑‍🏫")
    with st.expander("Come funziona?"):
        st.markdown("""
        1. Carica un file PDF con le slide.
        2. Anteprima e verifica del testo estratto.
        3. Genera i quesiti cloze automatici.
        4. Scarica i risultati per usarli nei tuoi quiz!
        """)
    st.divider()
    temperature = st.slider("Creatività (temperature)", 0.0, 1.0, value=0.2, step=0.05)
    numero_quesiti = st.number_input("Quesiti (indicativo)", min_value=10, max_value=50, value=30, step=1)


st.title("Generatore cloze da PDF")

st.markdown(
    "Genera rapidamente quesiti a completamento (cloze) di qualità didattica per quiz, prove, autocorrezione. "
    "Carica un PDF di slide o appunti, verifica il testo estratto, configura le impostazioni e genera la batteria di quesiti."
)

st.subheader("🔹 1. Carica e visualizza il PDF")
uploaded = st.file_uploader("Trascina o seleziona file PDF delle slide:", type=["pdf"])
if uploaded:
    # Preview
    st.subheader("🔹 2. Anteprima del documento")
    try: 
        pdf_reader(uploaded)
    except Exception as e: 
        st.warning(f"Viewer non disponibile: {e}")

    # Estrazione (memo su cambio file)
    if "pdf_bytes" not in st.session_state or st.session_state.get("pdf_name") != uploaded.name:
        st.session_state.pdf_bytes = uploaded.read()
        st.session_state.pdf_name = uploaded.name
        logger.info(f"Caricato PDF: {uploaded.name}, {len(st.session_state.pdf_bytes)} bytes")
        try:
            logger.info(f"Caricamento nuovo PDF: {uploaded.name}, {len(st.session_state.pdf_bytes)} bytes")
            st.session_state.raw_text = extract_text_from_pdf(st.session_state.pdf_bytes)
            logger.info(f"Estrazione testo da {uploaded.name} completata, {len(st.session_state.raw_text)} caratteri")
        except Exception as e:
            logger.error(f"Errore nell'estrazione testo PDF: {e}")
            st.session_state.raw_text = ""
        st.session_state.output_raw = ""
        st.session_state.output_lines = []

    text = st.session_state.raw_text

    st.markdown("**Statistiche**")
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📝 Parole: **{count_words(text)}**")
    with col2:
        st.caption(f"🔢 Token stimati: **{estimate_tokens(text)}**")
        
    with st.expander("Mostra testo estratto dalle slide"):
        st.text_area("Testo estratto (editabile per correzioni manuali):", text, height=250)

    st.subheader("🔹 3. Genera quesiti a completamento")
    st.markdown("Configura i parametri nella sidebar ➡️ e premi *Genera* per avviare la creazione dei quesiti.")
    disabled = not text

    btn_col, info_col = st.columns([1,3])
    with btn_col:
        genera = st.button("🚀 Genera", type="primary", disabled=disabled)
    with info_col:
        if disabled:
            st.info("Carica un PDF per abilitare la generazione.")

    if genera:
        # TODO: gestire limiti token (chunking in futuro)
        client = make_client(api_key)
        sys_p = build_system_prompt()
        usr_p = build_user_prompt(text, numero_quesiti)
        logger.info(f"Chiamata LLM: model={model}, temp={temperature}, n_quesiti={numero_quesiti}, tokens={MAX_TOKENS}")
        with st.spinner("Generazione quesiti in corso..."):
            try:
                raw = call_model(client, model, sys_p, usr_p, temperature, max_tokens=MAX_TOKENS)
                lines = filter_valid_cloze_lines(raw)
                st.session_state.output_raw = raw
                st.session_state.output_lines = lines
                logger.info(f"Risposte LLM ottenute: {len(lines)} quesiti estratti.")
            except Exception as e:
                st.error(f"Errore: {e}")
                logger.error(f"Errore nella chiamata LLM: {e}")
                st.session_state.output_raw = ""
                st.session_state.output_lines = []

    # --- RISULTATI ---
    if "output_raw" in st.session_state and (st.session_state.output_raw or st.session_state.output_lines):
        st.subheader("🔹 4. Risultati e download")

        tab1, tab2 = st.tabs(["👓 Quesiti puliti", "🪲 Output grezzo (debug)"])

        with tab1:
            if st.session_state.get("output_lines"):
                md = "\n".join(st.session_state.output_lines)
                st.markdown("### Quesiti Cloze estratti")
                st.code(md, language="markdown")
                st.success(f"{len(st.session_state.output_lines)} quesiti trovati. Scarica i risultati qui sotto!")
                st.download_button("⬇️ Scarica Markdown", data=md, file_name="quesiti_cloze.md", mime="text/markdown")
            else:
                st.warning("Nessuna riga valida con lacuna trovata. 🌱 Prova con temperature più bassa o rivedi il prompt.")
                logger.warning("Nessuna riga valida trovata nella risposta LLM.")

        with tab2:
            if st.session_state.output_raw:
                st.markdown("### Output grezzo (risposta LLM)")
                st.code(st.session_state.output_raw, language="markdown")
            else:
                st.info("Nessun output grezzo disponibile.")
