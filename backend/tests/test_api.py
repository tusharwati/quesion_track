import pytest
from fastapi.testclient import TestClient
import tempfile
import os


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "model_loaded" in data
    assert "database_connected" in data
    assert "version" in data


def test_get_settings(client):
    """Test getting settings."""
    response = client.get("/api/settings")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "stt_model" in data
    assert "language" in data
    assert "recent_question_count" in data


def test_update_settings(client):
    """Test updating settings."""
    new_settings = {
        "stt_model": "small",
        "recent_question_count": 3
    }
    
    response = client.put("/api/settings", json=new_settings)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["stt_model"] == "small"
    assert data["recent_question_count"] == 3


def test_list_questions_empty(client):
    """Test listing questions when empty."""
    response = client.get("/api/questions")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "questions" in data
    assert "total" in data
    assert isinstance(data["questions"], list)


def test_create_question(client):
    """Test creating a question."""
    response = client.post(
        "/api/questions",
        params={
            "raw_text": "how does yolo work",
            "corrected_text": "How does YOLO work?",
            "is_question": True,
            "confidence": 0.95,
            "processing_time": 1.2
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["raw_text"] == "how does yolo work"
    assert data["corrected_text"] == "How does YOLO work?"
    assert data["is_question"] is True


def test_delete_question(client):
    """Test deleting a question."""
    # Create a question first
    create_response = client.post(
        "/api/questions",
        params={
            "raw_text": "test question",
            "corrected_text": "Test question?",
            "is_question": True
        }
    )
    
    question_id = create_response.json()["id"]
    
    # Delete the question
    delete_response = client.delete(f"/api/questions/{question_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Question deleted successfully"


def test_clear_all_questions(client):
    """Test clearing all questions."""
    # Create some questions
    for i in range(3):
        client.post(
            "/api/questions",
            params={
                "raw_text": f"test question {i}",
                "corrected_text": f"Test question {i}?",
                "is_question": True
            }
        )
    
    # Clear all
    response = client.delete("/api/questions")
    
    assert response.status_code == 200
    assert "Cleared" in response.json()["message"]


def test_transcribe_invalid_file(client):
    """Test transcription with invalid file."""
    # Create a temporary text file (not audio)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is not an audio file")
        temp_path = f.name
    
    try:
        with open(temp_path, 'rb') as f:
            response = client.post(
                "/api/transcribe",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
    finally:
        os.unlink(temp_path)


def test_search_questions(client):
    """Test searching questions."""
    # Create questions with specific terms
    client.post(
        "/api/questions",
        params={
            "raw_text": "how does yolo work",
            "corrected_text": "How does YOLO work?",
            "is_question": True
        }
    )
    
    client.post(
        "/api/questions",
        params={
            "raw_text": "what is python",
            "corrected_text": "What is Python?",
            "is_question": True
        }
    )
    
    # Search for YOLO
    response = client.get("/api/questions", params={"search": "YOLO"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Should find at least one question with YOLO
    assert data["total"] >= 1
    assert any("YOLO" in q["corrected_text"] for q in data["questions"])
