from sqlalchemy import Column, String, Boolean, Integer
from app.database.base import Base


class Setting(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    
    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value
        }
