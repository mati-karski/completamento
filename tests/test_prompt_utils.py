from utils.prompt_utils import build_user_prompt

def test_build_user_prompt_basic():
    content = build_user_prompt("testo delle slide", 3)
    assert "testo delle slide" in content
    assert "3" in content
