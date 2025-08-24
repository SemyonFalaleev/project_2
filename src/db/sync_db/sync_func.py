from src.db.sync_db.init_db_sync import SessionLocal
from datetime import datetime
from datetime import timedelta
from src.db.models import User
from sqlalchemy import delete


def _delete_unconfirmed_users():
    with SessionLocal() as session:
        threshold = datetime.now() - timedelta(days=1)

        stmt = delete(User).where(not User.is_active, User.created_at < threshold)

        session.execute(stmt)
        session.commit()
