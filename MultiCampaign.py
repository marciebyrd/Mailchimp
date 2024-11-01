import pandas as pd
from mailchimp_marketing import Client
from dotenv import load_dotenv
import os
import time  # for adding delays between API calls
from datetime import datetime
from string import Template

# Load environment variables
load_dotenv()

# Initialize Mailchimp client
mailchimp = Client()
mailchimp.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")
})

def get_email_template(row):
    """Read HTML template and substitute variables from Excel row"""
    try:
        # Read the template file
        with open('GN-template.html', 'r', encoding='utf-8') as file:
            template_content = file.read()
        
        # Handle optional secondary_body_text with type checking
        def clean_text(value):
            """Helper function to clean text values"""
            if pd.isna(value):  # Check if value is NaN
                return ''
            if isinstance(value, float):  # Convert float to string
                return '' if pd.isna(value) else str(value).rstrip('0').rstrip('.')
            return str(value).strip()  # Convert to string and strip whitespace
        
        # Clean the secondary text
        secondary_text = clean_text(row.get('secondary_body_text', ''))
        if not secondary_text:
            # Remove the entire paragraph containing secondary_body_text if it's empty
            template_content = template_content.replace('<p>secondary_body_text</p>', '')
        
        # Create template object
        template = Template(template_content)
        
        # Create dictionary of variables for substitution with cleaned values
        template_vars = {
            'campaign_name': clean_text(row['Campaign Name']),
            'subject_line': clean_text(row['subject_line']),
            'preview_text': clean_text(row['preview_text']),
            'green_body_header': clean_text(row['green_body_header']),
            'black_body_header': clean_text(row['black_body_header']),
            'body_text': clean_text(row['body_text']),
            'secondary_body_text': secondary_text,
            'testimonial_text': clean_text(row['testimonial_text']),
            'call_to_action_url': clean_text(row['call_to_action_url']),
            'call_to_action_text': clean_text(row['call_to_action_text'])
        }
        
        # Substitute variables in template
        html_content = template.safe_substitute(template_vars)
        
        print("Template loaded and variables substituted successfully")
        return html_content
        
    except FileNotFoundError:
        print("Error: GN-template.html not found in current directory")
        raise
    except Exception as e:
        print(f"Error processing template: {str(e)}")
        raise

def create_campaign_from_row(row):
    try:
        # Create campaign settings
        campaign_settings = {
            "recipients": {
                "list_id": row['List ID']
            },
            "settings": {
                "subject_line": row['subject_line'],
                "preview_text": row['preview_text'],
                "title": row['Campaign Name'],
                "from_name": row['From Name'],
                "reply_to": row['Reply-to Email']
            },
            "type": "regular"
        }
        
        print(f"\nCreating campaign: {row['Campaign Name']}")
        campaign = mailchimp.campaigns.create(campaign_settings)
        campaign_id = campaign['id']
        print(f"Campaign ID created: {campaign_id}")
        
        # Generate HTML content using template
        html_content = get_email_template(row)
        
        # Set campaign content
        content = {
            "html": html_content
        }
        print("Setting campaign content...")
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



