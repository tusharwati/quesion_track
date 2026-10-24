from sqlalchemy import Column, String, Boolean, Integer
from app.database.base import Base


class TechnicalTerm(Base):
    __tablename__ = "technical_terms"
    
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False, unique=True, index=True)
    case_sensitive = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "term": self.term,
            "case_sensitive": self.case_sensitive
        }
