from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

GOOGLE_API_KEY = "AIzaSyAsyzfCItN0ByZ5i8vfOQuB0OhLj2Re0DE"
provider = GoogleProvider(api_key=GOOGLE_API_KEY)
model = GoogleModel("gemini-2.0-flash", provider=provider)