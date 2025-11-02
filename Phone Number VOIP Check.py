import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv('twilio_account_sid')
AUTH_TOKEN = os.getenv('twilio_auth_token')
MAX_WORKERS = 10
INPUT_FILE = input("Enter the input CSV file name (with phone numbers): ")
OUTPUT_FILE = input("Enter the output CSV file name: ")

def check_number(client, phone_number: str) -> tuple[str, str]:
    """Looks up a phone number using Twilio and checks if it's VoIP."""
    try:
        lookup = client.lookups.v2.phone_numbers(phone_number).fetch(fields="line_type_intelligence")
        line_type = lookup.line_type_intelligence.get("type")
        return phone_number, "Yes" if line_type == 'voip' else "No"
    except TwilioRestException:
        return phone_number, "Error: Invalid Number"
    except Exception as e:
        return phone_number, f"Error: Request Failed ({type(e).__name__})"

def main():
    """
    Reads phone numbers from an input CSV file, checks each number using Twilio to determine if it is a VoIP number,
    and writes the results to an output CSV file. Utilizes multithreading for efficient processing. Handles missing
    Twilio credentials and file errors gracefully.
    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: For any unexpected errors during processing.
    """
    """Main function to read, process, and write phone number data."""
    if "YOUR_ACCOUNT_SID" in ACCOUNT_SID:
        print("ERROR: Please set your Twilio credentials in the script before running.")
        return

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
             open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f_out, \
             ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            writer.writerow(['PhoneNumber', 'Is_VoIP'])

            client = Client(ACCOUNT_SID, AUTH_TOKEN)

            futures = {
                executor.submit(check_number, client, row[0].strip()): row[0].strip()
                for row in reader if row and row[0].strip()
            }

            count = 0
            for future in as_completed(futures):
                phone_number, status = future.result()
                writer.writerow([phone_number, status])
                count += 1
            
            print(f"Processing complete. {count} numbers checked. Results saved to '{OUTPUT_FILE}'.")

    except FileNotFoundError:
        print(f"ERROR: Input file '{INPUT_FILE}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
