from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.scanner import Scanner
from core.storage import save, recent
from reports.generator import write_reports

app = FastAPI(title="VulnX", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="web/static"), name="static")


class ScanRequest(BaseModel):
    target: str
    authorized: bool = False


@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/templates/index.html", encoding="utf-8") as file:
        return file.read()


@app.get("/api/history")
def history():
    return recent()


@app.post("/api/scan")
async def scan(request: ScanRequest):
    if not request.authorized:
        raise HTTPException(403, "Confirm ownership or explicit authorization.")
    try:
        result = await Scanner().scan(request.target)
        save(result)
        result["report_files"] = write_reports(result)
        return result
    except ValueError as error:
        raise HTTPException(400, str(error))
    except Exception as error:
        raise HTTPException(500, str(error)[:250])
