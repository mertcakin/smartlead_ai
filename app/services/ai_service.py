import requests

from config import Config


class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-20b"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def yanit_uret(self, mesaj, gecmis=None):

        if not self.api_key:
            return "Şu anda yapay zekâ hizmeti kullanılamıyor."

        if gecmis is None:
            gecmis = []

        messages = [
            {
                "role": "system",
                "content": Config.BUSINESS_CONTEXT
            }
        ]

        messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            raise AIServiceError(
                f"Yapay zekâ servisine bağlanılamadı: {e}"
            )


ai_service = AIService()