from datetime import datetime


class Course:
    def __init__(self, course_id, name, course_code, assignments, gpa):
        self.course_id = course_id
        self.name = name
        self.course_code = course_code
        self.assignments = assignments
        self.gpa = gpa

    def __repr__(self):
        return f"Course(course_id={self.course_id}, name={self.name}, course_code={self.course_code}, assignments={self.assignments}, gpa={self.gpa})"


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

    def __repr__(self):
        return f"Assignment(assignment_id={self.assignment_id}, name={self.name}, grade={self.grade}, course_id={self.course_id}, due_at={self.due_at}, lock_at={self.lock_at}, html_url={self.html_url}, points_possible={self.points_possible})"

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

    def __repr__(self):
        return f"Plannable(plannable_id={self.plannable_id}, context_type={self.context_type}, title={self.title}, plannable_date={self.plannable_date}, html_url={self.html_url})"