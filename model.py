from datetime import datetime


class Course:
    def __init__(self, course_id, name, course_code, assignments, gpa):
        self.course_id = course_id
        self.name = name
        self.course_code = course_code
        self.assignments = assignments
        self.gpa = gpa


class Assignment:
    def __init__(self, assignment_id: str, name: str, grade: str, course_id, due_at: datetime,
    lock_at,
                 html_url,
                 points_possible):
        self.assignment_id = assignment_id
        self.name = name
        self.grade = grade
        self.course_id = course_id
        self.due_at = due_at
        self.lock_at = lock_at
        self.html_url = html_url
        self.points_possible = points_possible

class Plannable:
    def __init__(self, plannable_id: str, context_type: str, title: str, plannable_date:
    datetime,
                 html_url:
    str):
        self.plannable_id = plannable_id
        self.context_type = context_type
        self.title = title
        self.plannable_date = plannable_date
        self.html_url = html_url
        
    def __str__(self):
        return f"Plannable ID: {self.plannable_id}, Type: {self.context_type}, Title: {self.title}, Created At: {self.created_at}, HTML URL: {self.html_url}"