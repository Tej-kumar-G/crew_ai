from crewai import Task
from agents import search_agent, download_agent, report_agent
from tools import url_search_tool, url_download_tool, report_tool

search_task = Task(
    description='Search for URLs related to the given vulnerability {vulnerability}.',
    expected_output='A list of URLs related to the vulnerability.',
    tools=[url_search_tool],
    agent=search_agent
)

download_task = Task(
    description='Download and clean content from the list of URLs.',
    expected_output='Cleaned text data from the URLs.',
    tools=[url_download_tool],
    agent=download_agent
)

# markdown_report_task = Task(
#     description='Generate a markdown vulnerability report based on downloaded data.',
#     expected_output='A comprehensive markdown report.',
#     tools=[markdown_report_tool],
#     agent=report_agent,
#     async_execution=False
# )
#
# html_report_task = Task(
#     description='Generate an HTML vulnerability report based on downloaded data.',
#     expected_output='A comprehensive HTML report.',
#     tools=[html_report_tool],
#     agent=report_agent,
#     async_execution=False
# )

report_task = Task(
    description='Generate a report based on those list of data.',
    expected_output='A comprehensive report.',
    tools=[report_tool],
    agent=report_agent,
    async_execution=False
)
