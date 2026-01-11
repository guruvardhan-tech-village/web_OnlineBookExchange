import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app, db
from sqlalchemy import text

app = create_app()
app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql+pymysql://root:Soma%409985@localhost:3306/MajorProject_test',
    'TESTING': True
})

with app.app_context():
    # Check foreign key constraints
    result = db.session.execute(text("""
        SELECT 
            kcu.TABLE_NAME,
            kcu.COLUMN_NAME,
            kcu.CONSTRAINT_NAME,
            kcu.REFERENCED_TABLE_NAME,
            kcu.REFERENCED_COLUMN_NAME,
            rc.DELETE_RULE,
            rc.UPDATE_RULE
        FROM information_schema.KEY_COLUMN_USAGE kcu
        JOIN information_schema.REFERENTIAL_CONSTRAINTS rc 
            ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME 
            AND kcu.CONSTRAINT_SCHEMA = rc.CONSTRAINT_SCHEMA
        WHERE kcu.REFERENCED_TABLE_SCHEMA = 'MajorProject_test'
        AND kcu.REFERENCED_TABLE_NAME IS NOT NULL
    """))
    
    print("Foreign Key Constraints:")
    for row in result:
        print(f"Table: {row[0]}, Column: {row[1]}, References: {row[3]}.{row[4]}, Delete: {row[5]}, Update: {row[6]}")
    
    # Also check if tables exist
    tables_result = db.session.execute(text("SHOW TABLES"))
    tables = [row[0] for row in tables_result]
    print(f"\nTables in database: {tables}")