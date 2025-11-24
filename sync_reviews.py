import sqlite3
import os

# Paths
LOCAL_REVIEW_DB = r'c:\Proyectos propios\SampleMaster\Sample\Page\local-review.db'
RENDER_DB = r'c:\Proyectos propios\SampleMaster\render\mibase.db'

def sync_reviews():
    if not os.path.exists(LOCAL_REVIEW_DB):
        print(f"Error: Local review DB not found at {LOCAL_REVIEW_DB}")
        return

    if not os.path.exists(RENDER_DB):
        print(f"Error: Render DB not found at {RENDER_DB}")
        return

    # 1. Get rejected IDs from local review DB
    print(f"Reading rejected reviews from {LOCAL_REVIEW_DB}...")
    try:
        conn_local = sqlite3.connect(LOCAL_REVIEW_DB)
        cursor_local = conn_local.cursor()
        
        cursor_local.execute("SELECT question_id FROM Review WHERE status = 0")
        rejected_ids = [row[0] for row in cursor_local.fetchall()]
        
        conn_local.close()
        print(f"Found {len(rejected_ids)} rejected questions.")
    except Exception as e:
        print(f"Error reading local DB: {e}")
        return

    if not rejected_ids:
        print("No rejected reviews found. Nothing to delete.")
        return

    # 2. Delete from Render DB
    print(f"Deleting {len(rejected_ids)} questions from {RENDER_DB}...")
    try:
        conn_render = sqlite3.connect(RENDER_DB)
        cursor_render = conn_render.cursor()
        
        # Prepare comma-separated string of placeholders
        placeholders = ','.join('?' for _ in rejected_ids)
        query = f"DELETE FROM Question WHERE id IN ({placeholders})"
        
        cursor_render.execute(query, rejected_ids)
        deleted_count = cursor_render.rowcount
        
        conn_render.commit()
        conn_render.close()
        
        print(f"Successfully deleted {deleted_count} questions from Render DB.")
        
    except Exception as e:
        print(f"Error updating Render DB: {e}")

if __name__ == "__main__":
    sync_reviews()
