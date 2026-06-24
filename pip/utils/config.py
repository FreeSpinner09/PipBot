import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEST_GUILD_ID = 1027186489672613918
print(f"TEST_GUILD_ID = {TEST_GUILD_ID}")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is missing from .env")
elif not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")
# elif not OPENAI_API_KEY:
#    raise ValueError("OPENAI_API_KEY is missing from .env")
