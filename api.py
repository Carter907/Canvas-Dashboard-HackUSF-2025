import datetime

import pytz

import model

import os
import requests

import parse

access_token = os.environ.get('CANVAS_API_ACCESS_TOKEN')
api_url = "https://usflearn.instructure.com/api/v1/"
headers = {"Authorization": f"Bearer {access_token}"}


def call_canvas_api(path, parameters):
    return requests.get(api_url + path, headers=headers, params=parameters)


def get_all_courses():
    response = call_canvas_api('courses', parameters={})  # add sub error
    course_list = []

    if response.status_code == 200:
        courses = response.json()
        if courses:
            for course in courses:
                course_list.append(
                    model.Course(
                        course.get('id'),
                        course.get('name'),
                        course.get('course_code'),
                        get_all_assignments(course.get('id')),
                        get_gpa_for_course(course.get('id'))
                    )
                )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return course_list


def get_gpa_for_course(course_id) -> float:
    sum = 0
    count = 0
    assignment_list = get_all_assignments(course_id)

    if len(assignment_list) == 0:
        return None

    for assignment in assignment_list:
        grade = assignment.grade
        if grade is not None:
            if grade == "complete":
                grade = assignment.points_possible
            sum+=(float(grade)/assignment.points_possible)*100;
            count+=1;
    if count == 0:
        return 0
    return ((sum / count)/100.0) * 4;


def get_all_assignments(course_id):
    parameters = {
        'include[]': 'submission',
        'order_by': 'position',
        'per_page': '100',
    }
    response = call_canvas_api(f"courses/{course_id}/assignments", parameters)

    assignment_list: list[model.Assignment] = []

    est = pytz.timezone('US/Eastern')
    if response.status_code == 200:
        assignments = response.json()
        if assignments:
            for assignment in assignments:
                # assignment_id, course_id, due_at, lock_at, html_url, allowed_extensions
                if assignment.get('due_at') is None:
                    continue;
                assignment_list.append(
                    model.Assignment(
                        assignment_id=assignment.get('id'),
                        name=assignment.get('name'),
                        grade=assignment.get('submission').get('grade'),
                        course_id=assignment.get('course_id'),
                        due_at=datetime.datetime.strptime(assignment.get(
                            'due_at'), "%Y-%m-%dT%H:%M:%SZ")if assignment.get('due_at') else None,
                        lock_at=assignment.get('lock_at'),
                        html_url=assignment.get('html_url'),
                        points_possible=assignment.get('points_possible'),

                    )
                )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
    assignment_list.sort(key=lambda x: x.due_at if x.due_at else
    datetime.datetime.max,
                         reverse=True)

    assignment_list = assignment_list
    
    for assignment in assignment_list:
        if assignment.due_at:
            assignment.due_at = parse.convert_to_edt(assignment.due_at)

    return assignment_list
