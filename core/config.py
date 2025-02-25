import dotenv
import os

# Load environment variables from .env file
dotenv.load_dotenv('config.env')

# Access environment variables
port: int = int(os.getenv('PORT'))

