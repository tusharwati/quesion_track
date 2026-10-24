import json
import os
from typing import List, Dict, Optional
import structlog
from rapidfuzz import fuzz, process
from app.core.config import settings


logger = structlog.get_logger()


class GlossaryService:
    def __init__(self, glossary_path: str = "backend/data/technical_terms.json"):
        self.glossary_path = glossary_path
        self.terms: Dict[str, bool] = {}  # term -> case_sensitive
        self._load_glossary()
    
    def _load_glossary(self):
        """Load technical terms from JSON file."""
        try:
            if os.path.exists(self.glossary_path):
                with open(self.glossary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for term_obj in data.get("terms", []):
                        term = term_obj["term"]
                        case_sensitive = term_obj.get("case_sensitive", True)
                        self.terms[term] = case_sensitive
                logger.info("Loaded technical terms glossary", count=len(self.terms))
            else:
                logger.warning("Glossary file not found, using empty glossary", path=self.glossary_path)
        except Exception as e:
            logger.error("Failed to load glossary", error=str(e))
            self.terms = {}
    
    def add_term(self, term: str, case_sensitive: bool = True):
        """Add a new term to the glossary."""
        self.terms[term] = case_sensitive
        self._save_glossary()
    
    def remove_term(self, term: str):
        """Remove a term from the glossary."""
        if term in self.terms:
            del self.terms[term]
            self._save_glossary()
    
    def _save_glossary(self):
        """Save glossary back to JSON file."""
        try:
            data = {
                "version": "1.0",
                "terms": [
                    {"term": term, "case_sensitive": cs}
                    for term, cs in self.terms.items()
                ]
            }
            os.makedirs(os.path.dirname(self.glossary_path), exist_ok=True)
            with open(self.glossary_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error("Failed to save glossary", error=str(e))
    
    def import_terms_from_file(self, file_path: str) -> int:
        """
        Import terms from a text/markdown file.
        Returns count of terms imported.
        """
        count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#') or line.startswith('//'):
                        continue
                    # Handle markdown headers and lists
                    if line.startswith('##'):
                        continue
                    if line.startswith('- ') or line.startswith('* '):
                        line = line[2:].strip()
                    if line and line not in self.terms:
                        self.terms[line] = True
                        count += 1
            
            self._save_glossary()
            logger.info("Imported terms from file", file=file_path, count=count)
            return count
            
        except Exception as e:
            logger.error("Failed to import terms", error=str(e), file=file_path)
            return 0
    
    def correct_text(self, text: str, threshold: int = 85) -> str:
        """
        Correct text using fuzzy matching against glossary terms.
        
        Args:
            text: Input text to correct
            threshold: Minimum fuzzy match score (0-100)
            
        Returns:
            Corrected text
        """
        if not self.terms:
            return text
        
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Check for exact match first
            if word in self.terms:
                corrected_words.append(word)
                continue
            
            # Check case-insensitive exact match
            for term, case_sensitive in self.terms.items():
                if not case_sensitive and word.lower() == term.lower():
                    corrected_words.append(term)
                    break
            else:
                # Fuzzy match
                best_match = None
                best_score = 0
                
                for term in self.terms.keys():
                    # Try to match against the word
                    score = fuzz.ratio(word.lower(), term.lower())
                    if score > best_score and score >= threshold:
                        best_score = score
                        best_match = term
                
                if best_match:
                    corrected_words.append(best_match)
                else:
                    corrected_words.append(word)
        
        return " ".join(corrected_words)
    
    def get_all_terms(self) -> List[Dict[str, any]]:
        """Get all terms in the glossary."""
        return [
            {"term": term, "case_sensitive": cs}
            for term, cs in self.terms.items()
        ]
