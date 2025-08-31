from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess
import os

app = FastAPI()

DOWNLOAD_DIR = "/tmp"  # Temporary storage in Railway container

@app.get("/download")
def download(url: str = Query(...)):
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    try:
        result = subprocess.run(
            ["yt-dlp", url, "-o", output_template],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return JSONResponse(content={"status": "error", "error": result.stderr})
        
        # Get the downloaded filename
        filename_line = [line for line in result.stdout.splitlines() if "[download] Destination" in line]
        filename = filename_line[-1].split("Destination: ")[1] if filename_line else "unknown"
        
        return JSONResponse(content={"status": "success", "file": filename})
    except Exception as e:
        return JSONResponse(content={"status": "error", "error": str(e)})
