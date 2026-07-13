import os
from dotenv import load_dotenv


load_dotenv()


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

print("GitHub Token:", GITHUB_TOKEN)