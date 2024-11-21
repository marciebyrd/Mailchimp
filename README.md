# Mailchimp

## Here's a step-by-step guide on how to use the MultiCampaign script:
###First, prepare your Excel file (campaigns.xlsx) with these columns:
Required columns:
- Campaign Name
- subject_line
- preview_text
- green_body_header
- black_body_header
- body_text
- List ID
- From Name
- Reply-to Email
- call_to_action_url
- call_to_action_text

Optional columns:
- secondary_body_text
- testimonial_text

## File Structure - Make sure you have these files in the same directory:
- campaigns.xlsx
- MultiCampaign.ts
- .env
### 2. Set up your .env file
- Your .env should include the following:
```
MAILCHIMP_API_KEY=your_api_key_here
MAILCHIMP_SERVER_PREFIX=your_server_prefix
```
## Example Excel Row
Campaign Name: Spring Garden Update
subject_line: Spring is Here! 🌱
preview_text: Check out our latest garden updates
green_body_header: Spring Update
black_body_header: Garden News
body_text: We're excited to share our latest garden updates...
List ID: abc123def456 (your actual Mailchimp list ID)
From Name: Grow Nashua
Reply-to Email: contact@grownashua.org
call_to_action_url: https://www.grownashua.org/volunteer
call_to_action_text: Volunteer Today!
secondary_body_text: (can be left blank)
testimonial_text: (can be left blank)

## Run the script
```
Make sure your virtual environment is activated
source .venv/bin/activate  # On Mac/Linux
OR
.venv\Scripts\activate     # On Windows

Run the script
python3 MultiCampaign.py
```
## Check Results
The script will create a timestamped results file (e.g., 20240319_143022_campaign_results.xlsx)
This file will show which campaigns were created successfully and any errors
Common Issues and Solutions:
If you get API errors, check your Mailchimp credentials
If template errors occur, verify all required columns exist in your Excel file
For file not found errors, check that all files are in the correct directory
