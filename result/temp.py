import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('REPLICATE_API_TOKEN'))