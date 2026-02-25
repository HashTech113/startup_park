from datetime import datetime
import os

from app.core.config import FRAME_STRIDE, OUTPUT_DIR
from app.services.store import set_job_state, update_video_record
from src.person_count.count import process_video


def process_video_job(job_id, record_id, safe_name, input_path):
    set_job_state(
        job_id,
        record_id=record_id,
        video_name=safe_name,
        status="processing",
        progress=0,
        frame_stride=FRAME_STRIDE,
        started_at=datetime.utcnow().isoformat(),
    )

    def on_progress(progress, processed_frames, total_frames):
        set_job_state(
            job_id,
            status="processing",
            progress=progress,
            processed_frames=processed_frames,
            total_frames=total_frames,
        )

    try:
        output_path, total_count, details = process_video(
            input_path,
            str(OUTPUT_DIR),
            frame_stride=FRAME_STRIDE,
            progress_callback=on_progress,
        )
        update_video_record(
            record_id,
            person_count=total_count,
            status="completed",
            output_path=output_path,
            details=details,
            completed_at=datetime.utcnow().isoformat(),
        )
        set_job_state(
            job_id,
            status="completed",
            progress=100,
            total_person_count=total_count,
            processed_video=f"/outputs/{os.path.basename(output_path)}",
            completed_at=datetime.utcnow().isoformat(),
        )
    except ValueError as exc:
        update_video_record(
            record_id,
            person_count=0,
            status="failed",
            details={"error": str(exc)},
            completed_at=datetime.utcnow().isoformat(),
        )
        set_job_state(
            job_id,
            status="failed",
            error=str(exc),
            completed_at=datetime.utcnow().isoformat(),
        )
    except Exception:
        update_video_record(
            record_id,
            person_count=0,
            status="failed",
            details={"error": "Video processing failed."},
            completed_at=datetime.utcnow().isoformat(),
        )
        set_job_state(
            job_id,
            status="failed",
            error="Video processing failed.",
            completed_at=datetime.utcnow().isoformat(),
        )
