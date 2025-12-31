import os
from groq import Groq
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "4096"))

    def chat_completion(self, messages, temperature=None, max_tokens=None, stream=False):
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temp,
            max_completion_tokens=max_tok,
            top_p=1.0, # Default
            stream=stream,
            stop=None
        )

        if stream:
            return completion
        else:
            return completion.choices[0].message.content

    def chat_completion_stream(self, messages, temperature=None, max_tokens=None):
        completion = self.chat_completion(messages, temperature, max_tokens, stream=True)
        full_response = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_response += content
        return full_response
