from src.utils import text_reverse


def test_text_reverse():
    assert text_reverse("bank") == "knab"
    assert text_reverse("") == ""
    assert text_reverse("a") == "a"
