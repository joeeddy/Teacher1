"""
Student Profile System for Teacher1
-----------------------------------
Tracks individual kindergarten students' learning progress, preferences, and performance.
"""

import json
import os
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import uuid

class KindergartenStudent:
    """Individual student profile for kindergarten learning."""
    
    def __init__(self, name: str, age: int = 5, student_id: Optional[str] = None):
        self.student_id = student_id or str(uuid.uuid4())
        self.name = name
        self.age = age
        self.created_at = datetime.now().isoformat()
        
        # Learning progress tracking
        self.progress = {
            "math": {"level": 1, "score": 0, "attempts": 0, "successes": 0},
            "reading": {"level": 1, "score": 0, "attempts": 0, "successes": 0},
            "spelling": {"level": 1, "score": 0, "attempts": 0, "successes": 0},
            "numbers": {"level": 1, "score": 0, "attempts": 0, "successes": 0}
        }
        
        # Learning style preferences (detected over time)
        self.learning_style = {
            "visual": 0.33,      # Preference for visual learning
            "auditory": 0.33,    # Preference for audio learning  
            "kinesthetic": 0.34  # Preference for interactive learning
        }
        
        # Engagement and emotional state tracking
        self.engagement = {
            "attention_span": 300,  # seconds, starts at 5 minutes for kindergarten
            "positive_responses": 0,
            "negative_responses": 0,
            "frustration_indicators": 0,
            "excitement_indicators": 0
        }
        
        # Session history
        self.sessions = []
        self.last_active = datetime.now().isoformat()
        
        # Personalization settings
        self.preferences = {
            "favorite_subject": None,
            "difficulty_preference": "adaptive",  # adaptive, easy, medium, hard
            "interaction_style": "encouraging",   # encouraging, neutral, challenging
            "break_frequency": 10  # minutes between suggested breaks
        }

    def start_session(self) -> str:
        """Start a new learning session."""
        session_id = str(uuid.uuid4())
        session = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "activities": [],
            "total_score": 0,
            "subjects_covered": [],
            "engagement_level": "neutral"
        }
        self.sessions.append(session)
        self.last_active = datetime.now().isoformat()
        return session_id

    def end_session(self, session_id: str):
        """End the current learning session."""
        for session in self.sessions:
            if session["session_id"] == session_id:
                session["end_time"] = datetime.now().isoformat()
                break

    def record_activity(self, session_id: str, subject: str, activity: str, 
                       success: bool, difficulty: int, time_taken: float):
        """Record a learning activity result."""
        # Find current session
        current_session = None
        for session in self.sessions:
            if session["session_id"] == session_id:
                current_session = session
                break
        
        if not current_session:
            return
        
        # Record activity
        activity_record = {
            "timestamp": datetime.now().isoformat(),
            "subject": subject,
            "activity": activity,
            "success": success,
            "difficulty": difficulty,
            "time_taken": time_taken,
            "score": self._calculate_activity_score(success, difficulty, time_taken)
        }
        
        current_session["activities"].append(activity_record)
        if subject not in current_session["subjects_covered"]:
            current_session["subjects_covered"].append(subject)
        
        # Update progress
        self._update_progress(subject, success, difficulty, time_taken)
        self._detect_learning_style(activity_record)
        self._update_engagement(success, time_taken)

    def _calculate_activity_score(self, success: bool, difficulty: int, time_taken: float) -> int:
        """Calculate score for an activity (0-100)."""
        if not success:
            return max(0, 20 - difficulty * 5)  # Participation points
        
        base_score = 50 + (difficulty * 10)  # Base score increases with difficulty
        
        # Time bonus (kindergarteners shouldn't be rushed)
        if time_taken < 30:  # Very fast (might be guessing)
            time_multiplier = 0.8
        elif time_taken < 120:  # Good pace
            time_multiplier = 1.0
        elif time_taken < 300:  # Taking time to think
            time_multiplier = 0.95
        else:  # Might need help
            time_multiplier = 0.7
            
        return min(100, int(base_score * time_multiplier))

    def _update_progress(self, subject: str, success: bool, difficulty: int, time_taken: float):
        """Update subject progress based on activity."""
        if subject not in self.progress:
            return
            
        progress = self.progress[subject]
        progress["attempts"] += 1
        
        if success:
            progress["successes"] += 1
            progress["score"] += self._calculate_activity_score(success, difficulty, time_taken)
            
            # Level progression (conservative for kindergarten)
            success_rate = progress["successes"] / progress["attempts"]
            if success_rate > 0.8 and progress["attempts"] >= 5:
                progress["level"] = min(5, progress["level"] + 1)  # Max level 5 for kindergarten

    def _detect_learning_style(self, activity_record: Dict):
        """Detect learning style preferences from activity patterns."""
        if activity_record["success"]:
            # Adjust learning style based on activity type and performance
            if "visual" in activity_record["activity"].lower():
                self.learning_style["visual"] += 0.1
            elif "sound" in activity_record["activity"].lower() or "say" in activity_record["activity"].lower():
                self.learning_style["auditory"] += 0.1
            elif "interactive" in activity_record["activity"].lower() or "game" in activity_record["activity"].lower():
                self.learning_style["kinesthetic"] += 0.1
            
            # Normalize to keep total = 1.0
            total = sum(self.learning_style.values())
            for style in self.learning_style:
                self.learning_style[style] /= total

    def _update_engagement(self, success: bool, time_taken: float):
        """Update engagement metrics."""
        if success:
            self.engagement["positive_responses"] += 1
            if time_taken < 60:  # Quick success might indicate excitement
                self.engagement["excitement_indicators"] += 1
        else:
            self.engagement["negative_responses"] += 1
            if time_taken > 180:  # Long time without success might indicate frustration
                self.engagement["frustration_indicators"] += 1

    def get_recommended_difficulty(self, subject: str) -> int:
        """Get recommended difficulty level for a subject (1-5)."""
        if subject not in self.progress:
            return 1
        
        progress = self.progress[subject]
        if progress["attempts"] == 0:
            return 1
        
        success_rate = progress["successes"] / progress["attempts"]
        current_level = progress["level"]
        
        # Adaptive difficulty based on recent performance
        if success_rate > 0.85:
            return min(5, current_level + 1)
        elif success_rate > 0.6:
            return current_level
        else:
            return max(1, current_level - 1)

    def get_preferred_learning_style(self) -> str:
        """Get the dominant learning style."""
        return max(self.learning_style.items(), key=lambda x: x[1])[0]

    def needs_break(self, session_start: datetime) -> bool:
        """Check if student needs a break based on attention span."""
        session_duration = (datetime.now() - session_start).seconds
        return session_duration > self.engagement["attention_span"]

    def is_frustrated(self) -> bool:
        """Check if student shows signs of frustration."""
        total_responses = self.engagement["positive_responses"] + self.engagement["negative_responses"]
        if total_responses < 5:
            return False
        
        frustration_rate = self.engagement["frustration_indicators"] / total_responses
        return frustration_rate > 0.3

    def get_encouragement_level(self) -> str:
        """Get appropriate encouragement level."""
        if self.is_frustrated():
            return "high"
        elif self.engagement["excitement_indicators"] > self.engagement["frustration_indicators"]:
            return "maintain"
        else:
            return "moderate"

    def to_dict(self) -> Dict:
        """Convert student profile to dictionary for storage."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "created_at": self.created_at,
            "progress": self.progress,
            "learning_style": self.learning_style,
            "engagement": self.engagement,
            "sessions": self.sessions,
            "last_active": self.last_active,
            "preferences": self.preferences
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'KindergartenStudent':
        """Create student profile from dictionary."""
        student = cls(data["name"], data["age"], data["student_id"])
        student.created_at = data["created_at"]
        student.progress = data["progress"]
        student.learning_style = data["learning_style"]
        student.engagement = data["engagement"]
        student.sessions = data["sessions"]
        student.last_active = data["last_active"]
        student.preferences = data["preferences"]
        return student

class StudentProfileManager:
    """Manages multiple student profiles."""
    
    def __init__(self, profiles_dir: str = "student_profiles"):
        self.profiles_dir = profiles_dir
        self.active_students = {}  # student_id -> KindergartenStudent
        
        # Create profiles directory if it doesn't exist
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)

    def create_student(self, name: str, age: int = 5) -> KindergartenStudent:
        """Create a new student profile."""
        student = KindergartenStudent(name, age)
        self.active_students[student.student_id] = student
        self.save_student(student)
        return student

    def load_student(self, student_id: str) -> Optional[KindergartenStudent]:
        """Load a student profile from file."""
        if student_id in self.active_students:
            return self.active_students[student_id]
        
        file_path = os.path.join(self.profiles_dir, f"{student_id}.json")
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            student = KindergartenStudent.from_dict(data)
            self.active_students[student_id] = student
            return student
        except Exception as e:
            print(f"Error loading student profile {student_id}: {e}")
            return None

    def save_student(self, student: KindergartenStudent):
        """Save a student profile to file."""
        file_path = os.path.join(self.profiles_dir, f"{student.student_id}.json")
        try:
            with open(file_path, 'w') as f:
                json.dump(student.to_dict(), f, indent=2)
        except Exception as e:
            print(f"Error saving student profile {student.student_id}: {e}")

    def list_students(self) -> List[Dict[str, str]]:
        """List all student profiles."""
        students = []
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith('.json'):
                student_id = filename[:-5]  # Remove .json extension
                file_path = os.path.join(self.profiles_dir, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    students.append({
                        "student_id": student_id,
                        "name": data["name"],
                        "age": data["age"],
                        "last_active": data["last_active"]
                    })
                except Exception as e:
                    print(f"Error reading profile {filename}: {e}")
        
        # Sort by last active
        students.sort(key=lambda x: x["last_active"], reverse=True)
        return students

    def get_student_by_name(self, name: str) -> Optional[KindergartenStudent]:
        """Find student by name."""
        for student_info in self.list_students():
            if student_info["name"].lower() == name.lower():
                return self.load_student(student_info["student_id"])
        return None