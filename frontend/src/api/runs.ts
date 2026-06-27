import type { BusinessConfiguration, RunRequest, RunResponse, StreamEvent } from "@/types/api";

const API_BASE = "/api/v1";
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

async function parseSSEStream(
  response: Response,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<boolean> {
  const reader = response.body?.getReader();
  if (!reader) throw new Error("No response stream");

  const decoder = new TextDecoder();
  let buffer = "";
  let receivedAny = false;

  while (true) {
    if (signal?.aborted) throw new DOMException("Aborted", "AbortError");

    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      const dataLine = part.split("\n").find((line) => line.startsWith("data: "));
      if (!dataLine) continue;

      const payload = JSON.parse(dataLine.slice(6)) as StreamEvent;
      receivedAny = true;
      onEvent(payload);
    }
  }

  return receivedAny;
}

async function streamRunOnce(
  request: RunRequest,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${API_BASE}/runs/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Stream failed (${response.status})`);
  }

  await parseSSEStream(response, onEvent, signal);
}

/** Stream a single LangGraph run via SSE with automatic retry on initial connection failure. */
export async function streamRun(
  request: RunRequest,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  let receivedAny = false;
  let wrappedOnEvent = (event: StreamEvent) => {
    receivedAny = true;
    onEvent(event);
  };

  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    try {
      await streamRunOnce(request, wrappedOnEvent, signal);
      return;
    } catch (err) {
      if (signal?.aborted) throw err;
      // Only retry if no events were received yet (avoid duplicate runs)
      if (receivedAny) throw err;
      if (attempt === MAX_RETRIES - 1) throw err;
      await new Promise((r) => setTimeout(r, RETRY_DELAY_MS * (attempt + 1)));
    }
  }
}

export async function createRun(request: RunRequest): Promise<RunResponse> {
  const response = await fetch(`${API_BASE}/runs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Run failed (${response.status})`);
  }

  return response.json() as Promise<RunResponse>;
}

export type { BusinessConfiguration, RunRequest, RunResponse, StreamEvent };
