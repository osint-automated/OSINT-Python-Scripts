from newsapi import NewsApiClient
import openai
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta

def get_news(query, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    try:
        one_day_ago = datetime.now() - timedelta(days=1)
        from_date = one_day_ago.strftime('%Y-%m-%d')
        all_articles = newsapi.get_everything(q=query, from_param=from_date)
        articles_text = "\n\n".join(
            [f"Title: {article.get('title')}\nDescription: {article.get('description')}"
             for article in all_articles['articles'] if article.get('title') and article.get('description')]
        )
        return articles_text
    except Exception as e:
        return None

def generate_summary(results, openai_api_key):
    llm = ChatOpenAI(model='gpt-4o-mini', api_key=openai_api_key)
    prompt = f'Take the following information and generate an informative summary paragraph highlighting military and geopolitical updates, using active voice, all facts, no fluffy language, past tense, this is for an OSINT report. Any date referenced should be structure as "day month" with the month spelled out i.e., 24 October, Each summary should being with During the reporting period, ...\n\n{results}'
    response = llm.invoke(prompt)
    return response.content

def generate_html_report(date_of_access, date_of_information, reporting_period_start, reporting_period_end, countries_list, executive_summary, individual_outputs):
    html_content = f"""
<!DOCTYPE html>
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
    <p><b>Countries:</b> {countries_list}</p>
    <p><b>Intent:</b> The intent of this report is to provide a high-level overview of significant military and
        geopolitical developments during the reporting period. The report consists of open-source reporting and updates
        on evolving conflicts, diplomatic initiatives, and strategic military actions involving Venezuela, Russia,
        Ukraine, China, Israel, Iran, and North Korea.</p>
    <hr>
    <p><b>Executive Summary:</b> {executive_summary}</p>
    <ul>
"""

    for item in individual_outputs:
        if ':' in item:
            country, summary = item.split(':', 1)
            html_content += f"""
        <li><b>{country.strip()}:</b> {summary.strip()}</li>
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
</html>
"""
    return html_content

def main():
    news_api_key = input('Enter NewsAPI API Key here: ')
    openai_api_key = input('Enter OpenAI API Key here: ')

    search_terms = ["Venezuela", "Russia", "Ukraine", "China", "Israel", "Iran", "North Korea"]
    country_codes = ["VEN", "RUS", "UKR", "CHN", "ISR", "IRN", "PRK"]
    all_summaries = []
    individual_outputs = []

    now = datetime.now()
    date_of_access = now.strftime("%d %B %Y")
    date_of_information = now.strftime("%d %B %Y")
    reporting_period_start = (now - timedelta(days=1)).strftime("%d %B")
    reporting_period_end = now.strftime("%d %B %Y")
    countries_list = ", ".join(country_codes)

    print("Open Source Intelligence (OSINT) Report")
    print(f"Date of Access: {date_of_access}")
    print(f"Date of Information: {date_of_information}")
    print(f"Reporting Period: {reporting_period_start} - {date_of_access}")
    print("Distribution: Approved for public release; distribution is unlimited.")
    print(f"Countries: {countries_list}")
    print('Intent: The intent of this report is to provide a high-level overview of significant military and geopolitical developments during the reporting period. The report consists of open-source reporting and updates on evolving conflicts, diplomatic initiatives, and strategic military actions involving Venezuela, Russia, Ukraine, China, Israel, Iran, and North Korea.')
    print("—" * 30)

    for search_term in search_terms:
        news_results = get_news(search_term, news_api_key)

        if news_results:
            summary = generate_summary(news_results, openai_api_key)
            all_summaries.append(f"{search_term}: {summary}")
            individual_outputs.append(f"{search_term}: {summary}\n")
        else:
            individual_outputs.append(f"No significant updates found for {search_term}.\n")

    if all_summaries:
        executive_summary_input = "\n\n".join(all_summaries)
        executive_summary = generate_summary(executive_summary_input, openai_api_key)
        print(f"Executive Summary: {executive_summary} \n")

    for output in individual_outputs:
        print(output)


    html_report = generate_html_report(
            date_of_access,
            date_of_information,
            reporting_period_start,
            reporting_period_end,
            countries_list,
            executive_summary,
            individual_outputs
        )

    with open(r"osint_report.html", "w", encoding="utf-8") as f:
        f.write(html_report)

if __name__ == "__main__":
    main()
