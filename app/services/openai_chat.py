from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def get_response(message: str, topic: str = "General", context: list = None) -> str:
    messages = [{"role": "system", "content": f"You are an AI assistant that helps users about {topic}."}]
    
    # Add most recent messages first (reverse order)
    if context:
        for entry in reversed(context):
            messages.append({"role": "user", "content": entry["message"]})
            messages.append({"role": "assistant", "content": entry["response"]})
    
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

