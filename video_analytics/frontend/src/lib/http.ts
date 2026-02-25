import { API_BASE_URL } from "@/config/env";

function buildApiUrl(endpoint: string): string {
  if (/^https?:\/\//i.test(endpoint)) {
    return endpoint;
  }

  const normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

  if (/^https?:\/\//i.test(API_BASE_URL)) {
    return `${API_BASE_URL}${normalizedEndpoint}`;
  }

  // Supports proxy-style bases such as /api in production.
  return `${API_BASE_URL}${normalizedEndpoint}`;
}

async function parseError(response: Response): Promise<Error> {
  try {
    const payload = await response.json();
    const message = payload?.detail || payload?.message;
    if (typeof message === "string" && message.trim()) {
      return new Error(message);
    }
  } catch {
    // Ignore parse errors and fall through to generic message.
  }

  return new Error(`API Error: ${response.status} ${response.statusText}`);
}

export async function requestJson<T>(endpoint: string, init?: RequestInit): Promise<T> {
  const response = await fetch(buildApiUrl(endpoint), init);
  if (!response.ok) {
    throw await parseError(response);
  }
  return response.json() as Promise<T>;
}

export async function requestBlob(endpoint: string, init?: RequestInit): Promise<Blob> {
  const response = await fetch(buildApiUrl(endpoint), init);
  if (!response.ok) {
    throw await parseError(response);
  }
  return response.blob();
}

export function toBackendAssetUrl(path: string): string {
  if (!path || /^https?:\/\//i.test(path)) {
    return path;
  }

  if (/^https?:\/\//i.test(API_BASE_URL)) {
    return new URL(path, API_BASE_URL).toString();
  }

  if (typeof window !== "undefined") {
    return new URL(path, window.location.origin).toString();
  }

  return path;
}
