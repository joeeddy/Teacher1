#!/usr/bin/env python3
"""
Teacher1 Kindergarten Demo
-------------------------
Demonstrates the individualized kindergarten learning features.
"""

import time
import json
from personalized_chatbot import PersonalizedKindergartenChatbot
from student_profile import StudentProfileManager

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_section(title):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")

def simulate_student_interaction(chatbot, student_name, interactions):
    """Simulate a student learning session."""
    print_section(f"Starting session for {student_name}")
    
    # Start session
    greeting = chatbot.start_session(student_name)
    print(f"🎓 Teacher1: {greeting}")
    
    # Process interactions
    for i, user_input in enumerate(interactions, 1):
        print(f"\n👶 {student_name}: {user_input}")
        
        response, metadata = chatbot.get_response(user_input)
        print(f"🎓 Teacher1: {response}")
        
        if metadata:
            if metadata.get('lesson_started'):
                print(f"   📚 Started {metadata.get('subject', 'general')} lesson")
            if metadata.get('answer_processed'):
                print("   ✅ Answer processed and recorded")
            if metadata.get('break_suggested'):
                print("   ⏰ Break time suggested")
            if metadata.get('encouragement_provided'):
                print("   💪 Extra encouragement provided")
        
        # Small delay to simulate real interaction
        time.sleep(0.5)
    
    # End session
    goodbye = chatbot.end_session()
    print(f"\n🎓 Teacher1: {goodbye}")
    
    # Show progress summary
    summary = chatbot.get_student_progress_summary()
    print_section(f"Progress Summary for {student_name}")
    print(f"Learning Style: {summary.get('learning_style', 'Not determined yet')}")
    print(f"Total Sessions: {summary.get('total_sessions', 0)}")
    print(f"Needs Encouragement: {'Yes' if summary.get('needs_encouragement') else 'No'}")
    
    if summary.get('progress'):
        print("\nSubject Progress:")
        for subject, data in summary['progress'].items():
            if data['attempts'] > 0:
                success_rate = (data['successes'] / data['attempts']) * 100
                print(f"  {subject.title()}: Level {data['level']} - {success_rate:.0f}% success rate")
            else:
                print(f"  {subject.title()}: Level {data['level']} - No attempts yet")

def main():
    """Main demo function."""
    print_header("Teacher1 Kindergarten Individualized Learning Demo")
    print("This demo shows how Teacher1 adapts to individual kindergarten students")
    
    # Create chatbot
    chatbot = PersonalizedKindergartenChatbot()
    
    # Demo different student profiles and learning patterns
    students_scenarios = [
        {
            "name": "Emma",
            "interactions": [
                "Hi!",
                "I want to learn math",
                "4", 
                "Can you help me with reading?",
                "a",
                "I like math more",
                "What is 5 + 2?",
                "7"
            ]
        },
        {
            "name": "Jake", 
            "interactions": [
                "Hello teacher",
                "I don't know what to learn",
                "Can you teach me numbers?",
                "1, 2, 3, 4, 5",
                "This is hard",
                "I can't do this",
                "Help me please",
                "OK let me try again"
            ]
        },
        {
            "name": "Sofia",
            "interactions": [
                "Good morning!",
                "I love reading!",
                "Spell cat: C-A-T",
                "What about dog?",
                "D-O-G",
                "Can we do more spelling?",
                "Spell 'sun' please",
                "S-U-N"
            ]
        }
    ]
    
    # Run scenarios
    for scenario in students_scenarios:
        simulate_student_interaction(
            chatbot, 
            scenario["name"], 
            scenario["interactions"]
        )
        print("\n" + "-"*60)
        time.sleep(1)  # Pause between students
    
    # Show all student profiles
    print_header("Student Profile Summary")
    
    manager = StudentProfileManager()
    students = manager.list_students()
    
    for student_info in students:
        student = manager.load_student(student_info["student_id"])
        if student:
            print_section(f"Profile: {student.name}")
            print(f"Age: {student.age}")
            print(f"Sessions: {len(student.sessions)}")
            print(f"Preferred Learning Style: {student.get_preferred_learning_style()}")
            
            total_activities = sum(len(session.get('activities', [])) for session in student.sessions)
            print(f"Total Learning Activities: {total_activities}")
            
            if student.is_frustrated():
                print("⚠️  Student may need extra encouragement")
            else:
                print("😊 Student engagement is good")
    
    print_header("Demo Features Showcase")
    print("✅ Individual student profiles with persistent data")
    print("✅ Adaptive difficulty based on performance")
    print("✅ Learning style detection (visual, auditory, kinesthetic)")
    print("✅ Progress tracking across subjects (math, reading, spelling, numbers)")
    print("✅ Emotional state monitoring and appropriate responses")
    print("✅ Personalized encouragement based on student needs")
    print("✅ Session management with automatic progress saving")
    print("✅ Kindergarten-appropriate content and interactions")
    print("✅ Age-appropriate attention span management")
    print("✅ Multi-modal learning activity suggestions")
    
    print_header("Improvements for Individual Kindergarten Teaching")
    print("🎯 PERSONALIZATION:")
    print("   • Each student gets their own learning profile")
    print("   • System remembers progress across sessions")
    print("   • Adaptive difficulty prevents frustration and boredom")
    print("   • Learning style detection optimizes teaching approach")
    
    print("\n🎯 ASSESSMENT & PROGRESS:")
    print("   • Real-time progress tracking for each subject")
    print("   • Success rate monitoring for difficulty adjustment")
    print("   • Engagement and emotional state tracking")
    print("   • Detailed session history for teacher/parent review")
    
    print("\n🎯 KINDERGARTEN-SPECIFIC:")
    print("   • Age-appropriate interaction patterns")
    print("   • Attention span awareness and break suggestions")
    print("   • Positive reinforcement and encouragement system")
    print("   • Multi-sensory learning activity recommendations")
    print("   • Simple, clear feedback appropriate for 5-year-olds")
    
    print(f"\nDemo completed! Check the 'student_profiles' directory for saved data.")

if __name__ == "__main__":
    main()