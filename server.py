import datetime

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import llm
import service

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")


@app.get("/events-list", response_class=HTMLResponse)
async def events_list(request: Request, access_token: str):
    events = service.get_planner_events(access_token)
    return templates.TemplateResponse(
        request=request,
        name="events.html",
        context={
            "events": events,

        }
    )


@app.get("/course-list", response_class=HTMLResponse)
async def course_list(request: Request, access_token: str):
    courses = service.get_all_courses(access_token)

    return templates.TemplateResponse(
        request=request,
        name="course-list.html",
        context={
            "courses": courses,
        }

    )


@app.get("/total-gpa", response_class=HTMLResponse)
async def total_gpa_page(request: Request, access_token: str):
    courses = service.get_all_courses(access_token)
    total_gpa = service.get_total_gpa(courses)

    return templates.TemplateResponse(
        request=request,
        name="total-gpa.html",
        context={
            "total_gpa": total_gpa,
        }
    )


@app.get("/course-advice", response_class=HTMLResponse)
async def course_advice(request: Request, access_token: str):
    courses = service.get_all_courses(access_token)
    total_gpa = service.get_total_gpa(courses)

    worst_course=courses[0]
    for course in courses:
        if course.gpa < worst_course.gpa:
            worst_course = course

    llm_advice = llm.assignment_advice(total_gpa, worst_course)


    return templates.TemplateResponse(
        request=request,
        name="course-advice.html",
        context={
            "advice": llm_advice,
        }
    )




@app.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, access_token: str = Form(...)):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "access_token": access_token
        }
    )

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
