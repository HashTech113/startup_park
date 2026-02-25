from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.services.store import get_job_state, load_analytics_records, resolve_processed_video_path


router = APIRouter(prefix="/api")


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = get_job_state(job_id)
    if not job:
        records = load_analytics_records()
        record = next((r for r in records if r.get("id") == job_id), None)
        if not record:
            raise HTTPException(status_code=404, detail="Job not found.")

        job = {
            "job_id": job_id,
            "record_id": job_id,
            "video_name": record.get("video_name", "unknown"),
            "status": record.get("status", "failed"),
            "progress": 100 if record.get("status") == "completed" else 0,
            "total_person_count": int(record.get("person_count", 0)),
            "processed_video": resolve_processed_video_path(record),
            "error": record.get("details", {}).get("error"),
            "updated_at": datetime.utcnow().isoformat(),
        }

    return JSONResponse({"success": True, "message": "Job status fetched successfully", "data": job})
