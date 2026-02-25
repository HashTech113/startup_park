from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response

from app.services.store import build_analytics_payload


router = APIRouter(prefix="/api")


@router.get("/analytics")
async def get_analytics():
    payload = build_analytics_payload()
    return JSONResponse({"success": True, "message": "Analytics fetched successfully", "data": payload})


@router.get("/analytics/report")
async def download_analytics_report():
    payload = build_analytics_payload()
    rows = ["video_name,upload_date,person_count,status"]
    for item in payload["recent_uploads"]:
        rows.append(f'{item["videoName"]},{item["uploadDate"]},{item["personCount"]},{item["status"]}')

    csv_data = "\n".join(rows) + "\n"
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="analytics_report.csv"'},
    )
