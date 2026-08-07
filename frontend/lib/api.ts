const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type Video = {
  id: number;
  url: string;
  video_id: string;
  title: string;
  thumbnail_url: string;
  created_at: string;
};

export class ApiError extends Error {}

async function parseErrorMessage(response: Response): Promise<string> {
  try {
    const data = await response.json();
    return data.detail ?? response.statusText;
  } catch {
    return response.statusText;
  }
}

export async function getVideos(): Promise<Video[]> {
  const response = await fetch(`${API_BASE_URL}/videos`, { cache: "no-store" });
  if (!response.ok) {
    throw new ApiError(await parseErrorMessage(response));
  }
  return response.json();
}

export async function createVideo(url: string): Promise<Video> {
  const response = await fetch(`${API_BASE_URL}/videos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!response.ok) {
    throw new ApiError(await parseErrorMessage(response));
  }
  return response.json();
}
