from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


def prompt_llm(question):
    template = """Question: {question}
    Answer: Let's think step by step."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="gemma3:1b")
    chain = prompt | model
    return chain.invoke({"question": "What is LangChain?"})