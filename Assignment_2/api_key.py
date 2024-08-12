import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

# Define the API key header
api_key_header = APIKeyHeader(name="Authorization")

# Define the API validate_api_keys
API_KEYS = os.getenv('API_KEYS')


# Define the API key validation function
async def validate_api_keys(api_key: str = Depends(api_key_header)):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

