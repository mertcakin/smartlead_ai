import requests

from config import Config


# Yapay zekâ servisiyle ilgili oluşabilecek hataları yönetmek için özel hata sınıfı oluşturdum.
class AIServiceError(Exception):
    pass


class AIService:

    def __init__(self):
        # API anahtarını ve kullanılacak yapay zekâ modelini tanımladım.
        self.api_key = Config.GROQ_API_KEY
        self.model = "openai/gpt-oss-20b"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def yanit_uret(self, mesaj, gecmis=None):

        # API anahtarı yoksa kullanıcıya uygun bir hata mesajı döndürdüm.
        if not self.api_key:
            return "Şu anda yapay zekâ hizmeti kullanılamıyor."

        if gecmis is None:
            gecmis = []

        # Yapay zekâya gönderilecek sistem talimatlarını oluşturdum.
        messages = [
            {
                "role": "system",
                "content": Config.BUSINESS_CONTEXT
            }
        ]

        # Önceki konuşmaları yapay zekâya göndererek konuşma geçmişini korudum.
        messages.extend(gecmis)

        # Kullanıcının yeni mesajını konuşmaya ekledim.
        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            # Kullanıcı mesajını Groq API'ye göndererek yapay zekâ yanıtı aldım.
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

            # API'den gelen hata durumlarını kontrol ettim.
            response.raise_for_status()

            data = response.json()

            # API yanıtından yapay zekânın oluşturduğu metni aldım.
            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            # API bağlantı hatalarını özel hata sınıfına aktararak yönettim.
            raise AIServiceError(
                f"Yapay zekâ servisine bağlanılamadı: {e}"
            )


# Uygulamada kullanılacak AIService nesnesini oluşturdum.
ai_service = AIService()