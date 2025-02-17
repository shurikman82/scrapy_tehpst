import os
from dotenv import load_dotenv


load_dotenv()

ASYNC_CONNECTION_STRING = os.getenv('ASYNC_CONNECTION_STRING')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')