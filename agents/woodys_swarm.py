import anthropic
import os
from datetime import date

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

TODAY = str(date.today())
BUSINESS = "Woody's Tree Xperts"
LOCATION = "North Carolina"
SERVICE = "professional tree removal, trimming, and storm damage cleanup"


def run_agent(role: str, task: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are {role}.\n\n"
                    f"Business: {BUSINESS} — {SERVICE} in {LOCATION}.\n"
                    f"Today's date: {TODAY}\n\n"
                    f"{task}"
                )
            }
        ]
    )
    return message.content[0].text


# --- Agent 1: Social Media Specialist ---
print("Running social media agent...")
social_media = run_agent(
    role="a professional social media copywriter specializing in home services",
    task="""Write platform-specific social media posts for today. Use each platform's native format and tone.

INSTAGRAM: A visually descriptive caption (150-200 words) with a strong first-line hook + 10 relevant hashtags.

FACEBOOK: A community-focused post (200-250 words) with a local feel and a clear call to action.

TIKTOK: A video script structured as:
  [HOOK] — first 3 seconds, must stop the scroll
  [CONTENT] — 30-45 seconds of value
  [CTA] — clear next step

LINKEDIN: A professional post (150-200 words) on the value and safety of hiring certified arborists. Speak to homeowners and property managers.

X/TWITTER: A punchy tweet under 280 characters with 2-3 hashtags.

Pick one theme for today and apply it consistently across all platforms. Themes to rotate: storm damage urgency, property value & curb appeal, safety risks of DIY tree work, seasonal maintenance reminders."""
)

# --- Agent 2: Sales Pitch Specialist ---
print("Running sales pitch agent...")
sales_pitch = run_agent(
    role="a top-performing field sales trainer for home service companies",
    task="""Write two sales scripts:

DOOR KNOCK SCRIPT — A natural, confident cold-approach for homeowners. Include:
  - Opening line (non-pushy, conversational)
  - One-sentence value proposition
  - Transition to asking for a quote or walkthrough
  - One recovery line if they say "not interested"

PHONE PITCH SCRIPT — A 60-second script for inbound or outbound calls. Include:
  - Greeting and company intro
  - One qualifying question
  - Core pitch (what makes Woody's the right choice)
  - Closing line that asks for the appointment"""
)

# --- Agent 3: Email Templates ---
print("Running email agent...")
email_copy = run_agent(
    role="a direct-response email copywriter for local home service businesses",
    task="""Write two email templates:

COLD OUTREACH EMAIL
  Subject line: (write one strong option)
  Body: 150 words max. Target homeowners who may need tree work but haven't reached out yet. Local, personal tone.

FOLLOW-UP EMAIL (sent 24-48 hours after a quote)
  Subject line: (write one strong option)
  Body: 100 words max. Acknowledge the quote, create mild urgency, make it easy to say yes. No pressure tactics."""
)

# --- Agent 4: Objection Handler ---
print("Running objection handler agent...")
objections = run_agent(
    role="a sales coach who specializes in closing home service deals face-to-face",
    task="""Write responses to the top 5 objections homeowners give about tree services.

For each objection:
  - Write the objection exactly as the homeowner would say it (in quotes)
  - Write a 2-3 sentence response that is empathetic, reframes the concern, and moves toward a close

Cover these objections:
  1. Price ("That's more than I expected / too expensive")
  2. Timing ("I'm not ready right now / maybe later")
  3. DIY ("I think my neighbor / son-in-law can handle it")
  4. Competition ("I'm getting a few quotes first")
  5. Approval ("I need to talk to my spouse / landlord first")"""
)

# --- Agent 5: Weekly Content Calendar ---
print("Running content calendar agent...")
calendar = run_agent(
    role="a social media strategist for local home service businesses",
    task=f"""Create a 7-day social media content calendar starting from {TODAY}.

For each day provide:
  - Day name + date
  - Platform (rotate through Instagram, Facebook, TikTok, LinkedIn, X/Twitter — use each at least once)
  - Content theme in one sentence
  - Best time to post (Eastern Time)
  - Content format (video, photo, carousel, text post, reel, story)

Vary the themes across the week: mix storm damage, before/after, customer testimonial, educational tip, promotional offer, seasonal reminder, and trust/credibility content. Format as a clean table."""
)

# --- Assemble final document ---
print("Assembling output...")
os.makedirs("output", exist_ok=True)
filename = f"output/woodys_swarm_{date.today()}.md"

sections = [
    ("Social Media Posts", social_media),
    ("Sales Pitch Scripts", sales_pitch),
    ("Email Templates", email_copy),
    ("Objection Responses", objections),
    ("Weekly Content Calendar", calendar),
]

with open(filename, "w") as f:
    f.write(f"# Woody's Tree Xperts — Full Marketing Kit — {TODAY}\n\n")
    for title, content in sections:
        f.write(f"---\n\n## {title}\n\n")
        f.write(content.strip())
        f.write("\n\n")

print(f"Swarm output generated successfully → {filename}")
