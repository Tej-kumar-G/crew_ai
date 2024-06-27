import os
import shutil
import markdown


def clear_tmp_directory(tmpdir_path: str):
    if os.path.exists(tmpdir_path):
        shutil.rmtree(tmpdir_path)
    os.makedirs(tmpdir_path)


def save_report(report_md: str, report_html: str, vulnerability: str):
    if not os.path.exists("reports"):
        os.makedirs("reports")
    output_file = f"reports/{vulnerability.lower().replace(' ', '_')}"
    with open(f"{output_file}.md", "w", encoding="utf-8") as markdown_file:
        markdown_file.write(report_md)
    with open(f"{output_file}.html", "w", encoding="utf-8") as html_file:
        html_file.write(report_html)

    append_task_info_to_report(output_file)


def append_task_info_to_report(output_file: str):
    with open("task_info.md", "r") as md_file:
        task_info_md = md_file.read()

    with open(f"{output_file}.md", "a", encoding="utf-8") as markdown_file:
        markdown_file.write("\n\n" + task_info_md)

    with open("task_info.html", "r") as html_file:
        task_info_html = html_file.read()

    with open(f"{output_file}.html", "a", encoding="utf-8") as html_file:
        html_file.write("<br><br>" + task_info_html)
