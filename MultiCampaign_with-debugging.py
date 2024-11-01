import pandas as pd
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import json

def create_multiple_campaigns():
    print("=== Starting Multiple Campaign Creation ===")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # Load environment variables and initialize client
        print("\n=== Setting up Mailchimp Client ===")
        load_dotenv()
        
        # Debug print environment variables (masked for security)
        api_key = os.getenv("MAILCHIMP_API_KEY")
        server = os.getenv("MAILCHIMP_SERVER_PREFIX")
        print(f"API Key found: {'Yes' if api_key else 'No'} (last 4 chars: {api_key[-4:] if api_key else 'None'})")
        print(f"Server prefix found: {'Yes' if server else 'No'} (value: {server})")

        mailchimp = Client()
        mailchimp.set_config({
            "api_key": api_key,
            "server": server
        })
        
        # Test connection with error details
        print("\n=== Testing Mailchimp Connection ===")
        try:
            ping_response = mailchimp.ping.get()
            print("Connection test response:", ping_response)
        except ApiClientError as e:
            print("Connection test failed!")
            print(f"Error Status Code: {e.status_code}")
            print(f"Error Detail: {e.text}")
            raise e

        # Read and validate campaign data
        print("\n=== Reading Campaign Data ===")
        try:
            df = pd.read_excel('campaigns.xlsx')
            print("Excel columns found:", df.columns.tolist())
            
            # Validate required columns
            required_columns = ['List ID', 'Subject Line', 'Preview Text', 
                              'Campaign Name', 'From Name', 'Reply-to Email', 
                              'Email Content']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Print first row data (masked for privacy)
            print("\nFirst row preview:")
            preview_row = df.iloc[0].copy()
            preview_row['Email Content'] = preview_row['Email Content'][:50] + '...'
            print(json.dumps(preview_row.to_dict(), indent=2))
            
        except Exception as e:
            print(f"Error reading Excel file: {str(e)}")
            return

        results = []

        # Process each campaign
        for index, row in df.iterrows():
            print(f"\n{'='*50}")
            print(f"Processing campaign {index + 1} of {len(df)}")
            
            try:
                # Validate row data
                for field in required_columns:
                    if pd.isna(row[field]) or str(row[field]).strip() == '':
                        raise ValueError(f"Missing or empty value for {field}")

                campaign_settings = {
                    "recipients": {
                        "list_id": str(row['List ID']).strip()  # Ensure list_id is string and trimmed
                    },
                    "settings": {
                        "subject_line": str(row['Subject Line']),
                        "preview_text": str(row['Preview Text']),
                        "title": str(row['Campaign Name']),
                        "from_name": str(row['From Name']),
                        "reply_to": str(row['Reply-to Email'])
                    },
                    "type": "regular"
                }
                
                print("\n=== Campaign Settings ===")
                print(json.dumps(campaign_settings, indent=2))

                try:
                    campaign = mailchimp.campaigns.create(campaign_settings)
                    campaign_id = campaign['id']
                    print(f"Campaign created with ID: {campaign_id}")
                except ApiClientError as e:
                    print("Campaign creation failed!")
                    print(f"Error Status Code: {e.status_code}")
                    print(f"Error Detail: {e.text}")
                    raise e

                content = {
                    "html": row['Email Content']
                }
                
                try:
                    content_response = mailchimp.campaigns.set_content(campaign_id, content)
                    print("Content set successfully")
                except ApiClientError as e:
                    print("Setting content failed!")
                    print(f"Error Status Code: {e.status_code}")
                    print(f"Error Detail: {e.text}")
                    raise e

                results.append({
                    'Date Created': datetime.now().strftime('%Y-%m-%d'),
                    'Time Created': datetime.now().strftime('%H:%M:%S'),
                    'Campaign Name': row['Campaign Name'],
                    'Campaign ID': campaign_id,
                    'Status': 'Success',
                    'Error': None
                })

            except Exception as e:
                error_detail = str(e)
                if isinstance(e, ApiClientError):
                    error_detail = f"Status: {e.status_code}, Detail: {e.text}"
                
                results.append({
                    'Date Created': datetime.now().strftime('%Y-%m-%d'),
                    'Time Created': datetime.now().strftime('%H:%M:%S'),
                    'Campaign Name': row['Campaign Name'],
                    'Campaign ID': None,
                    'Status': 'Failed',
                    'Error': error_detail
                })

            time.sleep(1)

        # Save results
        results_filename = f'campaign_results_{timestamp}.xlsx'
        results_df = pd.DataFrame(results)
        results_df.to_excel(results_filename, index=False)
        print(f"\nResults saved to: {results_filename}")

    except Exception as e:
        print(f"\n=== CRITICAL ERROR ===")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")

if __name__ == "__main__":
    create_multiple_campaigns()



