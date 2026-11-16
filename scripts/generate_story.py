
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

api_key = os.environ["GEMINI_API_KEY"]

prompt = """
You are the lead storyteller for Naija Story Vault,
a Nigerian storytelling YouTube channel.

Write an original, captivating Nigerian family drama titled:

THE MAID WHO INHERITED EVERYTHING

Characters:
- Ada: a young, hardworking maid.
- Oga Emeka: a wealthy businessman.
- Ife: his curious 10-year-old daughter.
- Mama Nkechi: a sharp-eyed older woman.

Style:
- Simple English mixed naturally with Nigerian Pidgin.
- Authentic Nigerian names, settings and dialogue.
- Emotional, suspenseful and entertaining.
- Strong opening hook.
- Meaningful character development.
- Unexpected but believable twist.
- A satisfying ending with a life lesson.

Write approximately 900 words.
Do not copy existing stories.
Use clear scene headings and dialogue.
Return only the complete story in Markdown.
"""

url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.8-flash:generateContent"
)

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }],
    "generationConfig": {
        "temperature": 0.9,
        "maxOutputTokens": 5000
    }
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    story = result["candidates"][0]["content"]["parts"][0]["text"]

    output = Path("stories")
    output.mkdir(exist_ok=True)

    filename = (
        "the-maid-who-inherited-everything-"
        + datetime.now().strftime("%Y%m%d")
        + ".md"
    )

    (output / filename).write_text(story, encoding="utf-8")

    print(f"Story successfully created: {filename}")

except urllib.error.HTTPError as error:
    print("Gemini API error:", error.code)
    print(error.read().decode("utf-8"))
    raise
