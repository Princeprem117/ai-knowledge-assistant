import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
# get the .env values to the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#model
MODEL_NAME="llama-3.3-70b-versatile"
#response settings

MAX_TOKENS=1024
TEMPERATURE=0.7

#storage
HISTORY_FILE ='data/history.json'
CHROMA_PERSIST_DIRECTORY = "data/chroma"
#app
APP_NAME = "AI Knowledge Assistant"
#embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"