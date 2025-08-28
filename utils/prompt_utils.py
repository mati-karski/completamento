import os

PROMPTS_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'prompts')
)

def load_system_prompt():
    """Legge il prompt system da file statico."""
    system_path = os.path.join(PROMPTS_DIR, "system_prompt.txt")
    with open(system_path, 'r', encoding='utf-8') as f:
        return f.read()

def build_system_prompt():
    """
    Wrapper per uniformità con build_user_prompt().
    Ritorna il system prompt statico.
    """
    return load_system_prompt()

def build_user_prompt(slides_text: str, numero_quesiti: int, **kwargs):
    """
    Carica e formatta user_prompt.txt con i parametri forniti.
    - slides_text: testo delle slide
    - numero_quesiti: numero minimo di quesiti
    Altri parametri possono essere passati come kwargs per placeholder extra.
    """
    user_path = os.path.join(PROMPTS_DIR, "user_prompt.txt")
    with open(user_path, 'r', encoding='utf-8') as f:
        template = f.read()
    # Usa .format() per sostituire i placeholder nel template
    # (Gestisce eventuali altri placeholder aggiunti)
    return template.format(
        slides_text=slides_text, 
        numero_quesiti=numero_quesiti,
        **kwargs
    )
