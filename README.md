# OSINT and Automation Scripts

This repository contains a collection of Python scripts for various OSINT (Open Source Intelligence) and automation tasks. The scripts cover a wide range of functionalities, from web scraping and data extraction to API interactions and report generation.

## Getting Started

To use these scripts, you'll need to set up your environment and install the necessary dependencies.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage the dependencies for this project.

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**On Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

**On macOS and Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Set Up API Keys

Many of the scripts in this repository require API keys to function. The project uses a `.env` file to manage these keys.

1.  Rename the `.env.example` file to `.env`.
2.  Open the `.env` file and add your API keys for the services you intend to use.

```
# .env file
abuseipdb_api_key='YOUR_ABUSEIPDB_API_KEY'
openai_api_key='YOUR_OPENAI_API_KEY'
news_api_key='YOUR_NEWS_API_KEY'
anthropic_api_key='YOUR_ANTHROPIC_API_KEY'
current_news_api_key='YOUR_CURRENTS_API_KEY'
dnsdumpster_api_key='YOUR_DNSDUMPSTER_API_KEY'
shodan_api_key='YOUR_SHODAN_API_KEY'
google_search_engine_id='YOUR_GOOGLE_SEARCH_ENGINE_ID'
google_api_key='YOUR_GOOGLE_API_KEY'
greynoise_api_key='YOUR_GREYNOISE_API_KEY'
apify_api_key='YOUR_APIFY_API_KEY'
proxy_check_api_key='YOUR_PROXYCHECK_API_KEY'
newsapi_key='YOUR_NEWSAPI_KEY'
newsdata_api_key='YOUR_NEWSDATA_API_KEY'
osint_industries_api_key='YOUR_OSINT_INDUSTRIES_API_KEY'
twilio_account_sid='YOUR_TWILIO_ACCOUNT_SID'
twilio_auth_token='YOUR_TWILIO_AUTH_TOKEN'
virus_total_api_key='YOUR_VIRUSTOTAL_API_KEY'
ipinfo_api_key='YOUR_IPINFO_API_KEY'
viewdns_api_key='YOUR_VIEWDNS_API_KEY'
alienvault_api_key='YOUR_ALIENVAULT_API_KEY'
```

### 6. External Dependencies

-   **FFMPEG:** The `YouTube Video Downloader.py` script requires FFMPEG to be installed on your system. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html).

## Script Descriptions

Here is a brief overview of each script in this repository:

-   **`abuseipdb_search.py`**: Checks the reputation of an IP address using the AbuseIPDB API.
-   **`ahmia_fi_scraper.py`**: Scrapes .onion links from the Ahmia.fi search engine.
-   **`alienvault_otx_search.py`**: Searches for IP address information on AlienVault OTX.
-   **`chatgpt_api.py`**: A simple command-line interface to interact with OpenAI's GPT models.
-   **`chinese_rss_search.py`**: Searches for keywords in various Chinese news RSS feeds.
-   **`claude_ai.py`**: Interacts with Anthropic's Claude API for text summarization.
-   **`CTI_Report_IP_Address.py`**: Generates a Cyber Threat Intelligence report for a given IP address, aggregating data from multiple sources.
-   **`currentapi_news.py`**: Fetches news articles from the Currents API.
-   **`cyber_threat_intelligence_report_generator.py`**: Generates a comprehensive CTI report based on news articles.
-   **`defang_urls.py`**: Defangs a list of URLs by replacing `.` with `[.]`.
-   **`disinformation_detection.py`**: Analyzes text for disinformation narratives using OpenAI's GPT models.
-   **`DNS_Records_Lookup.py`**: Performs a DNS lookup for a given domain.
-   **`DNSDumpster.py`**: Interacts with the DNSDumpster API to find DNS information about a domain.
-   **`email_extractor.py`**: Extracts email addresses from a given URL.
-   **`EXIF_Extractor.py`**: Extracts EXIF metadata from image files.
-   **`favicon_discovery.py`**: Finds websites with a matching favicon hash using Shodan.
-   **`file_metadata_analysis.py`**: Extracts metadata from various file types.
-   **`general_RSS_Search.py`**: Searches for keywords in a list of general news RSS feeds.
-   **`Get_IP_Address.py`**: Pings a domain to get its IP address.
-   **`Global SITREP Generator.py`**: Generates a global situation report from news articles.
-   **`Google News Scraper.py`**: Scrapes news articles from Google News.
-   **`google_search.py`**: Performs a Google Custom Search.
-   **`greynoise_ip_lookup.py`**: Looks up an IP address in the GreyNoise database.
-   **`HTTP_response_header_analysis.py`**: Analyzes the HTTP response headers of a website.
-   **`image_conversion.py`**: Converts images from one format to another.
-   **`image_scraper.py`**: Scrapes images from a webpage.
-   **`instagram_profile_scraper.py`**: Scrapes public Instagram profiles using the Apify API.
-   **`IP VPN Check.py`**: Checks if an IP address is a VPN or proxy.
-   **`IP_geolocation.py`**: Geolocates an IP address using the ipinfo.io API.
-   **`list_ips_proxy_checker.py`**: Checks a list of IP addresses for VPN or proxy usage.
-   **`news_summary_current_claude.py`**: Summarizes news articles from the Currents API using Anthropic's Claude.
-   **`newsapi_query_to_csv.py`**: Queries the NewsAPI and saves the results to a CSV file.
-   **`NewsDataAPI Search.py`**: Searches for news articles using the NewsData.io API.
-   **`osint_industries_search.py`**: Searches for information on OSINT Industries.
-   **`Phone Number VOIP Check.py`**: Checks if a phone number is a VoIP number using the Twilio API.
-   **`phone_number_extractor.py`**: Extracts phone numbers from a webpage.
-   **`ransomware_events_90_days_pygooglenews.py`**: Searches for ransomware events in the last 90 days using Google News.
-   **`reverse_IP_lookup.py`**: Performs a reverse IP lookup to find domains hosted on a given IP.
-   **`robotstxt_site_enum.py`**: Enumerates a website's `robots.txt` and `sitemap.xml` files.
-   **`russian_rss_search.py`**: Searches for keywords in various Russian news RSS feeds.
-   **`sentiment_analysis.py`**: Performs sentiment analysis on a text file.
-   **`shodan_ip_search.py`**: Searches for an IP address on Shodan.
-   **`simple_link_scraper.py`**: Scrapes all the links from a webpage.
-   **`status_check_up_or_down.py`**: Checks the status of a list of websites.
-   **`text_scraper.py`**: Scrapes the main text content from a webpage.
-   **`tiktok_scraper.py`**: Scrapes comments from TikTok videos using the Apify API.
-   **`top_keywords.py`**: Extracts the top keywords from a text file.
-   **`tor66_scraper.py`**: Scrapes .onion links from the Tor66 search engine.
-   **`tweet_scraper.py`**: Scrapes tweets from a Twitter handle using the Apify API.
-   **`virustotal_ip_lookup.py`**: Looks up an IP address on VirusTotal.
-   **`VPN_Proxy_Checker.py`**: Checks if an IP address is a VPN or proxy using the ProxyCheck.io API.
-   **`website_fingerprinting.py`**: Fingerprints a website by analyzing its HTTP headers.
-   **`whois_lookup.py`**: Performs a WHOIS lookup for a domain or IP address.
-   **`YouTube Video Downloader.py`**: Downloads a YouTube video.
-   **`youtube_channel_stats.py`**: Fetches statistics for a YouTube channel.
-   **`youtube_comments_download.py`**: Downloads comments from a YouTube video.
-   **`youtube_multi_channel_stats.py`**: Fetches statistics for multiple YouTube channels.