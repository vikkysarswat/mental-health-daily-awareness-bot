#!/usr/bin/env python3
"""
Mental Health Daily Awareness Bot - Main Script
This script orchestrates the daily workflow:
1. Fetch trending mental health topic
2. Generate script/content based on the topic
3. Create video with the generated content
4. Post the video to Instagram

NOTE: This file contains placeholders and commented steps for API integrations.
Fill in API keys in your environment (.env) and replace the TODO sections.
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ------------------------------
# Configuration placeholders
# ------------------------------
# Trending topic sources (choose one or implement both)
CHATGPT_API_KEY = os.getenv("OPENAI_API_KEY")        # For OpenAI Chat Completions / Responses API
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")  # For Perplexity API (pplx)

# Script generation (OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # e.g., gpt-4o, gpt-4o-mini, o4-mini

# Video creation (choose any provider)
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
FLEXCLIP_API_KEY = os.getenv("FLEXCLIP_API_KEY")

# Instagram posting
INSTAGRAM_USERNAME = os.getenv("IG_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("IG_PASSWORD")

# Output paths
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
VIDEO_PATH = os.path.join(OUTPUT_DIR, "daily_mental_health.mp4")
SCRIPT_PATH = os.path.join(OUTPUT_DIR, "script.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# 1) Trending Topic Fetch
# ------------------------------
def fetch_trending_topic(source: str = "chatgpt", region: Optional[str] = None) -> str:
    """
    Fetch a trending mental health topic using either ChatGPT (OpenAI) or Perplexity APIs.

    Args:
        source: "chatgpt" or "perplexity"
        region: optional region/country hint for localized trends

    Returns:
        topic string

    Steps for ChatGPT (OpenAI):
    - Install: pip install openai
    - Set OPENAI_API_KEY in .env
    - Use the Responses API (preferred) or Chat Completions to ask for a single, concise topic

    Steps for Perplexity:
    - Sign up and get API key
    - Call https://api.perplexity.ai/chat/completions with a short prompt asking for a single trending topic
    """
    prompt = (
        "You are a trend researcher. Provide ONE concise trending mental health topic "
        + (f"relevant to {region}. " if region else "")
        + "Return ONLY the topic title without extra sentences."
    )

    if source == "chatgpt":
        if not CHATGPT_API_KEY:
            raise RuntimeError("Missing OPENAI_API_KEY for ChatGPT trending topic fetch.")
        # Placeholder: OpenAI request (Responses API)
        # from openai import OpenAI
        # client = OpenAI(api_key=CHATGPT_API_KEY)
        # resp = client.responses.create(
        #     model="gpt-4o-mini",
        #     input=[{"role": "user", "content": prompt}],
        # )
        # topic = resp.output_text.strip()
        topic = "Mindful breathing for anxiety management"  # TODO: Replace with actual API response
        return topic

    elif source == "perplexity":
        if not PERPLEXITY_API_KEY:
            raise RuntimeError("Missing PERPLEXITY_API_KEY for Perplexity trending topic fetch.")
        # Placeholder: Perplexity API request
        # import requests
        # url = "https://api.perplexity.ai/chat/completions"
        # headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}", "Content-Type": "application/json"}
        # payload = {
        #   "model": "sonar",
        #   "messages": [{"role": "user", "content": prompt}],
        #   "max_tokens": 64,
        #   "temperature": 0.7
        # }
        # r = requests.post(url, headers=headers, json=payload, timeout=30)
        # r.raise_for_status()
        # topic = r.json()["choices"][0]["message"]["content"].strip()
        topic = "Journaling prompts to combat seasonal affective disorder"  # TODO: Replace with API response
        return topic

    else:
        raise ValueError("source must be 'chatgpt' or 'perplexity'")

# ------------------------------
# 2) Script Generation (OpenAI)
# ------------------------------
def generate_script(topic: str) -> str:
    """
    Generate a short, engaging video narration script for the given topic using OpenAI.

    Returns:
        The full script text.

    Steps:
    - Install: pip install openai
    - Set OPENAI_API_KEY in .env
    - Use a concise system/user prompt to produce a 45-60s script (115-150 words)
    - Save to SCRIPT_PATH
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("Missing OPENAI_API_KEY for script generation.")

    system_prompt = (
        "You are a compassionate mental health advocate creating a 45-60 second "
        "Instagram Reel script. Keep tone empathetic, practical, stigma-free. Include: "
        "1) a hook, 2) three actionable tips, 3) brief encouragement, 4) CTA to seek professional help when needed. "
        "Avoid medical claims."
    )
    user_prompt = f"Topic: {topic}. Write the script as short spoken lines."

    # Placeholder: OpenAI request (Responses API or Chat Completions)
    # from openai import OpenAI
    # client = OpenAI(api_key=OPENAI_API_KEY)
    # resp = client.responses.create(
    #     model=OPENAI_MODEL,
    #     input=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt},
    #     ],
    # )
    # script = resp.output_text.strip()
    script = (
        f"[Hook] Let’s talk about {topic}—in under a minute.\n"
        "Tip 1: Start with one deep breath: in for 4, out for 6.\n"
        "Tip 2: Name what you feel—labeling lowers intensity.\n"
        "Tip 3: Try a 2-minute body scan to release tension.\n"
        "You’re not alone—progress is messy and still progress.\n"
        "If you’re struggling, consider reaching out to a licensed professional.\n"
        "Follow for more daily mental health support."
    )

    with open(SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(script)

    return script

# ------------------------------
# 3) Video Creation (HeyGen or FlexClip)
# ------------------------------

def create_video_from_script(script: str, provider: str = "heygen") -> str:
    """
    Create a short video using the generated script via HeyGen or FlexClip API.

    Returns:
        Path to the created video file (or remote URL if you keep it in the cloud).

    HeyGen (placeholder):
    - Docs: https://docs.heygen.com/
    - Typical flow: create a talking avatar video with voiceover
    - Endpoint example: POST /v1/video.generate (subject to provider changes)

    FlexClip (placeholder):
    - Docs: https://api.flexclip.com/ (example placeholder)
    - Typical flow: create a text-to-speech video or template-based video

    Note: Below are pseudo-requests. Replace with real endpoints/fields.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if provider == "heygen":
        if not HEYGEN_API_KEY:
            raise RuntimeError("Missing HEYGEN_API_KEY for video creation.")
        # Placeholder pseudo-code for HeyGen
        # import requests, time
        # headers = {"Authorization": f"Bearer {HEYGEN_API_KEY}", "Content-Type": "application/json"}
        # payload = {
        #   "avatar_id": "your_avatar_id",
        #   "voice_id": "your_voice_id",
        #   "script": script,
        #   "background": "#000000",
        #   "aspect_ratio": "9:16",
        # }
        # job = requests.post("https://api.heygen.com/v1/video.generate", headers=headers, json=payload).json()
        # job_id = job["data"]["id"]
        # Poll status until completed, then download the mp4 to VIDEO_PATH
        # download_url = ...
        # with requests.get(download_url, stream=True) as r: ... save to VIDEO_PATH
        # For now, simulate a local placeholder file:
        with open(VIDEO_PATH, "wb") as f:
            f.write(b"FAKE_MP4_DATA")  # TODO: Replace with actual download
        return VIDEO_PATH

    elif provider == "flexclip":
        if not FLEXCLIP_API_KEY:
            raise RuntimeError("Missing FLEXCLIP_API_KEY for video creation.")
        # Placeholder pseudo-code for FlexClip
        # import requests, time
        # headers = {"Authorization": f"Bearer {FLEXCLIP_API_KEY}", "Content-Type": "application/json"}
        # payload = {
        #   "template_id": "your_template_id",
        #   "text_overlays": [script],
        #   "tts_voice": "en-US",
        #   "aspect_ratio": "9:16",
        # }
        # job = requests.post("https://api.flexclip.com/v1/video.create", headers=headers, json=payload).json()
        # job_id = job["data"]["id"]
        # Poll and download resulting video to VIDEO_PATH
        with open(VIDEO_PATH, "wb") as f:
            f.write(b"FAKE_MP4_DATA")  # TODO: Replace with actual download
        return VIDEO_PATH

    else:
        raise ValueError("provider must be 'heygen' or 'flexclip'")

# ------------------------------
# 4) Instagram Posting (instabot)
# ------------------------------

def post_to_instagram(video_path: str, caption: str) -> Dict[str, Any]:
    """
    Post a video to Instagram using instabot.

    Steps:
    - Install: pip install instabot
    - Important: Use at your own risk. Consider Meta Graph API for long-term stability.
    - Credentials from .env: IG_USERNAME, IG_PASSWORD

    Returns:
        A dict with status and any response info.
    """
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        raise RuntimeError("Missing IG_USERNAME/IG_PASSWORD for Instagram posting.")

    # Placeholder using instabot
    # from instabot import Bot
    # bot = Bot()
    # bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    # result = bot.upload_video(video_path, caption=caption)
    # return {"ok": bool(result), "result": result}

    # Simulate success response for scaffolding
    return {"ok": True, "result": {"message": "Simulated upload complete", "path": video_path}}

# ------------------------------
# Orchestration
# ------------------------------

def main():
    # 1) Fetch topic
    topic = fetch_trending_topic(source=os.getenv("TREND_SOURCE", "chatgpt"), region=os.getenv("TREND_REGION"))
    print(f"Topic: {topic}")

    # 2) Generate script
    script = generate_script(topic)
    print("Script generated and saved.")

    # 3) Create video
    provider = os.getenv("VIDEO_PROVIDER", "heygen")
    video_path = create_video_from_script(script, provider=provider)
    print(f"Video created at: {video_path}")

    # 4) Post to Instagram
    caption = f"Daily Mental Health: {topic}\n\nFollow for more supportive tips."
    ig_resp = post_to_instagram(video_path, caption)
    print(f"Instagram response: {ig_resp}")

if __name__ == "__main__":
    main()
