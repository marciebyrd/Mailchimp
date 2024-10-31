# Import required libraries
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading our secret keys from .env.local file
import mailchimp_marketing as MailchimpMarketing  # The main Mailchimp API library
from mailchimp_marketing.api_client import ApiClientError  # For handling Mailchimp errors

# Load our secret keys from .env.local file
load_dotenv()

# # Set up connection to Mailchimp
client = MailchimpMarketing.Client()

# Configure our connection using our secret API key and server
client.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),  # Get API key from .env.local
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")  # Get server prefix from .env.local
}) # Be careful with logging API keys in production!

def create_campaign(list_id, subject_line, preview_text, title, from_name, reply_to):
    # """
    # Creates a new email campaign in Mailchimp.

    try:
        # Create a new campaign with specified settings
        campaign = client.campaigns.create({
            "type": "regular",  # Standard email campaign
            "recipients": {
                "list_id": list_id  # Which mailing list to send to
            },
            "settings": {
                "subject_line": subject_line,
                "preview_text": preview_text,
                "title": title,
                "from_name": from_name,
                "reply_to": reply_to,
                "to_name": "*|FNAME|*"  # Will be replaced with recipient's first name
            }
        })
        print("New campaign created with ID:", campaign["id"])
        return campaign["id"]
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return None  # Add explicit return None

def add_content_to_campaign(campaign_id, html_content):
    # """
    # Adds HTML content to an existing campaign.
    
    # Parameters:
    #     campaign_id (str): The ID of the campaign to update
    #     html_content (str): The HTML content of the email
    # """
    try:
        # Add the HTML content to the campaign
        client.campaigns.set_content(campaign_id, {
            "html": html_content
        })
        print("Content added to campaign successfully")
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


# Example values - replace these with your actual information
    
    # Parameters:
    #     list_id (str): The ID of your mailing list in Mailchimp
    #     subject_line (str): What recipients will see as the email subject
    #     preview_text (str): The short preview text shown in email clients
    #     title (str): Internal name for the campaign (recipients don't see this)
    #     from_name (str): Name that will appear as the sender
    #     reply_to (str): Email address that will receive replies

list_id = "90c4971012"  # The ID of your Mailchimp mailing list
subject_line = "Your first exciting subject line"
preview_text = "A brief preview of your first email content"
title = "Internal title for your first campaign"
from_name = "Your Name or Company Name"
reply_to = "hoopster.lady@gmail.com"

# Example HTML template for the email
html_content = """
<html>
  <body>
    <h1>Hello, *|FNAME|*!</h1>
    <p>This is the content of your first email.</p>
  </body>
</html>
"""

# Create the campaign and add content to it
campaign_id = create_campaign(list_id, subject_line, preview_text, title, from_name, reply_to)
if campaign_id:  # Only proceed if we got a valid campaign_id
    add_content_to_campaign(campaign_id, html_content)
else:
    print("Failed to create campaign. Cannot add content.")

# End of file - To run this file, type "python3 Campaign.py" in the terminal

# Here's how to find your Mailchimp list ID:
# Log in to your Mailchimp account
# Go to Audience → All Contacts
# Click on "Settings" in the audience dropdown
# Click on "Audience name and defaults"
# You'll find your Audience ID at the bottom of the page. It will look something like "1234abcd56"
# Then update your code with the actual list ID: