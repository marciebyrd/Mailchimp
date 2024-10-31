from mailchimp_marketing import Client
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading our secret keys from .env.local file

# Load our secret keys from .env.local file
load_dotenv()

mailchimp = Client()
mailchimp.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")
})


response = mailchimp.ping.get()
print(response)