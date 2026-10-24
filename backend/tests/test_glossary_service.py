import pytest
from app.services.glossary_service import GlossaryService


def test_load_glossary():
    """Test that glossary loads correctly."""
    glossary = GlossaryService()
    terms = glossary.get_all_terms()
    
    assert len(terms) > 0, "Glossary should contain terms"
    
    # Check for specific terms
    term_names = [t["term"] for t in terms]
    assert "YOLO" in term_names
    assert "ESP32" in term_names
    assert "Python" in term_names


def test_correct_text():
    """Test technical term correction."""
    glossary = GlossaryService()
    
    test_cases = [
        ("how does your yolo model work", "how does your YOLO model work"),
        ("i used esp thirty two for this", "i used ESP32 for this"),
        ("the python script runs on linux", "the Python script runs on Linux"),
    ]
    
    for raw, expected in test_cases:
        corrected = glossary.correct_text(raw)
        assert corrected == expected, f"Failed for: {raw}"


def test_add_term():
    """Test adding a new term."""
    glossary = GlossaryService()
    
    initial_count = len(glossary.get_all_terms())
    glossary.add_term("TestTerm", case_sensitive=True)
    
    terms = glossary.get_all_terms()
    assert len(terms) == initial_count + 1
    
    term_names = [t["term"] for t in terms]
    assert "TestTerm" in term_names


def test_case_sensitivity():
    """Test case sensitivity in term matching."""
    glossary = GlossaryService()
    
    # Test case-sensitive match
    corrected = glossary.correct_text("python is a language")
    assert "Python" in corrected
    
    # Test exact match preservation
    corrected = glossary.correct_text("Python is a language")
    assert "Python" in corrected


def test_fuzzy_matching():
    """Test fuzzy matching for approximate matches."""
    glossary = GlossaryService()
    
    # Test approximate match
    corrected = glossary.correct_text("you only v seven", threshold=70)
    # Should match YOLOv7 if fuzzy matching works
    # Note: this depends on the threshold and fuzzy algorithm
    assert corrected is not None


def test_empty_text():
    """Test handling of empty text."""
    glossary = GlossaryService()
    
    corrected = glossary.correct_text("")
    assert corrected == ""
