"""
Kindergarten Learning Assessment Tool for Teacher1
--------------------------------------------------
Provides detailed assessment and reporting capabilities for individual students.
"""

import json
import datetime
from typing import Dict, List, Tuple
from student_profile import StudentProfileManager, KindergartenStudent

class KindergartenAssessment:
    """Assessment tool for analyzing kindergarten student progress."""
    
    def __init__(self):
        self.student_manager = StudentProfileManager()
        
        # Assessment criteria for kindergarten skills
        self.skill_levels = {
            "math": {
                1: "Counting 1-5, basic number recognition",
                2: "Counting 1-10, simple addition (1+1, 2+1)",
                3: "Counting 1-20, addition/subtraction up to 5",
                4: "Counting 1-50, addition/subtraction up to 10",
                5: "Counting 1-100, basic problem solving"
            },
            "reading": {
                1: "Letter recognition A-M, basic phonics",
                2: "Letter recognition A-Z, simple words",
                3: "Three-letter words, basic sentences",
                4: "Simple sentences, sight words",
                5: "Short stories, reading comprehension"
            },
            "spelling": {
                1: "Name spelling, 3-letter words",
                2: "Simple CVC words (cat, dog, sun)",
                3: "4-letter words, common words",
                4: "Simple sentences, familiar words",
                5: "Complex words, creative writing"
            },
            "numbers": {
                1: "Numbers 1-10, counting objects",
                2: "Numbers 1-20, number order",
                3: "Numbers 1-50, skip counting",
                4: "Numbers 1-100, number patterns",
                5: "Large numbers, mathematical concepts"
            }
        }
    
    def assess_student(self, student_name: str) -> Dict:
        """Generate comprehensive assessment for a student."""
        student = self.student_manager.get_student_by_name(student_name)
        if not student:
            return {"error": f"Student {student_name} not found"}
        
        assessment = {
            "student_name": student.name,
            "student_id": student.student_id,
            "age": student.age,
            "assessment_date": datetime.datetime.now().isoformat(),
            "total_sessions": len(student.sessions),
            "learning_profile": self._assess_learning_profile(student),
            "academic_progress": self._assess_academic_progress(student),
            "engagement_analysis": self._assess_engagement(student),
            "recommendations": self._generate_recommendations(student),
            "readiness_indicators": self._assess_readiness(student)
        }
        
        return assessment
    
    def _assess_learning_profile(self, student: KindergartenStudent) -> Dict:
        """Assess student's learning preferences and style."""
        return {
            "primary_learning_style": student.get_preferred_learning_style(),
            "learning_style_distribution": student.learning_style,
            "attention_span": f"{student.engagement['attention_span'] // 60} minutes",
            "engagement_pattern": self._analyze_engagement_pattern(student),
            "preferred_subjects": self._identify_preferred_subjects(student)
        }
    
    def _assess_academic_progress(self, student: KindergartenStudent) -> Dict:
        """Assess academic progress across all subjects."""
        progress = {}
        
        for subject, data in student.progress.items():
            success_rate = (data['successes'] / data['attempts']) if data['attempts'] > 0 else 0
            
            progress[subject] = {
                "current_level": data['level'],
                "skill_description": self.skill_levels[subject][data['level']],
                "attempts": data['attempts'],
                "success_rate": f"{success_rate:.1%}",
                "total_score": data['score'],
                "mastery_status": self._determine_mastery_status(success_rate, data['attempts']),
                "next_level_readiness": self._assess_level_readiness(success_rate, data['attempts'])
            }
        
        return progress
    
    def _assess_engagement(self, student: KindergartenStudent) -> Dict:
        """Analyze student engagement patterns."""
        total_responses = student.engagement['positive_responses'] + student.engagement['negative_responses']
        
        if total_responses == 0:
            engagement_score = "Insufficient data"
            positivity_rate = 0
        else:
            positivity_rate = student.engagement['positive_responses'] / total_responses
            if positivity_rate >= 0.8:
                engagement_score = "Highly engaged"
            elif positivity_rate >= 0.6:
                engagement_score = "Well engaged"
            elif positivity_rate >= 0.4:
                engagement_score = "Moderately engaged"
            else:
                engagement_score = "May need support"
        
        return {
            "overall_engagement": engagement_score,
            "positivity_rate": f"{positivity_rate:.1%}",
            "frustration_indicators": student.engagement['frustration_indicators'],
            "excitement_indicators": student.engagement['excitement_indicators'],
            "total_interactions": total_responses,
            "needs_encouragement": student.is_frustrated()
        }
    
    def _generate_recommendations(self, student: KindergartenStudent) -> List[str]:
        """Generate personalized learning recommendations."""
        recommendations = []
        
        # Learning style recommendations
        primary_style = student.get_preferred_learning_style()
        if primary_style == "visual":
            recommendations.append("Use more visual aids, pictures, and colorful materials")
            recommendations.append("Incorporate drawing and visual mapping activities")
        elif primary_style == "auditory":
            recommendations.append("Include more songs, rhymes, and verbal instructions")
            recommendations.append("Use storytelling and discussion-based learning")
        else:  # kinesthetic
            recommendations.append("Provide hands-on activities and movement-based learning")
            recommendations.append("Use manipulatives and interactive games")
        
        # Progress-based recommendations
        for subject, data in student.progress.items():
            if data['attempts'] > 0:
                success_rate = data['successes'] / data['attempts']
                if success_rate < 0.5:
                    recommendations.append(f"Consider review and reinforcement in {subject}")
                    recommendations.append(f"Break down {subject} concepts into smaller steps")
                elif success_rate > 0.8 and data['attempts'] >= 5:
                    recommendations.append(f"Ready to advance in {subject} - introduce new challenges")
        
        # Engagement recommendations
        if student.is_frustrated():
            recommendations.append("Provide extra encouragement and celebrate small victories")
            recommendations.append("Consider shorter learning sessions with more breaks")
        
        # Attention span recommendations
        if student.engagement['attention_span'] < 180:  # less than 3 minutes
            recommendations.append("Use very short activities (1-2 minutes) with frequent changes")
        elif student.engagement['attention_span'] < 300:  # less than 5 minutes
            recommendations.append("Break lessons into 3-5 minute segments")
        
        return recommendations if recommendations else ["Continue current approach - student is progressing well"]
    
    def _assess_readiness(self, student: KindergartenStudent) -> Dict:
        """Assess readiness for various kindergarten milestones."""
        readiness = {}
        
        # Math readiness
        math_score = self._calculate_readiness_score(student, 'math')
        readiness['mathematical_thinking'] = {
            "score": math_score,
            "ready_for": "Basic addition" if math_score >= 70 else "Number recognition practice"
        }
        
        # Reading readiness
        reading_score = self._calculate_readiness_score(student, 'reading')
        readiness['reading_readiness'] = {
            "score": reading_score,
            "ready_for": "Simple words" if reading_score >= 70 else "Letter sound practice"
        }
        
        # Overall kindergarten readiness
        overall_score = (math_score + reading_score) / 2
        if overall_score >= 80:
            readiness['overall'] = "Exceeds kindergarten expectations"
        elif overall_score >= 60:
            readiness['overall'] = "Meets kindergarten expectations"
        elif overall_score >= 40:
            readiness['overall'] = "Approaching kindergarten readiness"
        else:
            readiness['overall'] = "Needs additional support"
        
        return readiness
    
    def _calculate_readiness_score(self, student: KindergartenStudent, subject: str) -> int:
        """Calculate readiness score for a subject (0-100)."""
        if subject not in student.progress:
            return 0
        
        data = student.progress[subject]
        if data['attempts'] == 0:
            return 30  # Basic score for no attempts
        
        success_rate = data['successes'] / data['attempts']
        level_bonus = (data['level'] - 1) * 20  # Level progression bonus
        engagement_bonus = 10 if success_rate > 0.7 else 0
        
        score = min(100, int(success_rate * 50 + level_bonus + engagement_bonus + 30))
        return score
    
    def _analyze_engagement_pattern(self, student: KindergartenStudent) -> str:
        """Analyze student's engagement pattern."""
        if len(student.sessions) == 0:
            return "No session data"
        
        total_activities = sum(len(session.get('activities', [])) for session in student.sessions)
        avg_activities = total_activities / len(student.sessions)
        
        if avg_activities >= 8:
            return "High activity engagement"
        elif avg_activities >= 5:
            return "Good activity engagement"
        elif avg_activities >= 2:
            return "Moderate activity engagement"
        else:
            return "Low activity engagement"
    
    def _identify_preferred_subjects(self, student: KindergartenStudent) -> List[str]:
        """Identify student's preferred subjects based on engagement."""
        subject_scores = {}
        
        for subject, data in student.progress.items():
            if data['attempts'] > 0:
                success_rate = data['successes'] / data['attempts']
                engagement_score = success_rate * data['attempts']  # Weight by activity
                subject_scores[subject] = engagement_score
        
        if not subject_scores:
            return ["Insufficient data to determine preferences"]
        
        # Sort by engagement score
        sorted_subjects = sorted(subject_scores.items(), key=lambda x: x[1], reverse=True)
        return [subject for subject, score in sorted_subjects[:2]]  # Top 2 subjects
    
    def _determine_mastery_status(self, success_rate: float, attempts: int) -> str:
        """Determine mastery status for a subject."""
        if attempts < 3:
            return "Insufficient attempts"
        elif success_rate >= 0.9:
            return "Mastered"
        elif success_rate >= 0.7:
            return "Proficient"
        elif success_rate >= 0.5:
            return "Developing"
        else:
            return "Needs support"
    
    def _assess_level_readiness(self, success_rate: float, attempts: int) -> str:
        """Assess readiness to advance to next level."""
        if attempts < 5:
            return "Need more practice at current level"
        elif success_rate >= 0.85:
            return "Ready to advance"
        elif success_rate >= 0.7:
            return "Nearly ready to advance"
        else:
            return "Continue at current level"
    
    def generate_progress_report(self, student_name: str) -> str:
        """Generate a formatted progress report."""
        assessment = self.assess_student(student_name)
        
        if "error" in assessment:
            return assessment["error"]
        
        report = f"""
KINDERGARTEN LEARNING PROGRESS REPORT
====================================

Student: {assessment['student_name']}
Date: {assessment['assessment_date'][:10]}
Total Learning Sessions: {assessment['total_sessions']}

LEARNING PROFILE
---------------
Primary Learning Style: {assessment['learning_profile']['primary_learning_style'].title()}
Attention Span: {assessment['learning_profile']['attention_span']}
Engagement Pattern: {assessment['learning_profile']['engagement_pattern']}
Preferred Subjects: {', '.join(assessment['learning_profile']['preferred_subjects'])}

ACADEMIC PROGRESS
----------------"""
        
        for subject, progress in assessment['academic_progress'].items():
            report += f"""
{subject.upper()}:
  Current Level: {progress['current_level']} - {progress['skill_description']}
  Mastery Status: {progress['mastery_status']}
  Success Rate: {progress['success_rate']} ({progress['attempts']} attempts)
  Next Level: {progress['next_level_readiness']}"""
        
        report += f"""

ENGAGEMENT ANALYSIS
------------------
Overall Engagement: {assessment['engagement_analysis']['overall_engagement']}
Positive Response Rate: {assessment['engagement_analysis']['positivity_rate']}
Total Interactions: {assessment['engagement_analysis']['total_interactions']}
Needs Extra Encouragement: {'Yes' if assessment['engagement_analysis']['needs_encouragement'] else 'No'}

KINDERGARTEN READINESS
---------------------
Overall Readiness: {assessment['readiness_indicators']['overall']}
Math Skills: {assessment['readiness_indicators']['mathematical_thinking']['ready_for']}
Reading Skills: {assessment['readiness_indicators']['reading_readiness']['ready_for']}

RECOMMENDATIONS
--------------"""
        
        for i, rec in enumerate(assessment['recommendations'], 1):
            report += f"\n{i}. {rec}"
        
        return report

# Example usage and demonstration
if __name__ == "__main__":
    print("Kindergarten Assessment Tool Demo")
    print("=" * 50)
    
    assessment_tool = KindergartenAssessment()
    manager = StudentProfileManager()
    
    # Get all students
    students = manager.list_students()
    
    if not students:
        print("No student profiles found. Run the kindergarten_demo.py first.")
    else:
        for student_info in students:
            student_name = student_info['name']
            print(f"\nAssessment for {student_name}:")
            print("-" * 30)
            
            report = assessment_tool.generate_progress_report(student_name)
            print(report)
            print("\n" + "=" * 80)