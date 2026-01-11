#!/usr/bin/env python3
"""
Check database structure and data
"""
import pymysql

def check_database():
    """Check database structure and content"""
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Soma@9985',
            database='MajorProject'
        )
        cursor = connection.cursor()
        
        print("=== DATABASE STRUCTURE CHECK ===\n")
        
        # Show all tables
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        print(f"📋 Tables in MajorProject database ({len(tables)} total):")
        for table in tables:
            print(f"   ✓ {table[0]}")
        
        print("\n=== TABLE CONTENTS ===\n")
        
        # Check each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
            count = cursor.fetchone()[0]
            print(f"📊 {table_name}: {count} records")
            
            # Show structure
            cursor.execute(f'DESCRIBE {table_name}')
            columns = cursor.fetchall()
            print(f"   Columns: {', '.join([col[0] for col in columns])}")
        
        print("\n=== SAMPLE DATA ===\n")
        
        # Show sample users
        cursor.execute('SELECT id, email, first_name, last_name, role FROM users LIMIT 5')
        users = cursor.fetchall()
        print("👥 Sample Users:")
        for user in users:
            print(f"   ID: {user[0]}, Email: {user[1]}, Name: {user[2]} {user[3]}, Role: {user[4]}")
        
        # Show sample books
        cursor.execute('SELECT id, title, author, category FROM books LIMIT 5')
        books = cursor.fetchall()
        print("\n📚 Sample Books:")
        for book in books:
            print(f"   ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Category: {book[3]}")
        
        cursor.close()
        connection.close()
        
        print("\n✅ Database check completed successfully!")
        print("\nIf you don't see tables in MySQL Workbench:")
        print("1. Refresh the connection (F5)")
        print("2. Make sure you're looking at 'MajorProject' database")
        print("3. Expand the 'Tables' section")
        print("4. Try running: USE MajorProject; SHOW TABLES;")
        
    except Exception as e:
        print(f"❌ Error checking database: {str(e)}")

if __name__ == "__main__":
    check_database()