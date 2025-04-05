from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

import json
import requests
import os

access_token = os.environ.get('CANVAS_API_ACCESS_TOKEN')
api_url = "https://usflearn.instructure.com/api/v1/courses"
headers = {"Authorization": f"Bearer {access_token}"}

class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name
        
    def __str__(self):
        return f"Course ID: {self.course_id}, Name: {self.name}" 


def get_course_list():
    response = requests.get(api_url, headers=headers)
    course_list = []

    if response.status_code == 200:
        courses = response.json()
        if courses:
            for course in courses:
               id=course['id']
               name=course.get('name')
               course_list.append(Course(id, name))
                       
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return course_list


def prompt_llm(question):
    template = """Question: {question}
    Answer: Let's think step by step."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="gemma3:1b")
    chain = prompt | model
    return chain.invoke({"question": "What is LangChain?"})


if __name__ == "__main__":
    courses = get_course_list()
    for course in courses:
        print(course)