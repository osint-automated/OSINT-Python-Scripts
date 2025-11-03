import os
import requests
import ipaddress
from datetime import datetime
from dotenv import load_dotenv

# Optional libraries
try:
    import shodan
except ImportError:
    shodan = None
try:
    import proxycheck
except ImportError:
    proxycheck = None
try:
    import whois
except ImportError:
    whois = None
try:
    import openai
except ImportError:
    openai = None

load_dotenv()

# ===================== Configuration =====================
OPENAI_KEY = os.getenv("openai_api_key")
SHODAN_KEY = os.getenv("shodan_api_key")
PROXYCHECK_KEY = os.getenv("proxy_check_api_key")
VT_KEY = os.getenv("virus_total_api_key")
ABUSEIPDB_KEY = os.getenv("abuseipdb_api_key")
OTX_KEY = os.getenv("alienvault_api_key")
IPINFO_KEY = os.getenv("ipinfo_api_key")
GREYNOISE_KEY = os.getenv("greynoise_api_key")

# ===================== Utility Functions =====================
def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def safe_join(value):
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    elif isinstance(value, str):
        return value
    return 'N/A'

def format_date(value):
    if isinstance(value, list):
        return str(value[0]) if value else 'N/A'
    return str(value) if value else 'N/A'

# ===================== Data Gathering =====================
def get_geolocation(ip):
    try:
        url = f"https://ipinfo.io/{ip}/json?token={IPINFO_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "ip": data.get("ip"),
            "hostname": data.get("hostname"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "org": data.get("org"),
            "loc": data.get("loc"),
            "timezone": data.get("timezone"),
            "anycast": data.get("anycast"),
        }
    except Exception:
        return {}

def get_proxycheck(ip):
    if proxycheck:
        try:
            client = proxycheck.Blocking(key=PROXYCHECK_KEY)
            info = client.ip(ip)
            is_proxy = info.proxy() if info else None
            risk = info.risk() if info else None
            lat, lon = info.geological() if info else (None, None)
            client.close()
            return {"is_proxy": is_proxy, "risk": risk, "latitude": lat, "longitude": lon}
        except Exception:
            pass
    try:
        url = f"https://proxycheck.io/v2/{ip}?key={PROXYCHECK_KEY}&vpn=1"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get(ip, {})
        return {"is_proxy": data.get("proxy"), "risk": data.get("risk"), "latitude": None, "longitude": None}
    except Exception:
        return {}

def get_shodan_data(ip):
    if shodan is None or not SHODAN_KEY:
        return {}
    try:
        api = shodan.Shodan(SHODAN_KEY)
        host = api.host(ip)
        return {
            "ip_str": host.get("ip_str"),
            "org": host.get("org"),
            "isp": host.get("isp"),
            "os": host.get("os"),
            "ports": host.get("ports"),
            "hostnames": host.get("hostnames"),
        }
    except Exception:
        return {}

def get_virustotal(ip):
    if not VT_KEY:
        return {}
    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": VT_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", {}).get("attributes", {})
        votes = data.get("total_votes", {})
        return {
            "asn": data.get("asn"),
            "as_owner": data.get("as_owner"),
            "country": data.get("country"),
            "network": data.get("network"),
            "reputation": data.get("reputation"),
            "malicious": votes.get("malicious", 0),
            "harmless": votes.get("harmless", 0),
        }
    except Exception:
        return {}

def get_abuseipdb(ip):
    if not ABUSEIPDB_KEY:
        return {}
    try:
        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
        params = {"ipAddress": ip, "maxAgeInDays": "90"}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("data", {})
    except Exception:
        return {}

def get_greynoise(ip):
    if not GREYNOISE_KEY:
        return {}
    try:
        url = f"https://api.greynoise.io/v3/community/{ip}"
        headers = {"key": GREYNOISE_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}

def get_otx(ip):
    if not OTX_KEY:
        return {}
    pulses = []

    # 1️⃣ Get direct indicator pulses
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"
        headers = {"X-OTX-API-KEY": OTX_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        for p in data.get("pulse_info", {}).get("pulses", []):
            pulses.append({
                "name": p.get("name"),
                "description": p.get("description"),
                "adversary": p.get("adversary"),
                "tags": p.get("tags"),
                "created": p.get("created"),
                "link": p.get("references")[0] if p.get("references") else None
            })
    except Exception as e:
        print(f"Error fetching general indicator pulses: {e}")

    # 2️⃣ Search pulses (first page only)
    try:
        url = "https://otx.alienvault.com/api/v1/search/pulses"
        params = {"q": ip, "limit": 10, "page": 1}
        headers = {"X-OTX-API-KEY": OTX_KEY}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for p in data.get("results", []):
            pulses.append({
                "name": p.get("name"),
                "description": p.get("description"),
                "adversary": p.get("adversary"),
                "tags": p.get("tags"),
                "created": p.get("created"),
                "link": p.get("references")[0] if p.get("references") else None
            })
    except Exception as e:
        print(f"Error fetching search pulses: {e}")

    # Remove duplicates by pulse name
    unique_pulses = {p['name']: p for p in pulses}.values()
    return {"pulse_count": len(unique_pulses), "pulses": list(unique_pulses)}

def get_whois_data(identifier):
    if whois is None:
        return {}
    try:
        data = whois.whois(identifier)
        return {
            "ip": identifier,
            "domain": safe_join(getattr(data, 'domain', 'N/A')),
            "registrar": getattr(data, 'registrar', 'N/A'),
            "creation_date": format_date(getattr(data, 'creation_date', 'N/A')),
            "expiration_date": format_date(getattr(data, 'expiration_date', 'N/A')),
            "updated_date": format_date(getattr(data, 'updated_date', 'N/A')),
            "name_servers": safe_join(getattr(data, 'name_servers', 'N/A')),
            "status": safe_join(getattr(data, 'status', 'N/A')),
            "emails": safe_join(getattr(data, 'emails', 'N/A')),
        }
    except Exception:
        return {}

# ===================== LLM Executive Summary =====================
def generate_executive_summary(report_text: str) -> str:
    if openai is None or not OPENAI_KEY:
        return "Executive Summary: OpenAI API key or library not configured."
    try:
        client = openai.OpenAI(api_key=OPENAI_KEY)
        prompt = (
            "You are a senior cyber threat analyst. Read the structured CTI data below and generate "
            "a detailed paragraph executive summary. Include all OTX pulses by name, adversary, and tags. "
            "Use professional technical tone, active voice. Do NOT include recommendations.\n\n"
            "Executive summary should begin with 'Open Source Cyber Threat Intelligence (CTI) data for the given IP indicates that...'\n\n"
            "Dates should be structured as day month, i.e., 5 October."
            f"CTI REPORT DATA:\n{report_text}\n\nExecutive Summary:"
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior cyber threat analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Executive Summary: Error generating executive summary: {e}"

def prepare_cti_text_for_llm(geo, proxy, shodan_data, vt, abuse, gn, otx, whois_data):
    lines = []
    for key in ["ip", "hostname", "city", "region", "country", "org", "loc", "timezone", "anycast"]:
        lines.append(f"{key}: {geo.get(key)}")
    for k in ["is_proxy", "risk", "latitude", "longitude"]:
        lines.append(f"{k}: {proxy.get(k)}")
    lines.append(f"Shodan Ports: {', '.join(map(str, shodan_data.get('ports', [])))}")
    lines.append(f"Shodan Hostnames: {', '.join(shodan_data.get('hostnames', []))}")
    for k in ["asn","as_owner","country","network","reputation","malicious","harmless"]:
        lines.append(f"{k}: {vt.get(k)}")
    for k in ["abuseConfidenceScore","totalReports","country","lastReported","categories"]:
        lines.append(f"{k}: {abuse.get(k)}")
    for k in ["classification","last_seen","noise_type"]:
        lines.append(f"{k}: {gn.get(k)}")

    pulses = otx.get("pulses", [])
    for p in pulses:
        lines.append(f"- {p.get('name')} | Adversary: {p.get('adversary')} | Tags: {', '.join(p.get('tags') or [])} | Created: {p.get('created')} | Link: {p.get('link')}")

    for k,v in whois_data.items():
        lines.append(f"{k}: {v}")
    return "\n".join(lines)

# ===================== Main =====================
def main():
    ip = input("Enter IP address: ").strip()
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return

    timestamp = datetime.now().strftime("%d %B %Y")
    geo = get_geolocation(ip)
    proxy = get_proxycheck(ip)
    shodan_data = get_shodan_data(ip)
    vt = get_virustotal(ip)
    abuse = get_abuseipdb(ip)
    gn = get_greynoise(ip)
    otx = get_otx(ip)
    whois_data = get_whois_data(ip)

    # LLM Summary
    cti_text = prepare_cti_text_for_llm(geo, proxy, shodan_data, vt, abuse, gn, otx, whois_data)
    exec_summary = generate_executive_summary(cti_text)

    # Write report
    report_lines = []
    report_lines.append("Cyber Threat Intelligence (CTI) Report")
    report_lines.append(f"Date of Access: {timestamp}")
    report_lines.append(f"Date of Information: {timestamp}")
    report_lines.append("Distribution: Approved for public release; distribution is unlimited.")
    report_lines.append("Intent: This report provides a high-level technical overview of CTI data for the specified IP.")
    report_lines.append(f"Executive Summary: {exec_summary}")
    report_lines.append("---------------------------------------------------")

    # Geolocation
    report_lines.append("Geolocation:")
    for key in ["ip", "hostname", "city", "region", "country", "org", "loc", "timezone", "anycast"]:
        report_lines.append(f"  {key.capitalize()}: {geo.get(key)}")

    # Proxy
    report_lines.append("\nVPN/Proxy Check:")
    for k in ["is_proxy","risk","latitude","longitude"]:
        report_lines.append(f"  {k.replace('_',' ').capitalize()}: {proxy.get(k)}")

    # Shodan
    report_lines.append("\nShodan Data:")
    for k in ["ip_str","org","isp","os","ports","hostnames"]:
        report_lines.append(f"  {k.replace('_',' ').capitalize()}: {shodan_data.get(k)}")

    # VirusTotal
    report_lines.append("\nVirusTotal Data:")
    for k in ["asn","as_owner","country","network","reputation","malicious","harmless"]:
        report_lines.append(f"  {k.capitalize()}: {vt.get(k)}")

    # WHOIS
    report_lines.append("\nWHOIS Data:")
    for k,v in whois_data.items():
        report_lines.append(f"  {k.replace('_',' ').capitalize()}: {v}")

    # GreyNoise
    report_lines.append("\nGreyNoise Data:")
    for k in ["classification","last_seen","noise_type"]:
        report_lines.append(f"  {k.replace('_',' ').capitalize()}: {gn.get(k)}")

    # AbuseIPDB
    report_lines.append("\nAbuseIPDB Data:")
    for k in ["ipAddress","abuseConfidenceScore","totalReports","country","lastReported","categories"]:
        report_lines.append(f"  {k}: {abuse.get(k)}")

    # OTX Pulses
    report_lines.append("\nAlienVault OTX Pulses:")
    for pulse in otx.get("pulses", []):
        report_lines.append(f"  Pulse Name: {pulse.get('name')}")
        report_lines.append(f"    Description: {pulse.get('description')}")
        report_lines.append(f"    Adversary: {pulse.get('adversary')}")
        report_lines.append(f"    Tags: {', '.join(pulse.get('tags') or [])}")
        report_lines.append(f"    Created: {pulse.get('created')}")
        report_lines.append(f"    Link: {pulse.get('link')}")

    report_lines.append("============================================================")

    filename = f"{ip}_CTI_Report.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"CTI report for {ip} saved to {filename}")

if __name__ == "__main__":
    main()
