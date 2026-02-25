
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app

env = os.getenv("FLASK_ENV", "development")

app = create_app(env)

if __name__ == "__main__":
    # Use gunicorn in production: gunicorn -w 4 "app:create_app()"
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_ENV") == "development"
    )
