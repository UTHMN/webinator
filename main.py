import flask
from playwright.sync_api import sync_playwright

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage

from os import path, getenv
from dotenv import load_dotenv

dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = Client()

(client
  .set_endpoint(str(getenv('APPWRITE_ENDPOINT'))) # Your API Endpoint
  .set_project(str(getenv('APPWRITE_PROJECT_ID'))) # Your project ID
  .set_key(str(getenv('APPWRITE_API_KEY'))) # Your secret API key
)

storage = Storage(client)
databases = Databases(client)

websites_queue = []

app = flask.Flask(__name__)

def getScreenshots(website):
    screenshots_id = flask.request.args.get('id')
    
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch()
            page = browser.new_page()
            page.goto(website)
            page.screenshot(path=f'example-{browser_type.name}.png')
            browser.close()

@app.route('/queue/')
def queue():
    pos = "temp"
    
    return f'in queue position {pos}'