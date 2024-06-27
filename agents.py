from crewai import Agent
from tools import url_search_tool, url_download_tool, report_tool

search_agent = Agent(
    role='URL Search Agent',
    goal='Search for URLs related to the given vulnerability {vulnerability}.',
    verbose=True,
    memory=True,
    backstory=(
        'An expert in finding relevant URLs for vulnerabilities.'
    ),
    tools=[url_search_tool],
    allow_delegation=False
)

download_agent = Agent(
    role='URL Download Agent',
    goal='Download and clean content from the list of URLs.',
    verbose=True,
    memory=True,
    backstory=(
        'An expert in downloading and cleaning web content.'
    ),
    tools=[url_download_tool],
    allow_delegation=False
)

report_agent = Agent(
    role='Report Generation Agent',
    goal='Generate a detailed vulnerability report based on downloaded data.',
    verbose=True,
    memory=True,
    backstory=(
        'A specialist in creating comprehensive vulnerability reports.'
    ),
    tools=[report_tool],
    allow_delegation=False
)
