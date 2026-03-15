from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import web_search, x_search
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(api_key=os.getenv('xai_api_key'))

def generate_summary(prompt):
    """Generate a summary paragraph from xAI."""
    
    chat = client.chat.create(
        model="grok-4-1-fast-reasoning",
        tools=[x_search(), web_search()],
    )

    chat.append(user(prompt))

    full_response = ""

    for response, chunk in chat.stream():
        if chunk.content:
            print(chunk.content, end="", flush=True)
            full_response += chunk.content

    print("\n")

    return full_response.strip()


def generate_executive_summary(results, openai_api_key):
    """Generate a concise executive summary from multiple OSINT summaries."""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=openai_api_key
    )

    prompt = (
        "Take the following OSINT summaries and generate an executive summary paragraph for an intelligence report."
        "Active voice only, technical tone only, dates should be structured as day month, past tense only."
        "Focus on the most critical military and geopolitical updates only."
        "Do not include any markdown formatting in the output."
        "Begin with 'During the reporting period, ...'\n\n"
        f"{results}"
    )

    response = llm.invoke(prompt)

    return response.content


def generate_html_report(date_of_access, date_of_information, reporting_period_start, reporting_period_end,
                         combatant_commands, executive_summary, individual_outputs):

    html_content = f"""<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open Source Intelligence (OSINT) Report</title>
</head>

<body>

<h1><b>Open Source Intelligence (OSINT) Report</b></h1>

<p><b>Date of Access:</b> {date_of_access}</p>
<p><b>Date of Information:</b> {date_of_information}</p>
<p><b>Reporting Period:</b> {reporting_period_start} - {reporting_period_end}</p>
<p><b>Distribution:</b> Approved for public release; distribution is unlimited.</p>
<p><b>Combatant Commands:</b> {combatant_commands}</p>

<p><b>Intent:</b> The intent of this report is to provide a high-level overview of significant military and
geopolitical developments during the reporting period. The report consists of open-source reporting and updates
on evolving conflicts, diplomatic initiatives, and strategic military actions involving countries of interest
in the following Combatant Commands: {combatant_commands}.</p>

<hr>

<p><b>Executive Summary:</b> {executive_summary}</p>

<ul>
"""

    for command, summary in individual_outputs:
        html_content += f"""
<li><b>{command}:</b> {summary}</li>
<br>
"""

    html_content += """
</ul>

</body>
</html>
"""

    return html_content


def main():

    openai_api_key = os.getenv('openai_api_key')

    search_terms = {
        "SOUTHCOM": "give me a comprehensive summary paragraph covering geopolitical and military events in the last 24 hours ONLY for central/south america, active voice only, technical tone only, past tense only, dates should be structured as day month. Do not include any markdown formatting in the output. Begin with 'During the reporting period, ...'",
        "EUCOM": "give me a comprehensive summary paragraph covering geopolitical and military events in the last 24 hours ONLY for the russia/ukraine conflict, active voice only, technical tone only, past tense only, dates should be structured as day month. Do not include any markdown formatting in the output. Begin with 'During the reporting period, ...'",
        "PACOM": "give me a comprehensive summary paragraph covering geopolitical and military events in the last 24 hours ONLY for China in the Pacific/PACOM, active voice only, technical tone only, past tense only, dates should be structured as day month. Do not include any markdown formatting in the output. Begin with 'During the reporting period, ...'",
        "CENTCOM": "give me a comprehensive summary paragraph covering geopolitical and military events in the last 24 hours ONLY for the US-Israel-Iran conflict, active voice only, technical tone only, past tense only, dates should be structured as day month. Do not include any markdown formatting in the output. Begin with 'During the reporting period, ...'",
        "AFRICOM": "give me a comprehensive summary paragraph covering geopolitical and military events in the last 24 hours ONLY for Africa, active voice only, technical tone only, past tense only, dates should be structured as day month. Do not include any markdown formatting in the output. Begin with 'During the reporting period, ...'"
    }

    all_summaries = []
    individual_outputs = []

    now = datetime.now()

    date_of_access = now.strftime("%d %B %Y")
    date_of_information = now.strftime("%d %B %Y")
    reporting_period_start = (now - timedelta(days=1)).strftime("%d %B")
    reporting_period_end = now.strftime("%d %B %Y")

    combatant_commands = ", ".join(search_terms.keys())

    print("Generating OSINT Report...\n")

    for command, query in search_terms.items():

        print(f"Generating summary for {command}...\n")

        summary = generate_summary(query)

        all_summaries.append(summary)
        individual_outputs.append((command, summary))

    print("Generating executive summary...\n")

    executive_summary = generate_executive_summary(
        "\n\n".join(all_summaries),
        openai_api_key
    )

    html_report = generate_html_report(
        date_of_access,
        date_of_information,
        reporting_period_start,
        reporting_period_end,
        combatant_commands,
        executive_summary,
        individual_outputs
    )

    with open("osint_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)

    print("Report generated successfully: osint_report.html")


if __name__ == "__main__":
    main()