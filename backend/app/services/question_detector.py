import re
from typing import Tuple, List
import structlog


logger = structlog.get_logger()


class QuestionDetector:
    """
    Detects questions from text using keyword matching and linguistic patterns.
    """
    
    QUESTION_STARTERS = {
        'what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 'whose',
        'can', 'could', 'would', 'should', 'will', 'shall', 'may', 'might', 'must',
        'did', 'do', 'does', 'did', 'is', 'are', 'was', 'were', 'am',
        'have', 'has', 'had', 'will have',
        'explain', 'describe', 'tell me', 'clarify', 'define', 'list', 'name',
        'give me', 'show me', 'help me understand'
    }
    
    QUESTION_ENDINGS = {
        '?', 'right', 'correct', 'isn\'t it', 'doesn\'t it', 'won\'t it',
        'can\'t you', 'couldn\'t you', 'wouldn\'t you', 'shouldn\'t you',
        'don\'t you', 'aren\'t you', 'haven\'t you'
    }
    
    def __init__(self):
        # Compile regex patterns for efficiency
        self.starter_pattern = re.compile(
            r'^(' + '|'.join(re.escape(s) for s in sorted(self.QUESTION_STARTERS, key=len, reverse=True)) + r')\b',
            re.IGNORECASE
        )
        
        self.ending_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(e) for e in sorted(self.QUESTION_ENDINGS, key=len, reverse=True)) + r')\s*$',
            re.IGNORECASE
        )
    
    def detect(self, text: str) -> Tuple[bool, float]:
        """
        Detect if the text is a question.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (is_question, confidence)
        """
        if not text or not text.strip():
            return False, 0.0
        
        text_lower = text.lower().strip()
        confidence = 0.0
        signals = []
        
        # Check for question mark
        if '?' in text:
            signals.append(('question_mark', 0.9))
        
        # Check for question word at start
        if self.starter_pattern.match(text):
            signals.append(('starter', 0.8))
        
        # Check for question-ending phrases
        if self.ending_pattern.search(text):
            signals.append(('ending', 0.7))
        
        # Check for subject-verb inversion (e.g., "Are you...", "Have they...")
        inversion_pattern = re.match(r'^(is|are|was|were|am|have|has|had|do|does|did|can|could|would|should|will|shall|may|might|must)\s+\w+', text_lower)
        if inversion_pattern:
            signals.append(('inversion', 0.85))
        
        # Check for "tell me", "explain", etc. as commands
        command_pattern = re.match(r'^(tell me|explain|describe|clarify|define|list|name|give me|show me|help me understand)', text_lower)
        if command_pattern:
            signals.append(('command', 0.75))
        
        # Calculate confidence
        if signals:
            # Weight signals by type
            weighted_sum = sum(weight for _, weight in signals)
            # Normalize to 0-1 range
            confidence = min(weighted_sum / len(signals), 1.0)
        
        is_question = confidence >= 0.6
        
        logger.debug(
            "Question detection",
            is_question=is_question,
            confidence=confidence,
            signals=[s[0] for s in signals]
        )
        
        return is_question, round(confidence, 2)
    
    def correct_question(self, text: str) -> str:
        """
        Correct the grammar and punctuation of a detected question.
        
        Args:
            text: Input question text
            
        Returns:
            Corrected question text
        """
        if not text:
            return text
        
        # Capitalize first letter
        corrected = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        # Add question mark if not present
        if not corrected.strip().endswith('?'):
            corrected = corrected.rstrip() + '?'
        
        # Remove multiple question marks
        corrected = re.sub(r'\?+', '?', corrected)
        
        # Fix spacing before punctuation
        corrected = re.sub(r'\s+([?.,!])', r'\1', corrected)
        
        # Capitalize "I" when standing alone
        corrected = re.sub(r'\bi\b', 'I', corrected)
        
        # Fix common speech-to-text errors
        corrections = {
            r'\byou only\b': 'YOLO',
            r'\bi\s+o\b': 'I/O',
            r'\bc\s*\+\s*\+\b': 'C++',
            r'\bc\s*#\b': 'C#',
        }
        
        for pattern, replacement in corrections.items():
            corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)
        
        return corrected


# Singleton instance
question_detector = QuestionDetector()
