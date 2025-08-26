"""
Personalized Kindergarten Chatbot for Teacher1
----------------------------------------------
Enhanced chatbot integration with student profiling and adaptive learning.
"""

import os
import sys
import random
import time
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from student_profile import KindergartenStudent, StudentProfileManager

class PersonalizedKindergartenChatbot:
    """
    Personalized chatbot for kindergarten education with adaptive learning.
    """
    
    def __init__(self):
        self.student_manager = StudentProfileManager()
        self.current_student = None
        self.current_session_id = None
        self.session_start_time = None
        
        # Educational content organized by subject and difficulty
        self.educational_content = self._load_educational_content()
        
        # Emotional responses based on student state
        self.encouragement_responses = {
            "high": [
                "You're doing great! Let's try something a little different.",
                "I can see you're working hard! How about we take a fun break?",
                "You're such a good learner! Let's try this together step by step.",
                "Don't worry, learning takes time. You're doing wonderfully!"
            ],
            "moderate": [
                "Nice work! You're getting better at this!",
                "Great job! Let's keep going!",
                "You're learning so well! I'm proud of you!",
                "Excellent! You're becoming an expert!"
            ],
            "maintain": [
                "Fantastic! You're on fire today!",
                "Wow! You're really good at this!",
                "Amazing work! You're a superstar!",
                "Incredible! You make this look easy!"
            ]
        }

    def _load_educational_content(self) -> Dict:
        """Load kindergarten educational content organized by difficulty."""
        return {
            "math": {
                1: {  # Beginner
                    "questions": [
                        "What comes after 3?",
                        "Count with me: 1, 2, 3, ?",
                        "If you have 2 apples and I give you 1 more, how many do you have?",
                        "Show me 5 fingers!"
                    ],
                    "answers": ["4", "4", "3", "5"],
                    "activities": ["counting", "simple_addition", "number_recognition"]
                },
                2: {  # Easy
                    "questions": [
                        "What is 2 + 2?",
                        "Count backwards from 5: 5, 4, 3, ?",
                        "Which is bigger: 6 or 3?",
                        "If you have 5 toys and give away 2, how many are left?"
                    ],
                    "answers": ["4", "2", "6", "3"],
                    "activities": ["addition", "subtraction", "comparison"]
                },
                3: {  # Medium
                    "questions": [
                        "What is 5 + 3?",
                        "What is 10 - 4?",
                        "How many sides does a triangle have?",
                        "What number is between 7 and 9?"
                    ],
                    "answers": ["8", "6", "3", "8"],
                    "activities": ["addition", "subtraction", "shapes", "number_patterns"]
                }
            },
            "reading": {
                1: {  # Beginner
                    "questions": [
                        "What sound does the letter 'A' make?",
                        "Can you find the letter 'B' in the word 'BIG'?",
                        "What letter does 'CAT' start with?",
                        "Point to the letter 'M' in 'MOM'"
                    ],
                    "answers": ["a", "b", "c", "m"],
                    "activities": ["letter_recognition", "phonics", "letter_sounds"]
                },
                2: {  # Easy
                    "questions": [
                        "What word rhymes with 'CAT'?",
                        "How many letters are in 'DOG'?",
                        "What sound do you hear at the beginning of 'SUN'?",
                        "Can you read this word: 'THE'?"
                    ],
                    "answers": ["bat", "3", "s", "the"],
                    "activities": ["rhyming", "word_length", "beginning_sounds", "sight_words"]
                },
                3: {  # Medium
                    "questions": [
                        "What is the opposite of 'BIG'?",
                        "Can you make a sentence with the word 'HAPPY'?",
                        "What sound do you hear in the middle of 'CAT'?",
                        "How many words are in 'I like dogs'?"
                    ],
                    "answers": ["small", "varies", "a", "3"],
                    "activities": ["opposites", "sentence_building", "middle_sounds", "word_counting"]
                }
            },
            "spelling": {
                1: {  # Beginner
                    "questions": [
                        "Can you spell 'CAT'?",
                        "What letters make 'DOG'?",
                        "Spell your name for me!",
                        "How do you spell 'MOM'?"
                    ],
                    "answers": ["cat", "dog", "varies", "mom"],
                    "activities": ["simple_spelling", "name_spelling", "family_words"]
                },
                2: {  # Easy
                    "questions": [
                        "Can you spell 'FISH'?",
                        "How do you spell 'BOOK'?",
                        "Spell the word for a small furry pet: 'CAT'",
                        "Can you spell 'HAPPY'?"
                    ],
                    "answers": ["fish", "book", "cat", "happy"],
                    "activities": ["word_spelling", "themed_spelling", "emotion_words"]
                }
            },
            "numbers": {
                1: {  # Beginner
                    "questions": [
                        "Can you count to 5?",
                        "What number comes before 3?",
                        "Show me the number 7!",
                        "Count these dots: • • •"
                    ],
                    "answers": ["1,2,3,4,5", "2", "7", "3"],
                    "activities": ["counting", "number_order", "number_recognition", "dot_counting"]
                },
                2: {  # Easy
                    "questions": [
                        "Can you count to 10?",
                        "What number is missing: 1, 2, _, 4?",
                        "Which is smaller: 8 or 5?",
                        "Count by 2s: 2, 4, 6, _?"
                    ],
                    "answers": ["1,2,3,4,5,6,7,8,9,10", "3", "5", "8"],
                    "activities": ["counting_to_ten", "missing_numbers", "number_comparison", "skip_counting"]
                }
            }
        }

    def start_session(self, student_name: str) -> str:
        """Start a personalized learning session."""
        # Load or create student profile
        self.current_student = self.student_manager.get_student_by_name(student_name)
        if not self.current_student:
            print(f"Creating new profile for {student_name}")
            self.current_student = self.student_manager.create_student(student_name)
        
        # Start session
        self.current_session_id = self.current_student.start_session()
        self.session_start_time = datetime.now()
        
        # Personalized greeting
        greeting = self._generate_personalized_greeting()
        return greeting

    def _generate_personalized_greeting(self) -> str:
        """Generate a personalized greeting based on student profile."""
        name = self.current_student.name
        
        # Check if this is a returning student
        if len(self.current_student.sessions) > 1:
            last_session = self.current_student.sessions[-2]  # Previous session
            if last_session.get("subjects_covered"):
                last_subject = last_session["subjects_covered"][-1]
                return f"Hi {name}! Great to see you again! Last time we worked on {last_subject}. What would you like to learn today?"
        
        # New student greeting
        preferred_style = self.current_student.get_preferred_learning_style()
        if preferred_style == "visual":
            return f"Hello {name}! I'm so excited to learn with you today! I have some fun pictures and activities to show you!"
        elif preferred_style == "auditory":
            return f"Hi there, {name}! Ready to listen and learn together? We can practice sounds and words!"
        else:
            return f"Hey {name}! Let's have fun learning together today! We can play games and try new activities!"

    def get_response(self, user_input: str) -> Tuple[str, Dict]:
        """Generate a personalized response based on student profile and input."""
        if not self.current_student:
            return "Hi! What's your name? I'd love to learn with you!", {}
        
        # Check if student needs a break
        if self.current_student.needs_break(self.session_start_time):
            return self._suggest_break(), {"break_suggested": True}
        
        # Analyze input for learning intent
        intent, subject = self._analyze_input(user_input)
        
        # Get appropriate difficulty level
        difficulty = self.current_student.get_recommended_difficulty(subject) if subject else 1
        
        # Generate response based on intent
        if intent == "greeting":
            return self._generate_personalized_greeting(), {}
        elif intent == "help":
            return self._generate_help_response(), {}
        elif intent == "lesson_request":
            return self._generate_lesson(subject, difficulty), {"lesson_started": True, "subject": subject}
        elif intent == "answer":
            return self._process_answer(user_input, subject), {"answer_processed": True}
        elif intent == "encouragement_needed":
            return self._provide_encouragement(), {"encouragement_provided": True}
        else:
            return self._generate_adaptive_response(user_input), {}

    def _analyze_input(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Analyze user input to determine intent and subject."""
        input_lower = user_input.lower()
        
        # Greeting detection
        if any(word in input_lower for word in ["hi", "hello", "hey", "good morning"]):
            return "greeting", None
        
        # Help detection
        if any(word in input_lower for word in ["help", "don't know", "confused", "stuck"]):
            return "help", None
        
        # Subject detection
        if any(word in input_lower for word in ["math", "numbers", "count", "add", "plus"]):
            return "lesson_request", "math"
        elif any(word in input_lower for word in ["read", "letter", "word", "sound", "phonics"]):
            return "lesson_request", "reading"
        elif any(word in input_lower for word in ["spell", "spelling", "letters"]):
            return "lesson_request", "spelling"
        elif any(word in input_lower for word in ["number", "counting"]):
            return "lesson_request", "numbers"
        
        # Frustration indicators
        if any(word in input_lower for word in ["hard", "difficult", "can't", "don't want", "boring"]):
            return "encouragement_needed", None
        
        # Assume it's an answer to a question
        return "answer", self._get_current_subject()

    def _get_current_subject(self) -> Optional[str]:
        """Get the current subject being studied."""
        if not self.current_student or not self.current_session_id:
            return None
        
        current_session = None
        for session in self.current_student.sessions:
            if session["session_id"] == self.current_session_id:
                current_session = session
                break
        
        if current_session and current_session["activities"]:
            return current_session["activities"][-1]["subject"]
        
        return None

    def _generate_lesson(self, subject: str, difficulty: int) -> str:
        """Generate a personalized lesson based on subject and difficulty."""
        if subject not in self.educational_content:
            return f"I'd love to help you with {subject}! Let's start with something fun and easy."
        
        # Get content for the difficulty level
        content = self.educational_content[subject].get(difficulty, self.educational_content[subject][1])
        
        # Select a random question
        questions = content["questions"]
        question = random.choice(questions)
        
        # Store the current question for answer processing
        if not hasattr(self, '_current_question'):
            self._current_question = {}
        self._current_question[subject] = {
            "question": question,
            "difficulty": difficulty,
            "start_time": time.time()
        }
        
        # Personalize the presentation based on learning style
        learning_style = self.current_student.get_preferred_learning_style()
        
        if learning_style == "visual":
            return f"Let's look at this {subject} question together! {question} Take your time and think about it!"
        elif learning_style == "auditory":
            return f"Listen carefully to this {subject} question: {question} Say your answer out loud!"
        else:
            return f"Here's a fun {subject} challenge for you! {question} You can use your fingers or draw if it helps!"

    def _process_answer(self, user_input: str, subject: Optional[str]) -> str:
        """Process student's answer and provide feedback."""
        if not subject or not hasattr(self, '_current_question') or subject not in self._current_question:
            return "That's interesting! What would you like to learn about next?"
        
        current_q = self._current_question[subject]
        time_taken = time.time() - current_q["start_time"]
        
        # Simple answer evaluation (in a real system, this would be more sophisticated)
        is_correct = self._evaluate_answer(user_input, subject, current_q)
        
        # Record the activity
        self.current_student.record_activity(
            self.current_session_id,
            subject,
            f"question_{current_q['difficulty']}",
            is_correct,
            current_q["difficulty"],
            time_taken
        )
        
        # Save student progress
        self.student_manager.save_student(self.current_student)
        
        # Generate feedback
        return self._generate_feedback(is_correct, time_taken, subject)

    def _evaluate_answer(self, user_input: str, subject: str, question_data: Dict) -> bool:
        """Evaluate if the student's answer is correct."""
        # This is a simplified evaluation - in a real system this would be much more sophisticated
        input_lower = user_input.lower().strip()
        
        # For math questions, look for numbers
        if subject == "math":
            try:
                if any(char.isdigit() for char in user_input):
                    return True  # Give credit for attempting math
            except:
                pass
        
        # For reading/spelling, look for letter attempts
        if subject in ["reading", "spelling"]:
            if any(char.isalpha() for char in user_input):
                return True  # Give credit for attempting letters
        
        # For counting, look for number sequences
        if subject == "numbers":
            if any(char.isdigit() for char in user_input) or "," in user_input:
                return True  # Give credit for counting attempts
        
        # Default: give credit for attempting
        return len(input_lower) > 0

    def _generate_feedback(self, is_correct: bool, time_taken: float, subject: str) -> str:
        """Generate personalized feedback based on performance."""
        encouragement_level = self.current_student.get_encouragement_level()
        
        if is_correct:
            if time_taken < 30:
                feedback = random.choice([
                    "Wow! You're so quick and smart!",
                    "Amazing! You got that super fast!",
                    "Fantastic! You're a {subject} superstar!"
                ]).format(subject=subject)
            else:
                feedback = random.choice([
                    "Excellent work! You really thought about that!",
                    "Great job! I can see you're thinking carefully!",
                    "Perfect! Taking your time helped you get it right!"
                ])
        else:
            if encouragement_level == "high":
                feedback = random.choice(self.encouragement_responses["high"])
            else:
                feedback = random.choice([
                    "Good try! Let's work on this together!",
                    "That's okay! Learning takes practice!",
                    "Nice attempt! Let me help you with this!"
                ])
        
        # Add a follow-up question or activity
        next_activity = self._suggest_next_activity(subject, is_correct)
        return f"{feedback} {next_activity}"

    def _suggest_next_activity(self, subject: str, last_success: bool) -> str:
        """Suggest the next learning activity."""
        if self.current_student.is_frustrated():
            return "How about we try something different and fun?"
        
        if last_success:
            return f"Ready for another {subject} challenge?"
        else:
            return f"Let's try a different {subject} activity that might be easier!"

    def _provide_encouragement(self) -> str:
        """Provide encouragement when student is frustrated."""
        encouragement_level = self.current_student.get_encouragement_level()
        return random.choice(self.encouragement_responses[encouragement_level])

    def _suggest_break(self) -> str:
        """Suggest a break when student has been learning for too long."""
        return random.choice([
            "You've been working so hard! How about we take a little break? We can stretch or sing a song!",
            "Great job learning today! Let's take a fun break and then come back to learning!",
            "You're doing amazing! Want to take a quick break? We can play a movement game!"
        ])

    def _generate_help_response(self) -> str:
        """Generate helpful response when student asks for help."""
        return random.choice([
            "I'm here to help you! What would you like to learn about? We can try math, reading, spelling, or numbers!",
            "Of course I'll help! Tell me what you're curious about and we'll learn together!",
            "I love helping! What sounds fun to you today - counting, letters, or maybe some math?"
        ])

    def _generate_adaptive_response(self, user_input: str) -> str:
        """Generate adaptive response for general conversation."""
        return random.choice([
            "That's really interesting! Tell me more!",
            "I love learning new things with you! What else are you thinking about?",
            "You're so smart! What would you like to explore next?",
            "That's a great thought! What would you like to learn about today?"
        ])

    def end_session(self) -> str:
        """End the current learning session."""
        if not self.current_student or not self.current_session_id:
            return "Goodbye! Come back anytime to learn more!"
        
        # End the session
        self.current_student.end_session(self.current_session_id)
        self.student_manager.save_student(self.current_student)
        
        # Generate personalized goodbye
        name = self.current_student.name
        current_session = None
        for session in self.current_student.sessions:
            if session["session_id"] == self.current_session_id:
                current_session = session
                break
        
        if current_session and current_session["activities"]:
            subjects = list(set(activity["subject"] for activity in current_session["activities"]))
            subject_list = ", ".join(subjects)
            return f"Great job today, {name}! You worked on {subject_list} and did wonderful! I can't wait to learn with you again!"
        else:
            return f"Thanks for spending time with me, {name}! Come back soon and we'll learn lots of fun things together!"

    def get_student_progress_summary(self) -> Dict:
        """Get a summary of the current student's progress."""
        if not self.current_student:
            return {}
        
        return {
            "name": self.current_student.name,
            "progress": self.current_student.progress,
            "learning_style": self.current_student.get_preferred_learning_style(),
            "engagement": self.current_student.engagement,
            "total_sessions": len(self.current_student.sessions),
            "needs_encouragement": self.current_student.is_frustrated()
        }

# Example usage for testing
if __name__ == "__main__":
    chatbot = PersonalizedKindergartenChatbot()
    
    # Start a session
    greeting = chatbot.start_session("Emma")
    print("Bot:", greeting)
    
    # Simulate conversation
    test_inputs = [
        "I want to learn math",
        "5",
        "Can you help me with reading?",
        "I don't know",
        "bye"
    ]
    
    for user_input in test_inputs:
        print(f"Student: {user_input}")
        response, metadata = chatbot.get_response(user_input)
        print(f"Bot: {response}")
        if metadata:
            print(f"Metadata: {metadata}")
        print()
    
    # End session
    goodbye = chatbot.end_session()
    print("Bot:", goodbye)
    
    # Show progress summary
    summary = chatbot.get_student_progress_summary()
    print("\nProgress Summary:", summary)