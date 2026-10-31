from app.services.safety import may_be_crisis

def test_detects_direct_self_harm_phrases():
    assert may_be_crisis("I want to kill myself")
    assert may_be_crisis("I want to end my life")

def test_ordinary_stress_is_not_keyword_flagged():
    assert not may_be_crisis("I am stressed about my exam tomorrow")
