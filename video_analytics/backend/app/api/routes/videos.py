from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os

from app.services.store import (
    load_analytics_records,
    pop_job_state,
    records_lock,
    resolve_processed_video_path,
    save_analytics_records,
)


router = APIRouter(prefix="/api")


@router.get("/videos/{video_id}")
async def get_video_details(video_id: str):
    records = load_analytics_records()
    record = next((r for r in records if r.get("id") == video_id), None)
    if not record:
        raise HTTPException(status_code=404, detail="Video record not found.")

    processed_video = resolve_processed_video_path(record)

    created_at = record.get("created_at", "")
    upload_date = created_at.split("T")[0] if "T" in created_at else created_at

    return JSONResponse(
        {
            "success": True,
            "message": "Video details fetched successfully",
            "data": {
                "id": record.get("id", ""),
                "videoName": record.get("video_name", "unknown"),
                "uploadDate": upload_date,
                "personCount": int(record.get("person_count", 0)),
                "status": record.get("status", "failed"),
                "processedVideo": processed_video,
                "details": record.get("details", {}),
            },
        }
    )


@router.delete("/videos/{video_id}")
async def delete_video(video_id: str):
    with records_lock:
        records = load_analytics_records()
        record_index = next((idx for idx, r in enumerate(records) if r.get("id") == video_id), None)
        if record_index is None:
            raise HTTPException(status_code=404, detail="Video record not found.")

        record = records[record_index]
        input_path = record.get("input_path", "")
        output_path = record.get("output_path", "")

        if input_path and os.path.exists(input_path):
            os.remove(input_path)

        if output_path and os.path.exists(output_path):
            os.remove(output_path)

        records.pop(record_index)
        save_analytics_records(records)

    pop_job_state(video_id)

    return JSONResponse({"success": True, "message": "Video deleted permanently"})
