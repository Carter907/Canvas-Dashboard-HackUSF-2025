import datetime
from typing import Any

import pytz
import model
import os
import requests
import parse


api_url = "https://usflearn.instructure.com/api/v1/"

def call_canvas_api(access_token, path, parameters):
    headers = {"Authorization": f"Bearer {access_token}"}

    return requests.get(api_url + path, headers=headers, params=parameters)


def get_all_courses(access_token):
    response = call_canvas_api(access_token, 'courses', parameters={})  # add sub error
    course_list = []

    if response.status_code == 200:
        courses = response.json()
        if courses:
            for course in courses:
                assignments = get_all_assignments(access_token, course.get('id'))
                if len(assignments) == 0:
                    continue;

                course_list.append(
                    model.Course(
                        course_id=course.get('id'),
                        name=course.get('name'),
                        course_code=course.get('course_code'),
                        gpa=get_gpa_for_course(access_token, course.get('id')),
                        assignments=assignments
                    )
                )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return course_list

def get_planner_events(access_token):
    start=datetime.date.today()
    parameters = {
        'start_date': start.strftime('%Y-%m-%d'),
    }

    response = call_canvas_api(access_token, 'planner/items', parameters=parameters)  # add sub
    # error
    planner_list = []

    if response.status_code == 200:
        items = response.json()
        if items:
            for planner_item in items:
                
                plannable_date=datetime.datetime.strptime(planner_item.get('plannable_date'), "%Y-%m-%dT%H:%M:%SZ")
                plannable_date=parse.convert_to_edt(plannable_date)

                planner_list.append(
                    model.Plannable(
                        plannable_id=planner_item.get('plannable_id'),
                        title=planner_item.get('plannable').get('title'),
                        plannable_date=plannable_date,
                        context_type=planner_item.get('context_type'),
                        html_url=planner_item.get('html_url'),
                    )
                )
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return planner_list


def get_gpa_for_course(access_token, course_id) -> None | int | float | Any:
    sum = 0
    count = 0
    assignment_list = get_all_assignments(access_token, course_id)

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

    course_gpa = ((sum / count)/100.0) * 4
    rounded_gpa = round(course_gpa * 100) / 100

    return rounded_gpa;

def get_total_gpa(courses: list[model.Course]):
    if len(courses) == 0:
        return None
    sum=0
    for course in courses:
        if course.gpa is None:
            sum+=4.0;
            continue
        sum+=course.gpa
    total_gpa = sum/len(courses)
    rounded_gpa = round(total_gpa*100)/100

    return rounded_gpa

def get_all_assignments(access_token, course_id):
    parameters = {
        'include[]': 'submission',
        'order_by': 'position',
        'per_page': '100',
    }
    response = call_canvas_api(access_token, f"courses/{course_id}/assignments", parameters)

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
                        due_at=datetime.datetime.strptime(assignment.get('due_at'), "%Y-%m-%dT%H:%M:%SZ"),
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
