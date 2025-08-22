import os
from typing import Optional
import httpx

# OLLAMA API configuration
# OLLAMA_HOST = (os.getenv("OLLAMA_HOST") or "http://ollama:11434").rstrip("/")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

# System hints for message generation
SYSTEM_HINTS = {
    "intro":    "Write a concise friendly introduction and value proposition.",
    "followup": "Write a polite follow-up referencing a prior note.",
    "meeting":  "Request a short 15-minute meeting with a clear CTA.",
}

def _build_prompt(message_type: str, context: str, prompt_hint: Optional[str]) -> str:
    style = SYSTEM_HINTS.get(message_type, "Write a brief professional note.")
    user_hint = f" Additional context: {prompt_hint}" if prompt_hint else ""
    return f"{style}\nContext: {context}{user_hint}\nKeep it under 120 words."

# Generate a message using the OLLAMA API (tries /api/chat, falls back to /api/generate)
async def generate_message_from_ollama(
    message_type: str,
    context: str,
    prompt_hint: Optional[str] = None,
) -> str:
    prompt = _build_prompt(message_type, context, prompt_hint)

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as c:
        try:
            # First try: /api/chat
            chat_payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that writes short, professional, actionable messages.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            }
            chat_url = f"{OLLAMA_HOST}/api/chat"
            resp = await c.post(chat_url, json=chat_payload)
            if resp.status_code == 404:
                raise httpx.HTTPStatusError("Not Found", request=resp.request, response=resp)
            resp.raise_for_status()
            data = resp.json()
            text = (data.get("message") or {}).get("content", "")
            if isinstance(text, str) and text.strip():
                return text.strip()
        except httpx.HTTPStatusError as e:
            # Fall through to /api/generate only on 404
            if getattr(e, "response", None) is None or e.response.status_code != 404:
                return f"[Ollama error] {str(e)}"
        except Exception as e:
            return f"[Ollama exception] {str(e)}"

        # Fallback: /api/generate
        try:
            gen_payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
            gen_url = f"{OLLAMA_HOST}/api/generate"
            resp = await c.post(gen_url, json=gen_payload)
            resp.raise_for_status()
            data = resp.json()
            text = data.get("response", "")
            if not isinstance(text, str) or not text.strip():
                return f"[Unexpected Ollama response] {data}"
            return text.strip()
        except Exception as e:
            return f"[Ollama generate error] {str(e)}"
