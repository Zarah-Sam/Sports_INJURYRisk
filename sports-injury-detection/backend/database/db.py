"""
In-Memory & JSON Backed Database Service
Provides persistent storage for Users, Athletes, Assessments, Alerts, and Exercises.
"""
import json
import uuid
import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
from backend.config import DATA_DIR

DB_FILE = DATA_DIR / "app_state.json"

class Database:
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.athletes: Dict[str, Dict[str, Any]] = {}
        self.assessments: Dict[str, Dict[str, Any]] = {}
        self.notifications: List[Dict[str, Any]] = []
        self.load_or_seed()

    def load_or_seed(self):
        """Loads data from JSON file or seeds fresh initial realistic state."""
        if DB_FILE.exists():
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.users = data.get("users", {})
                    self.athletes = data.get("athletes", {})
                    self.assessments = data.get("assessments", {})
                    self.notifications = data.get("notifications", [])
                    return
            except Exception as e:
                print(f"[DB] Error loading DB_FILE: {e}. Re-seeding database.")
        
        self._seed_default_data()
        self.save()

    def save(self):
        """Persists current state to JSON file."""
        try:
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "users": self.users,
                    "athletes": self.athletes,
                    "assessments": self.assessments,
                    "notifications": self.notifications
                }, f, indent=2, default=str)
        except Exception as e:
            print(f"[DB] Failed to save DB: {e}")

    def _seed_default_data(self):
        from backend.database.seed_data import DEFAULT_USERS, DEFAULT_ATHLETES, DEFAULT_ASSESSMENTS, DEFAULT_NOTIFICATIONS
        self.users = {u["id"]: u for u in DEFAULT_USERS}
        self.athletes = {a["athlete_id"]: a for a in DEFAULT_ATHLETES}
        self.assessments = {ass["id"]: ass for ass in DEFAULT_ASSESSMENTS}
        self.notifications = list(DEFAULT_NOTIFICATIONS)

    # --- Athlete CRUD ---
    def get_athletes(self) -> List[Dict[str, Any]]:
        return list(self.athletes.values())

    def get_athlete(self, athlete_id: str) -> Optional[Dict[str, Any]]:
        return self.athletes.get(athlete_id)

    def update_athlete(self, athlete_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if athlete_id in self.athletes:
            self.athletes[athlete_id].update(updates)
            self.save()
            return self.athletes[athlete_id]
        return None

    def add_athlete(self, athlete_data: Dict[str, Any]) -> Dict[str, Any]:
        athlete_id = athlete_data.get("athlete_id") or f"ATH-{str(uuid.uuid4())[:6].upper()}"
        athlete_data["athlete_id"] = athlete_id
        if "created_at" not in athlete_data:
            athlete_data["created_at"] = datetime.datetime.now().isoformat()
        self.athletes[athlete_id] = athlete_data
        self.save()
        return athlete_data

    # --- Assessment Records ---
    def add_assessment(self, record: Dict[str, Any]) -> Dict[str, Any]:
        rec_id = record.get("id") or f"ASM-{str(uuid.uuid4())[:8]}"
        record["id"] = rec_id
        if "created_at" not in record:
            record["created_at"] = datetime.datetime.now().isoformat()
        self.assessments[rec_id] = record
        
        # Automatically update athlete's latest stats
        athlete_id = record.get("athlete_id")
        if athlete_id and athlete_id in self.athletes:
            ath = self.athletes[athlete_id]
            ath["last_assessment_date"] = record["created_at"]
            ath["latest_risk_score"] = record.get("overall_risk_score", 50)
            ath["risk_category"] = record.get("risk_category", "Moderate Risk")
            ath["movement_quality_score"] = record.get("movement_quality_score", 75)
            
        self.save()
        return record

    def get_assessments(self, athlete_id: Optional[str] = None) -> List[Dict[str, Any]]:
        records = list(self.assessments.values())
        if athlete_id:
            records = [r for r in records if r.get("athlete_id") == athlete_id]
        records.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return records

    def get_assessment(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        return self.assessments.get(assessment_id)

    # --- Notifications ---
    def add_notification(self, notif: Dict[str, Any]) -> Dict[str, Any]:
        if "id" not in notif:
            notif["id"] = f"NOTIF-{str(uuid.uuid4())[:6]}"
        if "timestamp" not in notif:
            notif["timestamp"] = datetime.datetime.now().isoformat()
        notif["read"] = False
        self.notifications.insert(0, notif)
        self.save()
        return notif

    def get_notifications(self, unread_only: bool = False) -> List[Dict[str, Any]]:
        if unread_only:
            return [n for n in self.notifications if not n.get("read")]
        return self.notifications

    def mark_notifications_read(self):
        for n in self.notifications:
            n["read"] = True
        self.save()

# Global database singleton
db = Database()
