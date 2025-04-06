from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def assignment_advice(total_gpa, worst_course):
    template = """Give me guidance on how to increase my GPA of {total_gpa}.
    I'm struggling mainly with {worst_course}, which
    has a GPA of {worst_course_gpa}. Be concise on your advice (maximum 100 words), and don't use 
    markdown syntax."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="gemma3:1b")
    chain = prompt | model
    return chain.invoke(
        {
            "total_gpa": total_gpa,
            "worst_course": worst_course,
            "worst_course_gpa": worst_course.gpa,
        }
    )