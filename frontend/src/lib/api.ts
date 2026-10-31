export const API_BASE = (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
export type ChatMessage = { role: "user" | "assistant"; content: string };
export async function postJSON<T>(path: string, body: unknown): Promise<T> {
  let response: Response;
  try { response = await fetch(`${API_BASE}${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }); }
  catch { throw new Error("Could not reach Stillwell's API. Make sure the backend is running."); }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status}).`);
  return data as T;
}
