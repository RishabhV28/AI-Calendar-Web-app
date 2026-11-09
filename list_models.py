from openai import OpenAI
from app.config import settings

client=OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
for m in client.models.list().data:
    print(m.id)

