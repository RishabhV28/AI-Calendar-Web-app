import json
from openai import OpenAI
from app.config import settings
from app.chat.tools import TOOLS
from app.chat.executor import run_tool, now_local
import traceback

client= OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)


def chat(db, user, message: str)->str:
    system=(
               f"You are a scheduling assistant. Current date and time: {now_local():%A, %d %B %Y, %H:%M} (India). "
        "When the user asks to add an event, call create_event immediately. Do not ask for extra details "
        "such as company, notes, or location. If am/pm isn't given, pick the most plausible waking-hours "
        "interpretation (12:00 is noon) and mention your assumption in your reply. Default the duration to "
        "60 minutes. Only ask a question if the date or time is genuinely missing. "
        "ALWAYS fill in every required argument when calling a tool, taken from the user's message. "
        "For create_event you must pass title, date (e.g. 'tomorrow') and time (e.g. '12:00'). "
        "Never call a tool with empty arguments. "
        "Conflict checking happens automatically inside the tool, so never offer to check it separately. "
        "Never claim an event exists or was created unless a tool result confirms it. "
        "If a tool reports a conflict, tell the user and ask what to do.")
    messages=[
        {"role":"system","content": system},
        {"role":"user","content": message},
    ]
    try:
        for _ in range(5):
            resp=client.chat.completions.create(
                model=settings.LLM_MODEL, messages=messages,tools=TOOLS,
            )
            msg=resp.choices[0].message
            if not msg.tool_calls:
                return msg.content or "Sorry, I didnt get a response."
            messages.append(msg.model_dump(exclude_none=True))
            for tc in msg.tool_calls:
        
                try:
                    args=json.loads(tc.function.arguments)
                    result=run_tool(tc.function.name, args, db, user)

                except json.JSONDecodeError:
                    result= {"status": "error", 'message':"Malformed tool arguments"}
                messages.append({"role":"tool","tool_call_id":tc.id, "content": json.dumps(result)})
        return "Sorry, I got stuck on that one."
    except Exception as e:
        traceback.print_exc()
        return " The AI service had a problem. Try again in a moment"