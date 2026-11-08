import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "web.app:app",
        host=os.getenv("VULNX_HOST", "127.0.0.1"),
        port=int(os.getenv("VULNX_PORT", "8000")),
    )
