from dotenv import load_dotenv
from smart_getenv import getenv


load_dotenv()

API_KEY = getenv('API_KEY', type=str)
ORG_ID = getenv('ORG_ID', type=str)
PROJECT_ID = getenv('PROJECT_ID', type=str)
TEMPLATE_BUILD_TARGET = getenv('TEMPLATE_BUILD_TARGET', type=str)
WEBHOOK_SECRET = getenv('WEBHOOK_SECRET', type=str)
