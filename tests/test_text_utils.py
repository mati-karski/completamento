from utils.text_utils import estimate_tokens, filter_valid_cloze_lines

def test_estimate_tokens_simple():
    text = "Questo è un semplice testo per il test."
    assert estimate_tokens(text) > 0

def test_filter_valid_cloze_lines():
    testo = """
    L'acqua è composta da due atomi di idrogeno e uno di _ossigeno_.
    L'acqua è composta da due atomi di idrogeno e uno di ossigeno.
    """
    lines = filter_valid_cloze_lines(testo)
    assert len(lines) == 1

def test_no_cloze_lines():
    lines = filter_valid_cloze_lines("Niente underscore qui!")
    assert lines == []
