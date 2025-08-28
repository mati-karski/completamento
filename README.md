# Generatore di quesiti Cloze (a completamento) da PDF tramite API OpenAI

Questa applicazione genera automaticamente **quesiti a completamento (Cloze)** a partire da PDF di slide o appunti, sfruttando modelli LLM (come OpenAI o OpenRouter) tramite API.  

L’interfaccia è realizzata con Streamlit e permette agli insegnanti o formatori di creare in pochi clic batterie di esercizi didattici di alta qualità.

## Funzionalità principali

- Caricamento di PDF (slide, appunti, dispense)
- Estrazione automatica del testo slide per slide
- Generazione di quesiti Cloze *univoci e didattici* via modello LLM (API OpenAI/OpenRouter)
- Configurazione personalizzabile (numero quesiti, temperatura, modello usato)
- Download diretto dei quesiti in formato Markdown
- Interfaccia semplice, intuitiva e pronta per l’utilizzo didattico

## Tecnologie

- [Streamlit](https://streamlit.io/) per la UI
- [OpenAI Python SDK](https://pypi.org/project/openai/) e/o OpenRouter
- [pypdf](https://pypdf.readthedocs.io/en/latest/) per parsing PDF

## Utilizzo

1. Carica il tuo PDF di slide.
2. Scegli i parametri per la generazione dei quesiti.
3. Ottieni ed esporta i Cloze per i tuoi quiz!

## Requisiti

- Chiave API (openai/openrouter)
- Python 3.9+

## Licenza

MIT
