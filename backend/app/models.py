from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import JSON

Base = declarative_base()


class Resource(Base):
    """SQLAlchemy model for resources."""

    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    eligibility = Column(Text)
    category = Column(String)
    service_type = Column(String)
    min_age = Column(Integer)
    max_age = Column(Integer)
    system = Column(String)
    counties = Column(JSON)
    insurance_types = Column(JSON)
    partners_involved = Column(JSON)
    tags = Column(JSON)
    associated_docs = Column(JSON)

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return f"<Resource id={self.id} name={self.name}>"
