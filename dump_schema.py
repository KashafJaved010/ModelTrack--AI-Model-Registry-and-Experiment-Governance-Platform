"""Generate schema.sql (MySQL DDL) from the SQLAlchemy models."""
from sqlalchemy.schema import CreateTable

from app import create_app
from app.extensions import db


def main():
    app = create_app() 
    
    # Yahan app_context add karna zaroori tha taake db.engine kaam kar sake
    with app.app_context():
        with open("schema.sql", "w", encoding="utf-8") as fh:
            fh.write("-- Auto-generated MySQL DDL for ModelTrack\n")
            fh.write("-- 40 tables\n\n")
            for table in db.metadata.sorted_tables:
                ddl = str(CreateTable(table).compile(db.engine))
                fh.write(ddl.strip() + ";\n\n")
        print(f"Wrote schema.sql with {len(db.metadata.tables)} tables")


if __name__ == "__main__":
    main()