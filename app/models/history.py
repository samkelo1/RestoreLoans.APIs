from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base

class StatementHistory(Base):
    __tablename__ = "statement_history"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=True)
    statement_type = Column(String(200), nullable=False)  # 'application' or 'financial'
    statement_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    file_path = Column(String(200), nullable=False)