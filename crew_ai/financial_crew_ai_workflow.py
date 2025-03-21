import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun

# Import Secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def create_ai_financial_news_workflow():
    
    # Tools
    search_tool = DuckDuckGoSearchRun()

    # Define your agents with roles and goals
    researcher = Agent(
        role='Financial News Researcher',
        goal='Research and summarize the latest financial news',
        backstory="""You are an experienced financial analyst with a keen eye for market trends.
        Your expertise lies in distilling complex financial information into concise summaries.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    )

    writer = Agent(
        role='Financial Content Writer',
        goal='Craft engaging summaries of financial news',
        backstory="""You are a seasoned financial writer known for making intricate financial topics accessible to a broad audience.""",
        verbose=True,
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
        allow_delegation=True
    )

    # Create tasks for your agents
    task1 = Task(
        description="""Research and summarize the latest financial news for 2025.
        Identify key trends, significant events, and potential market impacts.""",
        expected_output="Bullet-point summary of the latest financial news",
        llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"),
        agent=researcher
    )

    task2 = Task(
        description="""Using the research provided, develop an engaging summary
        that highlights the most significant financial news.
        The summary should be informative yet accessible, catering to a financially savvy audience.
        Ensure clarity and conciseness.""",
        expected_output="""Python Dictionanry of Summary Title and Comprehensive financial news summary of at least 4 paragraphs.
        The summary should be informative yet accessible, catering to a financially savvy audience.
        Ensure clarity and conciseness.
        
        Result Example:
        {
            "title": "Financial News Summary - 2025",
            "summary": "The financial markets in 2025 have been marked by significant volatility..."
        }
        """,
        agent=writer
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2,  # You can set it to 1 or 2 for different logging levels
    )

    # Get your crew to work!
    result = crew.kickoff()

    print("######################")
    return result

# To Test in Local
# result = create_ai_financial_news_workflow()
# print(result)
