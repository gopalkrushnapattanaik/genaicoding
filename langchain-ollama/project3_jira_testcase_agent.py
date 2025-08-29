import os
from dotenv import load_dotenv
import pandas as pd
import requests
from langchain.tools import Tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import ollama

# Load environment variables
load_dotenv()
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
ollama_model = os.getenv("OLLAMA_MODEL", "llama2")

def generate_pytest_file_from_excel(jira_id: str, excel_path: str = "testcases.xlsx") -> str:
    df = pd.read_excel(excel_path)
    test_cases = []
    jira_col = None
    for col in df.columns:
        if str(col).strip().lower() in ["jira id", "jiraid"]:
            jira_col = col
            break
    if jira_col is None:
        return "No Jira ID column found in Excel file."
    filtered = df[df[jira_col].astype(str).str.strip().str.upper() == jira_id.strip().upper()]
    for _, row in filtered.iterrows():
        row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns if pd.notnull(row[col])])
        test_cases.append(row_text)
    if not test_cases:
        return f"No test cases found for Jira ID {jira_id} in {excel_path}"
    py_filename = f"{jira_id}_test.py"
    with open(py_filename, "w", encoding="utf-8") as pyfile:
        pyfile.write("import pytest\n\n")
        for tc in test_cases:
            prompt = (
                "You are a senior QA engineer. Convert the following test case information into a complete pytest-style test function in Python. "
                "Only output valid Python code as plain text. Do NOT include any markdown, code block markers, explanations, notes, or comments about assumptions. "
                "Only include necessary imports once at the top. If 'LoginPage' and 'HomePage' are needed, import them from 'app' at the top. Do not repeat imports. "
                f"Test Case Information:\n{tc}\n"
            )
            response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
            pytest_code = response["message"]["content"].strip()
            pyfile.write(pytest_code + "\n\n")
    return f"Pytest file generated: {py_filename}"

def test_case_to_pytest_code_tool(test_case_text: str) -> str:
    prompt = (
        f"""You are a senior QA engineer. Convert the following test case description into a complete pytest-style test function in Python.\nInclude all necessary assertions and use clear, descriptive naming.\n\nTest Case Description:\n{test_case_text}\n"""
    )
    response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
    pytest_code = response["message"]["content"]
    jira_id = os.environ.get("CURRENT_JIRA_ID", "unknown")
    py_filename = f"{jira_id}_test.py"
    write_header = not os.path.exists(py_filename)
    with open(py_filename, "a", encoding="utf-8") as pyfile:
        if write_header:
            pyfile.write("import pytest\n\n")
        pyfile.write(pytest_code + "\n\n")
    print(f"Pytest code appended to {py_filename}")
    return pytest_code

def story_to_test_case(user_story: str) -> str:
    prompt = f"""
        You are a senior QA engineer. Convert the following user story into at least 5 distinct, detailed test cases in plain text format (not code).\n        For each test case, generate a unique and descriptive test case title based on the user story provided.\n        Include for each test case:\n        - Test case title\n        - Preconditions\n        - Steps to execute\n        - Expected result\n\n        User Story:\n        {user_story}\n        """
    response = ollama.chat(model=ollama_model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def fetch_jira_story(jira_id: str) -> str:
    url = f"{JIRA_URL}/rest/api/2/issue/{jira_id}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {JIRA_API_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Jira issue: {response.text}")
    data = response.json()
    story = data['fields'].get('description') or data['fields'].get('summary')
    if not story:
        raise Exception("No user story or description found in Jira issue.")
    return story

tools = [
    Tool(
        name="JiraStoryFetcher",
        description="Fetches user story from Jira using issue ID",
        func=fetch_jira_story
    ),
    Tool(
        name="TestCaseGenerator",
        description="Generates at least 5 detailed test cases from a user story",
        func=story_to_test_case
    ),
    Tool(
        name="ExcelToPytestFileGenerator",
        description="Reads all test cases for a Jira ID from Excel and generates a single pytest file.",
        func=generate_pytest_file_from_excel
    ),
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a smart assistant that uses JiraStoryFetcher, TestCaseGenerator, and PytestCodeGenerator to help the user generate test cases and code from Jira IDs."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if __name__ == "__main__":
    jira_id = input("Enter Jira issue ID: ").strip()
    os.environ["CURRENT_JIRA_ID"] = jira_id
    result = agent_executor.invoke({"input": f"Generate test cases and pytest code for Jira ID {jira_id}"})
    pytest_code = result["output"]
    print("Agent Output:\n", pytest_code)
