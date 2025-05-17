import os

from fastapi import Request
from fastapi.responses import HTMLResponse
from pyinstrument import Profiler
from urllib.parse import quote
from datetime import datetime

from core import PROFILE_DIR


async def profile_request(request: Request, call_next):
    profiling = request.query_params.get("profile", True)

    if profiling:
        os.makedirs(PROFILE_DIR, exist_ok=True)
        profiler = Profiler()
        profiler.start()
        response = await call_next(request)
        profiler.stop()

        method = request.method
        path = request.url.path.strip("/").replace("/", "_") or "root"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        safe_name = quote(f"{method}_{path}_{timestamp}.html", safe="")

        file_path = os.path.join(PROFILE_DIR, safe_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(profiler.output_html())

        return HTMLResponse(content=profiler.output_html())

    else:
        return await call_next(request)
