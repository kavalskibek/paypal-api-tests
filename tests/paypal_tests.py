from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = os.getenv('BASE_URL')

