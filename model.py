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

