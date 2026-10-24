import pytest
from app.services.question_detector import question_detector


def test_detect_question_mark():
    """Test detection of questions with question marks."""
    is_question, confidence = question_detector.detect("What is your name?")
    assert is_question is True
    assert confidence >= 0.6


def test_detect_question_words():
    """Test detection of questions starting with question words."""
    test_cases = [
        ("How does this work", True),
        ("What is the purpose", True),
        ("Why did you choose this approach", True),
        ("When should we deploy", True),
        ("Where is the server", True),
        ("Which option is better", True),
        ("Who is responsible", True),
    ]
    
    for text, expected in test_cases:
        is_question, _ = question_detector.detect(text)
        assert is_question == expected, f"Failed for: {text}"


def test_detect_inversion():
    """Test detection of questions with subject-verb inversion."""
    test_cases = [
        ("Are you ready", True),
        ("Have you completed the task", True),
        ("Do you understand", True),
        ("Is the system working", True),
        ("Can you explain", True),
    ]
    
    for text, expected in test_cases:
        is_question, _ = question_detector.detect(text)
        assert is_question == expected, f"Failed for: {text}"


def test_detect_command_forms():
    """Test detection of questions with command forms."""
    test_cases = [
        ("Tell me about your project", True),
        ("Explain the architecture", True),
        ("Describe your approach", True),
        ("Clarify the requirements", True),
    ]
    
    for text, expected in test_cases:
        is_question, _ = question_detector.detect(text)
        assert is_question == expected, f"Failed for: {text}"


def test_detect_tag_questions():
    """Test detection of tag questions."""
    test_cases = [
        ("You're using YOLOv7, right?", True),
        ("The model is accurate, isn't it?", True),
        ("You've tested it, haven't you?", True),
    ]
    
    for text, expected in test_cases:
        is_question, _ = question_detector.detect(text)
        assert is_question == expected, f"Failed for: {text}"


def test_reject_statements():
    """Test that statements are not detected as questions."""
    test_cases = [
        ("The system is working correctly", False),
        ("I implemented the feature yesterday", False),
        ("We chose React for the frontend", False),
        ("The model achieved 95% accuracy", False),
    ]
    
    for text, expected in test_cases:
        is_question, _ = question_detector.detect(text)
        assert is_question == expected, f"Failed for: {text}"


def test_correct_question():
    """Test question correction functionality."""
    test_cases = [
        ("how does your yolo model work", "How does your YOLO model work?"),
        ("what is the api endpoint", "What is the API endpoint?"),
        ("explain your approach", "Explain your approach?"),
    ]
    
    for raw, expected in test_cases:
        corrected = question_detector.correct_question(raw)
        assert corrected == expected, f"Failed for: {raw}"


def test_empty_text():
    """Test handling of empty text."""
    is_question, confidence = question_detector.detect("")
    assert is_question is False
    assert confidence == 0.0
