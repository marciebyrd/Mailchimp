import pandas as pd
from mailchimp_marketing import Client
from dotenv import load_dotenv
import os
import time  # for adding delays between API calls
from datetime import datetime
# Load environment variables
load_dotenv()

# Initialize Mailchimp client
mailchimp = Client()
mailchimp.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")
})

def create_campaign_from_row(row):
    try:
        # Create campaign
        campaign_settings = {
            "recipients": {
                "list_id": row['List ID']
            },
            "settings": {
                "subject_line": row['Subject Line'],
                "preview_text": row['Preview Text'],
                "title": row['Campaign Name'],
                "from_name": row['From Name'],
                "reply_to": row['Reply-to Email']
            },
            "type": "regular"
        }
        
        campaign = mailchimp.campaigns.create(campaign_settings)
        campaign_id = campaign['id']
        
        # Add content
        content = {
            "html": row['Email Content']
        }
        mailchimp.campaigns.set_content(campaign_id, content)
        
        print(f"Successfully created campaign: {row['Campaign Name']}")
        return True, campaign_id
        
    except Exception as e:
        print(f"Failed to create campaign {row['Campaign Name']}: {str(e)}")
        return False, None

def main():
    # Read the Excel file
    df = pd.read_excel('campaigns.xlsx')
    
    results = []
    
    # Process each row
    for index, row in df.iterrows():
        success, campaign_id = create_campaign_from_row(row)
        
        # Store results
        results.append({
            'Campaign Name': row['Campaign Name'],
            'Success': success,
            'Campaign ID': campaign_id
        })
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)
    
    # Create a results DataFrame and save to Excel
    results_df = pd.DataFrame(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_df.to_excel(f'{timestamp}_campaign_results.xlsx', index=False)

if __name__ == "__main__":
    main()

    # This script creates a new campaign for each row from the campaigns.xlsx file.
    # to run the code type python3 MultiCampaign.py in the terminal
    # the results will be saved in a file called <timestamp>_campaign_results.xlsx



