import os
from dotenv import load_dotenv

load_dotenv()

# Discord
TOKEN: str = os.getenv("DISCORD_TOKEN", "")

# Owner
OWNER_ID: int = int(os.getenv("OWNER_ID", "1042929958286266540"))

# Roblox API
ROBLOX_API_URL: str = os.getenv("ROBLOX_API_URL", "")
ROBLOX_API_KEY: str = os.getenv("ROBLOX_API_KEY", "")

# Database
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "database.db")
