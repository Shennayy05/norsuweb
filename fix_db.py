import sqlite3
import os

def fix_db():
    log = []
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Check current columns
        cursor.execute("PRAGMA table_info(dashboard_post)")
        columns = [col[1] for col in cursor.fetchall()]
        log.append(f"Initial columns: {columns}")
        
        # Add missing columns
        changes_made = False
        if 'post_type' not in columns:
            log.append("Adding post_type column...")
            cursor.execute("ALTER TABLE dashboard_post ADD COLUMN post_type VARCHAR(20) DEFAULT 'general'")
            changes_made = True
        
        if 'author' not in columns:
            log.append("Adding author column...")
            cursor.execute("ALTER TABLE dashboard_post ADD COLUMN author VARCHAR(255)")
            changes_made = True
        
        if 'college' not in columns:
            log.append("Adding college column...")
            cursor.execute("ALTER TABLE dashboard_post ADD COLUMN college VARCHAR(50) DEFAULT 'all'")
            changes_made = True
            
        if 'target_audience' not in columns:
            log.append("Adding target_audience column...")
            cursor.execute("ALTER TABLE dashboard_post ADD COLUMN target_audience VARCHAR(50) DEFAULT 'all'")
            changes_made = True

        if changes_made:
            conn.commit()
            log.append("Changes committed successfully.")
        else:
            log.append("No changes needed.")
            
        conn.close()
        log.append("Database fix completed.")
    except Exception as e:
        log.append(f"Error: {str(e)}")
    
    with open('fix_log.txt', 'w') as f:
        f.write('\n'.join(log))

if __name__ == "__main__":
    fix_db()
