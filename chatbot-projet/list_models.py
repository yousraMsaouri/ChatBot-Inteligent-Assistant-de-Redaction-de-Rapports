# list_models.py
import google.generativeai as genai
import os

# Configure ta clé API (depuis .env ou directement)
genai.configure(api_key="AIzaSyBBghb7GhLUXrxn6-NtE-P9AdnOV4IQTPg")

print("🔍 Liste des modèles Gemini disponibles :\n")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"✅ {m.name}")
        print(f"   Version: {m.version}")
        print(f"   Affichage: {m.display_name}\n")