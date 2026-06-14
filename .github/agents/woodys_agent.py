import anthropic
import os
from datetime import date

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": """You are a lead generation expert for Woody's Tree Xperts,
            a professional tree service company in North Carolina.
            
            Generate today's sales kit including:
            
            1. DOOR KNOCK SCRIPT — A confident, natural opening line 
               for approaching homeowners cold
               
            2. FOLLOW UP MESSAGE — A text/email to send after a quote
            
            3. 3 SOCIAL MEDIA POSTS — Targeting homeowners who need 
               tree removal, trimming, or storm damage cleanup
               
            4. OBJECTION RESPONSES — Top 3 objections homeowners give 
               and how to crush them
               
            Be direct, confident, and closing-focused.
            Today's date: """ + str(date.today())
        }
    ]
)

output = message.content[0].text

os.makedirs("output", exist_ok=True)
filename = f"output/woodys_{date.today()}.md"

with open(filename, "w") as f:
    f.write(f"# Woody's Daily Sales Kit — {date.today()}\n\n")
    f.write(output)

print("Woody's kit generated successfully")
