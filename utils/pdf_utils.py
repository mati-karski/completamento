import io
from typing import List
from pypdf import PdfReader
import streamlit as st

@st.cache_data(show_spinner="Estrazione testo PDF in corso…")
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Estrae il testo da un file PDF (in bytes).
    Ogni pagina viene prefissata con '[Slide {n}]' per contesto.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for i, page in enumerate(reader.pages, 1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(f"[Slide {i}]\n{text}")
    return "\n\n".join(pages).strip()

def clean_pdf_text(text: str) -> str:
    """
    (Estendibile) Rimuove header/footer ripetuti, pulisce layout.
    Al momento ritorna il testo in input senza modifiche.
    """
    # Qui puoi aggiungere logiche di pulizia specifiche, se necessario.
    return text

def split_pdf_into_slides(text: str) -> List[str]:
    """
    Suddivide il testo estratto in blocchi slide.
    Utile se vuoi lavorare separatamente sulle singole slide.
    """
    slides = text.split("\n\n")
    return [slide.strip() for slide in slides if slide.strip()]
