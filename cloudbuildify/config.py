from dotenv import load_dotenv
from smart_getenv import getenv


load_dotenv()

# Cloudbuild configuration
CLOUDBUILD_API_KEY = getenv('CLOUDBUILD_API_KEY', type=str)
CLOUDBUILD_WEBHOOK_SECRET = getenv('CLOUDBUILD_WEBHOOK_SECRET', type=str)
CLOUDBUILD_ORG_ID = getenv('CLOUDBUILD_ORG_ID', type=str)
CLOUDBUILD_PROJECT_ID = getenv('CLOUDBUILD_PROJECT_ID', type=str)
CLOUDBUILD_TEMPLATE_BUILD_TARGET = getenv('CLOUDBUILD_TEMPLATE_BUILD_TARGET', type=str)

# Bitbucket configuration
BITBUCKET_USER = getenv('BITBUCKET_USER', type=str)
BITBUCKET_PASSWORD = getenv('BITBUCKET_PASSWORD', type=str)
BITBUCKET_WEBHOOK_SECRET = getenv('BITBUCKET_WEBHOOK_SECRET', type=str)
BITBUCKET_ORG_ID = getenv('BITBUCKET_ORG_ID', type=str)
BITBUCKET_PROJECT_ID = getenv('BITBUCKET_PROJECT_ID', type=str)
