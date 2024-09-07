import os
from dotenv import load_dotenv

def load_config():
    """Load environment variables."""
    load_dotenv()
    os.environ['HF_TOKEN'] = os.getenv("HF_TOKEN")
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
