# -*- coding: utf-8 -*-
from newsapi import NewsApiClient
from openai import OpenAI
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('openai_api_key')
NEWS_API_KEY = os.getenv('news_api_key')
MAX_ARTICLES_PER_QUERY = 100
MAX_PAGES = 1

access_date = datetime.date.today()
seven_days_ago = access_date - datetime.timedelta(days=7)

report_30_days_ago_date_api = seven_days_ago.strftime("%Y-%m-%d")
report_todays_date_api = access_date.strftime("%Y-%m-%d")

report_30_days_ago_date_display = seven_days_ago.strftime("%d %B %Y")
report_todays_date_display = access_date.strftime("%d %B %Y")
reporting_period_display = f"{report_30_days_ago_date_display} - {report_todays_date_display}"

newsapi = NewsApiClient(api_key=NEWS_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def news_retrieval(query: str) -> str:
    collected_text = ""
    for page in range(1, MAX_PAGES + 1):
        try:
            all_articles = newsapi.get_everything(
                q=query,
                from_param=report_30_days_ago_date_api,
                to=report_todays_date_api,
                language='en',
                sort_by='publishedAt',
                page=page,
                page_size=MAX_ARTICLES_PER_QUERY
            )
            articles = all_articles.get('articles', [])
            if not articles:
                break
            for article in articles:
                desc = article.get('description') or ""
                if desc:
                    collected_text += desc + "\n"
            time.sleep(1)
        except Exception as e:
            print(f"Error retrieving news for query '{query}': {e}")
            break
    return collected_text

def generate_executive_summary(text_for_summary: str) -> str:
    if not text_for_summary.strip():
        return "No relevant articles found for this reporting period."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": (
                "You are a senior Cyber Threat Intelligence Analyst. "
                "Provide an executive-level overview summarizing the following set of CTI findings. "
                "Write one concise paragraph capturing key trends and significant events. "
                "Maintain a factual and technical tone, active voice, and no assessments or predictions. "
                "ANY DATES REFERENCED SHOULD BE STRUCTURED AS DAY MONTH I.E. 23 OCTOBER."
                "EACH SUMMARY SHOULD BEGIN WITH 'During the reporting period, ..."
            )},
            {"role": "user", "content": text_for_summary},
        ]
    )
    return response.choices[0].message.content

def generate_overall_summary(all_summaries: list) -> str:
    combined_text = "\n".join(all_summaries)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": (
                "You are a senior Cyber Threat Intelligence Analyst. "
                "Provide an executive-level overview summarizing the following set of CTI findings. "
                "Write one concise paragraph capturing key trends and significant events. "
                "Maintain a factual and technical tone, active voice, and no assessments or predictions. "
                "ANY DATES REFERENCED SHOULD BE STRUCTURED AS DAY MONTH I.E. 23 OCTOBER."
                "EACH SUMMARY SHOULD BEGIN WITH 'During the reporting period, ..."
            )},
            {"role": "user", "content": combined_text},
        ]
    )
    return response.choices[0].message.content

def write_html_report_full(overall_summary, headers, all_summaries, access_date, info_date, reporting_period, filename="Cyber_Threat_Intelligence_Report.html"):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Cyber Threat Intelligence (CTI) Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    margin: 0;
    padding: 10px;
    color: inherit;  /* let Streamlit decide the text color */
}}
h1 {{
    font-size: 24pt;
    font-weight: bold;
    margin: 0;
}}
b {{
    font-weight: bold;
}}
p {{
    margin: 0.3em 0 1em 0;
}}
ul {{
    padding-left: 1.5em;
    margin: 0.5em 0 1em 0;
}}
li {{
    margin-bottom: 0.8em;
}}
hr {{
    border: 1px solid currentColor; /* inherit line color */
    margin: 10px 0;
}}
</style>
</head>
<body>
<h1>Cyber Threat Intelligence (CTI) Report</h1>
<p><b>Date of Access:</b> {access_date}</p>
<p><b>Date of Information:</b> {info_date}</p>
<p><b>Reporting Period:</b> {reporting_period}</p>
<p><b>Distribution:</b> Approved for public release; distribution is unlimited.</p>
<p><b>Intent:</b> The intent of this report is to provide a high-level overview of significant cyberspace developments during the reporting period. The report consists of open-source reporting and updates on vulnerabilities and exploits, ransomware and malware, and cyberattacks and campaigns.</p>
<hr>
<p><b>Executive Summary:</b> {overall_summary.strip()}</p>
<ul>
"""
    for header, summary in zip(headers, all_summaries):
        clean_summary = " ".join(summary.strip().splitlines())
        html_content += f'<li><b>{header}:</b> {clean_summary}</li>\n'

    html_content += "</ul>\n</body>\n</html>"

    with open(r'C:\Users\thisi\Desktop\Python_VSCode\venv\CTI Report Generator\Cyber_Threat_Intelligence_Report.html', "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Full HTML report saved as {filename}")


if __name__ == "__main__":
    query_list = [
        '(vulnerability OR vulnerabilities OR CVE OR exploit OR zero-day OR "security flaw" OR "remote code execution" OR RCE OR "privilege escalation" OR "buffer overflow") AND (discovered OR released OR patched OR announced)',
        '(ransomware OR "ransomware attack" OR "ransomware campaign" OR malware OR "malware campaign" OR trojan OR "remote access trojan" OR RAT OR "info stealer" OR infostealer OR botnet OR "malicious software" OR "malware infection" OR payload OR "threat actor" OR "malware variant") AND (discovered OR detected OR outbreak OR campaign OR attack OR infection OR "in the wild")',
        '("cyber attack" OR cyberattack OR "cyber campaign" OR "hacking campaign" OR "data breach" OR "security breach" OR intrusion OR "cyber espionage" OR "DDoS attack" OR "phishing campaign" OR "supply chain attack" OR "APT" OR "advanced persistent threat" OR "nation-state attack") AND (detected OR reported OR discovered OR ongoing OR attributed)',
        ]

    headers = [
        "Vulnerabilities & Exploits",
        "Ransomware & Malware",
        "Cyberattacks & Campaigns"
    ]

    all_summaries = []
    for query in query_list:
        text_block = news_retrieval(query)
        if not text_block.strip():
            all_summaries.append("No relevant articles found for this topic.")
            continue
        summary = generate_executive_summary(text_block)
        all_summaries.append(summary)

    overall_summary = generate_overall_summary(all_summaries)

    with open(r'C:\Users\thisi\Desktop\Python_VSCode\venv\CTI Report Generator\Cyber Threat Intelligence Report.txt', 'a', encoding='utf-8') as f:
        f.write(f"Cyber Threat Intelligence (CTI) Report\n")
        f.write(f"Date of Access: {report_todays_date_display}\n")
        f.write(f"Date of Information: {report_todays_date_display}\n")
        f.write(f"Reporting Period: {reporting_period_display}\n")
        f.write("Distribution: Approved for public release; distribution is unlimited.\n")
        f.write("The intent of this report is to provide a high-level overview of significant cyberspace developments during the reporting period. The report consists of open-source reporting and updates on vulnerabilities and exploits, ransomware and malware, and cyberattacks and campaigns.\n")
        f.write('-' * 45 + '\n')
        f.write(f"Executive Summary: {overall_summary.strip()}\n")
        for header, summary in zip(headers, all_summaries):
          f.write(f"{header}: {summary.strip()}\n")

    write_html_report_full(overall_summary, headers, all_summaries, report_todays_date_display,
                           report_todays_date_display, reporting_period_display)

    print("Cyber Threat Intelligence Report generated successfully.")