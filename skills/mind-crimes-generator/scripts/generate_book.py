#!/usr/bin/env python3
"""
Mind Crimes Database Helper
Provides CLI interface to query and update case database
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "/opt/mind-crimes-automation/data/mindcrimes.db"

class MindCrimesDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    def check(self):
        """Check for next approved case"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, case_hash, title, victim_name, victim_age, 
                   murder_date, arrest_date, cold_case_years,
                   location, state, suspect_name, suspect_age,
                   dna_method, source_url, score, status, book_number
            FROM cases 
            WHERE status = 'approved'
            ORDER BY score DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        if not row:
            return {"status": "none", "message": "No approved cases found"}
        
        return {
            "status": "found",
            "case_id": row["id"],
            "case_hash": row["case_hash"],
            "title": row["title"],
            "victim_name": row["victim_name"],
            "victim_age": row["victim_age"],
            "murder_date": row["murder_date"],
            "arrest_date": row["arrest_date"],
            "cold_case_years": row["cold_case_years"],
            "location": row["location"],
            "state": row["state"],
            "suspect_name": row["suspect_name"],
            "suspect_age": row["suspect_age"],
            "dna_method": row["dna_method"],
            "source_url": row["source_url"],
            "score": row["score"],
            "book_number": row["book_number"]
        }
    
    def get(self, case_id):
        """Get specific case by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, case_hash, title, victim_name, victim_age, 
                   murder_date, arrest_date, cold_case_years,
                   location, state, suspect_name, suspect_age,
                   dna_method, source_url, raw_text, score, 
                   score_breakdown, status, book_number,
                   generated_at, uploaded_at, live_at,
                   created_at, updated_at
            FROM cases 
            WHERE id = ?
        """, (case_id,))
        
        row = cursor.fetchone()
        if not row:
            return {"status": "error", "message": f"Case {case_id} not found"}
        
        return {
            "status": "found",
            "case_id": row["id"],
            "case_hash": row["case_hash"],
            "title": row["title"],
            "victim_name": row["victim_name"],
            "victim_age": row["victim_age"],
            "murder_date": row["murder_date"],
            "arrest_date": row["arrest_date"],
            "cold_case_years": row["cold_case_years"],
            "location": row["location"],
            "state": row["state"],
            "suspect_name": row["suspect_name"],
            "suspect_age": row["suspect_age"],
            "dna_method": row["dna_method"],
            "source_url": row["source_url"],
            "raw_text": row["raw_text"],
            "score": row["score"],
            "score_breakdown": row["score_breakdown"],
            "case_status": row["status"],
            "book_number": row["book_number"],
            "generated_at": row["generated_at"],
            "uploaded_at": row["uploaded_at"],
            "live_at": row["live_at"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    
    def update(self, case_id, status, **kwargs):
        """Update case status and optional fields"""
        valid_statuses = ['scraped', 'alerted', 'approved', 'generating', 
                         'generated', 'uploaded', 'live', 'skipped']
        
        if status not in valid_statuses:
            return {
                "status": "error", 
                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            }
        
        # Build dynamic update query
        fields = ["status = ?", "updated_at = ?"]
        values = [status, datetime.now().isoformat()]
        
        # Add optional fields
        if 'book_number' in kwargs:
            fields.append("book_number = ?")
            values.append(kwargs['book_number'])
        
        if status == 'generated':
            fields.append("generated_at = ?")
            values.append(datetime.now().isoformat())
        elif status == 'uploaded':
            fields.append("uploaded_at = ?")
            values.append(datetime.now().isoformat())
        elif status == 'live':
            fields.append("live_at = ?")
            values.append(datetime.now().isoformat())
        
        # Add case_id to values
        values.append(case_id)
        
        query = f"UPDATE cases SET {', '.join(fields)} WHERE id = ?"
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"Case {case_id} not found"}
        
        return {
            "status": "success",
            "case_id": case_id,
            "new_status": status,
            "updated_at": datetime.now().isoformat()
        }
    
    def list_by_status(self, status, limit=10):
        """List cases by status"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, title, victim_name, score, status, created_at
            FROM cases 
            WHERE status = ?
            ORDER BY score DESC
            LIMIT ?
        """, (status, limit))
        
        rows = cursor.fetchall()
        return {
            "status": "success",
            "count": len(rows),
            "cases": [
                {
                    "case_id": row["id"],
                    "title": row["title"],
                    "victim_name": row["victim_name"],
                    "score": row["score"],
                    "status": row["status"],
                    "created_at": row["created_at"]
                }
                for row in rows
            ]
        }
    
    def stats(self):
        """Get database statistics"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                status,
                COUNT(*) as count,
                AVG(score) as avg_score
            FROM cases
            GROUP BY status
            ORDER BY count DESC
        """)
        
        rows = cursor.fetchall()
        return {
            "status": "success",
            "stats": [
                {
                    "status": row["status"],
                    "count": row["count"],
                    "avg_score": round(row["avg_score"], 2) if row["avg_score"] else 0
                }
                for row in rows
            ]
        }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "Usage: generate_book.py <command> [args]",
            "commands": {
                "check": "Check for next approved case",
                "get <case_id>": "Get specific case details",
                "update <case_id> <status>": "Update case status",
                "list <status> [limit]": "List cases by status",
                "stats": "Get database statistics"
            }
        }, indent=2))
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        with MindCrimesDB() as db:
            if command == "check":
                result = db.check()
                
            elif command == "get":
                if len(sys.argv) < 3:
                    result = {"status": "error", "message": "Usage: get <case_id>"}
                else:
                    case_id = int(sys.argv[2])
                    result = db.get(case_id)
                    
            elif command == "update":
                if len(sys.argv) < 4:
                    result = {"status": "error", "message": "Usage: update <case_id> <status>"}
                else:
                    case_id = int(sys.argv[2])
                    status = sys.argv[3]
                    result = db.update(case_id, status)
                    
            elif command == "list":
                if len(sys.argv) < 3:
                    result = {"status": "error", "message": "Usage: list <status> [limit]"}
                else:
                    status = sys.argv[2]
                    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
                    result = db.list_by_status(status, limit)
                    
            elif command == "stats":
                result = db.stats()
                
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown command: {command}"
                }
        
        print(json.dumps(result, indent=2))
        
    except sqlite3.Error as e:
        print(json.dumps({
            "status": "error",
            "message": f"Database error: {str(e)}"
        }, indent=2))
        sys.exit(1)
        
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
