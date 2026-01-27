from sqlalchemy import create_engine, text
from app.core.config import get_settings
engine = create_engine(get_settings().SQLALCHEMY_DATABASE_URI)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DB connected:", result.scalar())
except Exception as e:
    print("❌ DB connection failed:", e)
