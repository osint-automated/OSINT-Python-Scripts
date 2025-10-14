from newsapi import NewsApiClient
import openai
from langchain_openai import ChatOpenAI
from datetime import datetime, timedelta

def get_news(query, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    try:
        seven_days_ago = datetime.now() - timedelta(days=1)
        from_date = seven_days_ago.strftime('%Y-%m-%d')
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
    prompt = f'Take the following information and generate an informative summary paragraph highlighting military and geopolitical updates, using active voice, all facts, no fluffy language, past tense, this is for an OSINT report. ensure that any locations are specified with their state or country (e.g., Atlanta, Georgia). Each summary should being with During the reporting period, ...\n\n{results}'
    response = llm.invoke(prompt)
    return response.content

def main():
    """
    Generates a global situation report by fetching news articles for specified countries,
    summarizing the results using OpenAI, and printing an executive summary and individual
    country updates.
    Prompts the user for NewsAPI and OpenAI API keys, retrieves news for a set of countries,
    summarizes each country's news, and produces an executive summary. Outputs the report
    with relevant metadata including date of access, date of information, reporting period,
    and country codes.
    Dependencies:
        - get_news(search_term, news_api_key): Function to fetch news articles.
        - generate_summary(text, openai_api_key): Function to summarize text using OpenAI.
        - datetime, timedelta: For date calculations.
    User Input:
        - NewsAPI key
        - OpenAI API key
    Output:
        - Prints the global situation report to the console.
    """
    news_api_key = input('Enter your NewsAPI key: ')
    openai_api_key = input('Enter your OpenAI API key: ')

    search_terms = ["Russia", "Ukraine", "China", "Israel", "Iran", "North Korea", "Venezuela"]
    country_codes = ["RUS", "UKR", "CHN", "ISR", "IRN", "PRK", "VEN"]
    all_summaries = []
    individual_outputs = []

    now = datetime.now()
    date_of_access = now.strftime("%d %B %Y")
    date_of_information = (now - timedelta(days=1)).strftime("%d %B %Y")
    reporting_period_start = (now - timedelta(days=1)).strftime("%d %B")
    reporting_period_end = (now - timedelta(days=1)).strftime("%d %B %Y")
    countries_list = ", ".join(country_codes)

    print("Global Situation Report")
    print(f"Date of Access: {date_of_access}")
    print(f"Date of Information: {date_of_information}")
    print(f"Reporting Period: {reporting_period_start} - {date_of_access}")
    print("Distribution: Approved for public release; distribution is unlimited.")
    print(f"Countries: {countries_list}")
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


if __name__ == "__main__":
    main()