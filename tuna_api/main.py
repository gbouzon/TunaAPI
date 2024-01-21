#imports
from fastapi import FastAPI
from dotenv import find_dotenv, dotenv_values
import openai

app = FastAPI()

# load environment variables
config = dotenv_values(find_dotenv())
openai.api_key = config.get('CHATGPT_APIKEY')

# define endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}




