import json
from openai import OpenAI
from app.config import settings
from app.chat.tools import TOOLS
from app.chat.executor import run_tool, now_local

client= OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)


def chat(db, user, message: str)->str:
    system=(
        f"You are a scheduling assistant. Current date and time:{now_local(): %A,%d %B %Y, %H:%M} (India)."
        "Use the tools to read or change the calendar. Never claim an event exists or was created"
        "unless a tool result confirms it. If a tool reports a conflict, tell the user and ask what to do."
    
    )
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
        print(f"LLM error:{e}")
        return " The AI service had a problem. Try again in a moment"