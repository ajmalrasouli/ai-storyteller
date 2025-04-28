import sqlite3
import os
import sys

def migrate_database():
    try:
        # Check if the database file exists
        db_path = os.path.join('instance', 'stories.db')
        if not os.path.exists(db_path):
            print(f"ERROR: Database file not found at {os.path.abspath(db_path)}")
            # Check if the instance directory exists, if not try the root directory
            root_db_path = 'stories.db'
            if os.path.exists(root_db_path):
                print(f"Found database at root level: {os.path.abspath(root_db_path)}")
                db_path = root_db_path
            else:
                print("ERROR: Could not find stories.db in either instance/ or root directory")
                print("Checking directories...")
                for dir_name, _, files in os.walk('.'):
                    for file in files:
                        if file.endswith('.db'):
                            print(f"Found database: {os.path.join(dir_name, file)}")
                return False

        print(f"Using database at: {os.path.abspath(db_path)}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in database:", [table[0] for table in tables])

        if ('story',) not in tables:
            print("ERROR: 'story' table not found in database")
            return False

        # Check if the column already exists
        cursor.execute("PRAGMA table_info(story)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        print("\nCurrent story table structure:")
        for column in columns:
            print(f"  {column[1]} ({column[2]})")

        if 'image_url' not in column_names:
            print("\nAdding image_url column to story table...")
            cursor.execute("ALTER TABLE story ADD COLUMN image_url TEXT")
            conn.commit()
            print("Successfully added image_url column!")
            
            # Verify the table structure after modification
            cursor.execute("PRAGMA table_info(story)")
            updated_columns = cursor.fetchall()
            print("\nUpdated table structure:")
            for column in updated_columns:
                print(f"  {column[1]} ({column[2]})")
        else:
            print("\nimage_url column already exists in story table")

        conn.close()
        print("\nDatabase migration completed successfully!")
        return True
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Starting database migration...")
    if migrate_database():
        print("Migration successful!")
    else:
        print("Migration failed!")
        sys.exit(1) 