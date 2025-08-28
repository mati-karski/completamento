import streamlit as st
from openai import OpenAI

def get_llm_config():
    """
    Restituisce modello e API key dalla configurazione (secrets.toml).
    Usa sezione 'openai' per chiave e nome modello.
    Gestisce eccezioni se mancano valori.
    """
    try:
        api_key = st.secrets["openai"]["key"]
        model = st.secrets["openai"]["model"]
    except KeyError as e:
        raise RuntimeError(f"Manca la voce nei secrets.toml: {e}")
    return api_key, model

def make_client(api_key: str) -> OpenAI:
    """
    Istanzia e ritorna un client OpenAI/OpenRouter.
    """
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

def call_model(client, model: str, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int):
    """
    Effettua una chiamata al modello con i parametri forniti.
    Ritorna la risposta generata.
    """
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as e:
        raise RuntimeError(f"Errore nella chiamata al modello: {e}")
    
    if not resp.choices:
        raise RuntimeError("Nessuna risposta ricevuta dal modello")
    
    return resp.choices[0].message.content

