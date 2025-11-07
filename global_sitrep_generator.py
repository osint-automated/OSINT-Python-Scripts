"""
This script generates a Global Situation Report (SITREP) by fetching news
articles from various combatant commands (SOUTHCOM, EUCOM, PACOM, CENTCOM, AFRICOM).
It uses the NewsAPI to get the news and the OpenAI API (GPT-4o-mini) to generate
summaries and an executive summary. The final report is saved as an HTML file.
"""
from newsapi import NewsApiClient
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def get_news(query, api_key):
    """Fetch recent news articles from NewsAPI for a given query."""
    newsapi = NewsApiClient(api_key=api_key)
    try:
        one_day_ago = datetime.now() - timedelta(days=1)
        from_date = one_day_ago.strftime('%Y-%m-%d')
        all_articles = newsapi.get_everything(
            q=query,
            from_param=from_date,
            language='en',
            sort_by='relevancy',
            page_size=50
        )
        articles_text = "\n\n".join(
            [f"Title: {a.get('title')}\nDescription: {a.get('description')}"
             for a in all_articles['articles'] if a.get('title') and a.get('description')]
        )
        return articles_text
    except Exception as e:
        print(f"[Error] Fetching news for '{query}': {e}")
        return None


def generate_summary(results, openai_api_key):
    """Use GPT model to summarize news results into an OSINT-style report paragraph."""
    llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=openai_api_key)
    prompt = (
        "Take the following information and generate an informative summary paragraph highlighting "
        "military and geopolitical updates, using active voice, all facts, no fluffy language, past tense. "
        "This is for an OSINT report. Ensure that any locations are specified with their state or country "
        "(e.g., Atlanta, Georgia). Any date referenced should be structured as 'day month' (e.g., 24 October). "
        "Each summary should begin with 'During the reporting period, open source reporting indicated.....'\n\n"
        f"{results}"
    )
    response = llm.invoke(prompt)
    return response.content


def generate_executive_summary(results, openai_api_key):
    """Generate a concise executive summary from multiple OSINT summaries."""
    llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=openai_api_key)
    prompt = (
        "Take the following OSINT summaries and generate a concise executive summary paragraph. "
        "Active voice, all facts, no fluffy language, past tense."
        "Focus on the most critical military and geopolitical updates only, using clear and factual language. "
        "Keep it concise and high-level.\n\n"
        f"{results}"
    )
    response = llm.invoke(prompt)
    return response.content


def generate_html_report(date_of_access, date_of_information, reporting_period_start, reporting_period_end,
                         combatant_commands, executive_summary, individual_outputs):
    """Generate HTML content following the provided OSINT report structure exactly."""
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
        on evolving conflicts, diplomatic initiatives, and strategic military actions involving countries of interest in the following Combatant Commands: {combatant_commands}.</p>
    <hr>
    <p><b>Executive Summary:</b> {executive_summary}</p>
    <ul>
"""

    for item in individual_outputs:
        if ':' in item:
            command, summary = item.split(':', 1)
            html_content += f"""
        <li><b>{command.strip()}:</b> {summary.strip()}</li>
        <br>
"""
        else:
            html_content += f"""
        <li>{item.strip()}</li>
        <br>
"""

    html_content += """
    </ul>
</body>
</html>"""
    return html_content


def main():
    news_api_key = os.getenv('news_api_key')
    openai_api_key = os.getenv('openai_api_key')

    # Search terms mapped to combatant commands
    search_terms = {
        "SOUTHCOM": "Venezuela AND (Russia OR United States OR USA OR US OR U.S.)",
        "EUCOM": "Ukraine AND Russia OR NATO",
        "PACOM": "China OR North Korea OR Taiwan OR South China Sea",
        "CENTCOM": "Iran OR Israel OR Gaza OR Hamas OR Lebanon OR Syria",
        "AFRICOM": 'Sudan OR "South Sudan" OR Nigeria OR Libya OR Mali OR Niger OR Chad OR "Burkina Faso" OR "Central African Republic" OR Somalia OR Ethiopia OR Eritrea OR Djibouti OR Mozambique OR "Democratic Republic of Congo" OR "Equatorial Guinea" OR Angola OR "South Africa" OR Zimbabwe OR Cameroon OR Algeria'
    }

    all_summaries = []
    individual_outputs = []

    now = datetime.now()
    date_of_access = now.strftime("%d %B %Y")
    date_of_information = now.strftime("%d %B %Y")
    reporting_period_start = (now - timedelta(days=1)).strftime("%d %B")
    reporting_period_end = now.strftime("%d %B %Y")
    combatant_commands = ", ".join(search_terms.keys())

    print("Generating OSINT Report.\n")

    # Generate per-command summaries
    for command, query in search_terms.items():
        print(f"Fetching and summarizing {command} news...")
        news_results = get_news(query, news_api_key)

        if news_results:
            summary = generate_summary(news_results, openai_api_key)
            all_summaries.append(f"{command}: {summary}")
            individual_outputs.append(f"{command}: {summary}")
        else:
            individual_outputs.append(f"{command}: No significant updates found.")

    # Generate concise executive summary combining all
    print("\nGenerating executive summary...")
    executive_summary_input = "\n\n".join(all_summaries)
    executive_summary = generate_executive_summary(executive_summary_input, openai_api_key)

    # Create HTML report
    html_report = generate_html_report(
        date_of_access,
        date_of_information,
        reporting_period_start,
        reporting_period_end,
        combatant_commands,
        executive_summary,
        individual_outputs
    )

    # Save report
    with open('osint_report.html', "w", encoding="utf-8") as f:
        f.write(html_report)

    print(f"\nReport generated successfully: 'osint_report.html'")

if __name__ == "__main__":
    main()
