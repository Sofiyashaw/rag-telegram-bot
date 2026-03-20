import requests
from config import OLLAMA_URL, MODEL_NAME
from utils.logger import log

class Generator:
    def generate(self, query, context):
        try:
            prompt = f"""
            You are a helpful assistant.

            Answer ONLY using the context.
            If answer not present, say "I don't know".
            Keep answer short and clear.

            Context:
            {context}

            Question:
            {query}
            """

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": False
                }
            )

            result = response.json().get("response", "No response")
            log("Generated response")

            return result

        except Exception as e:
            return f"Error: {str(e)}"

    def summarize(self, text):
        prompt = f"Summarize this in 2-3 lines:\n{text}"

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json().get("response", "No summary")