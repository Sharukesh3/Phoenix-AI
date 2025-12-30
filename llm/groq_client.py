from groq import Groq
import config

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        
    def chat_completion(self, messages, temperature=None, max_tokens=None, stream=False):
        temp = temperature if temperature is not None else config.GROQ_TEMPERATURE
        max_tok = max_tokens if max_tokens is not None else config.GROQ_MAX_TOKENS
        
        completion = self.client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=messages,
            temperature=temp,
            max_completion_tokens=max_tok,
            top_p=config.GROQ_TOP_P,
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
