from crewai import Crew, Process
from agents import search_agent, download_agent, report_agent
from tasks import search_task, download_task, report_task
from utils import clear_tmp_directory, save_report
import argparse

crew = Crew(
    agents=[search_agent, download_agent, report_agent],
    tasks=[search_task, download_task, report_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)


def main(vulnerability: str, count: int = 5):
    clear_tmp_directory("tempdir")
    result = crew.kickoff(inputs={'vulnerability': vulnerability, 'count': count})
    report_md = result
    save_report(report_md, '', vulnerability)
    print("Vulnerability exploration completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a vulnerability report.")
    parser.add_argument("vuln", type=str, help="Vulnerability CVE or Name for research")
    parser.add_argument("--count", type=int, default=5, help="Number of URLs to search (default: 5)")
    args = parser.parse_args()
    main(args.vuln, args.count)
