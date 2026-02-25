import { API_BASE_URL } from "@/config/env";
import { requestBlob, requestJson, toBackendAssetUrl } from "@/lib/http";

interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

interface UploadResponse {
  message: string;
  job_id: string;
  status: "processing";
  frame_stride: number;
}

interface UploadJobStatus {
  job_id: string;
  record_id: string;
  video_name: string;
  status: "processing" | "completed" | "failed";
  progress: number;
  frame_stride?: number;
  processed_frames?: number;
  total_frames?: number;
  total_person_count?: number;
  processed_video?: string;
  error?: string;
  started_at?: string;
  updated_at?: string;
  completed_at?: string;
}

interface AnalyticsData {
  total_videos: number;
  total_persons: number;
  total_processing_time_seconds?: number;
  active_cameras: number;
  todays_detections: number;
  hourly_analytics: { hour: string; detections: number; uploads: number }[];
  person_count_per_video: { video: string; count: number }[];
  recent_uploads: {
    id: string;
    videoName: string;
    uploadDate: string;
    personCount: number;
    status: "completed" | "processing" | "failed";
    processedVideo?: string;
    processingTimeSeconds?: number;
  }[];
}

interface VideoDetails {
  id: string;
  videoName: string;
  uploadDate: string;
  personCount: number;
  status: "completed" | "processing" | "failed";
  processedVideo: string;
  details: {
    fps?: number;
    total_frames?: number;
    duration_seconds?: number;
    peak_count?: number;
    counts_per_second?: { second: number; count: number }[];
  };
}

async function apiRequest<T>(endpoint: string, options?: RequestInit): Promise<ApiResponse<T>> {
  return requestJson<ApiResponse<T>>(endpoint, options);
}

export async function uploadVideo(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  return requestJson<UploadResponse>("/upload-video", {
    method: "POST",
    body: formData,
  });
}

export async function getUploadJobStatus(jobId: string): Promise<UploadJobStatus> {
  const response = await apiRequest<UploadJobStatus>(`/api/jobs/${jobId}`);
  const data = response.data;
  if (data?.processed_video) {
    data.processed_video = toBackendAssetUrl(data.processed_video);
  }
  return data;
}

export async function getAnalytics(): Promise<ApiResponse<AnalyticsData>> {
  return apiRequest<AnalyticsData>("/api/analytics");
}

export async function downloadReport(): Promise<Blob> {
  return requestBlob("/api/analytics/report", { method: "GET" });
}

export async function getVideoDetails(videoId: string): Promise<ApiResponse<VideoDetails>> {
  return apiRequest<VideoDetails>(`/api/videos/${videoId}`);
}

export async function deleteVideo(videoId: string): Promise<void> {
  await requestJson<{ success: boolean; message: string }>(`/api/videos/${videoId}`, {
    method: "DELETE",
  });
}

export { API_BASE_URL };
export type { ApiResponse, UploadResponse, UploadJobStatus, AnalyticsData, VideoDetails };
