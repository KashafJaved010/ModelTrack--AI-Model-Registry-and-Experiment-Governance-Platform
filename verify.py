"""Optional smoke test — run after install.

    python verify.py

Checks:
  1. Registry has exactly 40 models
  2. SQLAlchemy metadata has exactly 40 tables
  3. db.create_all() succeeds
  4. Soft delete sets flags without removing the row
  5. Transaction rollback discards pending inserts on exception
"""
import sys

from app import create_app
from app.extensions import db
from app.models.registry import MODEL_REGISTRY
from app.models.data import Tag


def main():
    print("[0] starting verification...")
    app = create_app()
    with app.app_context():
        n_reg = len(MODEL_REGISTRY)
        n_meta = len(db.metadata.tables)
        print(f"[1] registry size: {n_reg} (expected 40)")
        print(f"[2] metadata size: {n_meta} (expected 40)")
        if n_reg != 40 or n_meta != 40:
            print("FAIL: model count mismatch")
            return 1

        db.create_all()
        print("[3] db.create_all() OK")

        # Soft delete test
        t = Tag(name="_verify_temp", created_by=1)
        db.session.add(t)
        db.session.commit()
        tid = t.id
        t.soft_delete(user_id=1)
        db.session.commit()
        again = Tag.query.get(tid)
        if again is None:
            print("FAIL: soft delete physically removed the row")
            return 1
        if not (again.is_deleted and again.deleted_by == 1 and again.deleted_at):
            print("FAIL: soft delete flags not set")
            return 1
        db.session.delete(again)
        db.session.commit()
        print("[4] soft delete OK")

        # Rollback test
        try:
            t2 = Tag(name="_verify_rollback", created_by=1)
            db.session.add(t2)
            db.session.flush()
            raise RuntimeError("simulated failure")
        except RuntimeError:
            db.session.rollback()
        if Tag.query.filter_by(name="_verify_rollback").first():
            print("FAIL: rollback did not discard the pending row")
            return 1
        print("[5] transaction rollback OK")

        print()
        print("ALL CHECKS PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())