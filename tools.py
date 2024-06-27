import os
import requests
from bs4 import BeautifulSoup
import html2text
import re
import json
import markdown
from googlesearch import search
from crewai_tools import BaseTool
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI


class WebsiteSearchTool(BaseTool):
    name: str = "Website Search Tool"
    description: str = "Searches for URLs related to a given topic."

    def _run(self, topic: str, count: int = 5) -> list:
        topic = topic.split('-')[0]
        search_terms = [
            "exploit wild", "vulnerability mitigation", "security blog",
            "patch detection", "new zeroday", "securing", "critical alert"
        ]
        urls = []
        for term in search_terms:
            for url in search(f"{topic} {term}", num_results=count):
                urls.append(url)
        return sorted(set(urls))


class WebsiteDownloadTool(BaseTool):
    name: str = "Website Download Tool"
    description: str = "Downloads and cleans content from a list of URLs."

    def _run(self, url_list: list) -> list:
        list_jsons = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.download_and_clean, url) for url in url_list]
            for future in as_completed(futures):
                text = future.result()
                if text:
                    json_text = json.dumps(text)
                    list_jsons.append(json_text)
        return list_jsons

    def download_and_clean(self, url: str) -> str:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style", "img", "a"]):
                script.extract()
            body_text = soup.get_text()
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.ignore_emphasis = True
            h.ignore_tables = True
            clean_text = h.handle(body_text)
            clean_text = re.sub(r'[^\w\s\n<>/]+', '', clean_text)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            return clean_text
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return None


# class MarkdownReportTool(BaseTool):
#     name: str = "Markdown Report Tool"
#     description: str = "Generates a detailed markdown vulnerability report based on downloaded data."
#
#     def _run(self, list_of_jsons: list) -> str:
#         report_md = ""
#         for json_text in list_of_jsons:
#             report_md += json.loads(json_text) + "\n\n"
#         return report_md
#
#
# class HTMLReportTool(BaseTool):
#     name: str = "HTML Report Tool"
#     description: str = "Generates a detailed HTML vulnerability report based on downloaded data."
#
#     def _run(self, list_of_jsons: list) -> str:
#         markdown_tool = MarkdownReportTool()
#         report_md = markdown_tool._run(list_of_jsons)
#         report_html = markdown.markdown(report_md, extensions=["markdown.extensions.extra"])
#         return report_html

class ReportTool(BaseTool):
    name: str = "Report Tool"
    description: str = "Generates a detailed vulnerability report based on downloaded data."

    def _run(self, list_of_jsons) -> tuple:
        if isinstance(list_of_jsons, list):
            content = ''.join([item['content'] for item in list_of_jsons])
        else:
            content = list_of_jsons
        # with open(data_file, "r", encoding="utf-8") as file:
        #     report = file.read()

        system_template = """You are a Research Analyst, specialized in writing connected informative reports. \
        You will analyze question and answers given, and writes well-connected, actionable, and informative reports.
        """
        system_message_prompt_template = SystemMessagePromptTemplate.from_template(system_template)

        human_template = """Write vulnerability report following sections: description, vulnerability details, 
        affected products and impact, vulnerability identifiers threat actors using vulnerability, exploitation 
        details, mitigations, recommendations short-term and long-term strategies, references focus only on available 
        information using markdown format and try using available information without losing. \n\nInterview Summary 
        Information:{report_information}"""

        human_message_prompt_template = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt_template, human_message_prompt_template])



        final_prompt = chat_prompt_template.format_prompt(report_information=content).to_messages()
        chat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")
        completion = chat(final_prompt)

        report_md = completion.content
        report_html = markdown.markdown(report_md, extensions=["markdown.extensions.extra"])

        return report_md, report_html


url_search_tool = WebsiteSearchTool()
url_download_tool = WebsiteDownloadTool()
# markdown_report_tool = MarkdownReportTool()
# html_report_tool = HTMLReportTool()

report_tool = ReportTool()
