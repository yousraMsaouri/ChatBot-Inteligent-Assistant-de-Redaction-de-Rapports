# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime

# Imports locaux
import backend.gemini_handler as gemini_handler
from backend.database import SessionLocal, UserReport, UserMessage
from backend.tasks import send_reminder_email, schedule_call_if_not_downloaded
from backend.pdf_generator import generate_pdf_report

app = FastAPI(title="Chatbot Intelligent pour Rapports")

# Autoriser le frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ReportRequest(BaseModel):
    user_id: str
    report_name: str

# Servir les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/chat")
async def chat(request: ChatRequest):
    db = next(get_db())

    # Sauvegarder le message utilisateur
    user_message = UserMessage(user_id=request.user_id, message=request.message, sender="user")
    db.add(user_message)
    db.commit()

    # Récupérer l'historique
    user_reports = db.query(UserReport).filter(UserReport.user_id == request.user_id).all()
    last_report_name = user_reports[-1].report_name if user_reports else "Aucun"

    # === 🔥 DÉTECTION FLEXIBLE DE CRÉATION DE RAPPORT ===
    message_lower = request.message.lower().strip()

    # Mots-clés pour créer un rapport
    if any(keyword in message_lower for keyword in [
        "crée un nouveau rapport",
        "créer un nouveau rapport",
        "génère un nouveau rapport",
        "générer un nouveau rapport"
    ]):
        report_title = None

        # Extraire après "intitulé :"
        if "intitulé :" in request.message:
            try:
                report_title = request.message.split("intitulé :")[1].strip()
            except:
                pass

        # Extraire après "intitulé" (sans :)
        elif "intitulé" in message_lower:
            try:
                after_keyword = request.message.split("intitulé")[1].strip()
                if after_keyword.startswith(("l ", "la ", "le ", "les ")):
                    parts = after_keyword.split(maxsplit=1)
                    report_title = parts[1] if len(parts) > 1 else parts[0]
                else:
                    report_title = after_keyword
            except:
                pass

        # Extraire après "sur"
        elif "sur " in message_lower:
            try:
                report_title = request.message.split("sur ")[1].strip()
            except:
                pass

        # Extraire après "à propos de"
        elif "à propos de " in message_lower:
            try:
                report_title = request.message.split("à propos de ")[1].strip()
            except:
                pass

        # Nettoyer le titre
        if report_title:
            report_title = report_title.split("avec la structure habituelle")[0].strip()
            report_title = report_title.split("en utilisant la structure habituelle")[0].strip()
            report_title = report_title.title()

            # Générer contenu avec Gemini
            prompt = f"""
            Tu es un expert en rédaction. Rédige un rapport complet intitulé '{report_title}',
            avec une introduction, une analyse des risques, une méthodologie, et une conclusion.
            Style professionnel, clair, concis.
            """
            try:
                gemini_response = gemini_handler.generate_response(prompt)
            except Exception as e:
                gemini_response = f"Erreur Gemini : {str(e)}"

            # Créer entrée en base
            new_report = UserReport(
                user_id=request.user_id,
                report_name=report_title,
                plan_json='{"sections": ["introduction", "analyse", "conclusion"]}',
                file_path="",
                downloaded=False
            )
            db.add(new_report)
            db.commit()
            db.refresh(new_report)

            # Générer PDF
            pdf_path = generate_pdf_report(
                user_id=request.user_id,
                title=report_title,
                content=gemini_response
            )
            relative_path = pdf_path.replace("static/", "/static/")
            new_report.file_path = relative_path
            db.commit()

            # Planifier email et appel
            download_link = f"http://localhost:8000{relative_path}"
            send_reminder_email.apply_async(
                (request.user_id, new_report.id, download_link),
                countdown=2
            )
            schedule_call_if_not_downloaded.apply_async(
                (request.user_id, new_report.id, download_link),
                countdown=5
            )

            # Réponse au bot
            response_text = f"✅ Rapport '{report_title}' généré avec succès ! Un email vous a été envoyé."

            bot_message = UserMessage(user_id=request.user_id, message=response_text, sender="bot")
            db.add(bot_message)
            db.commit()
            db.close()

            return {"response": response_text}

    # === 🤖 Mode conversationnel normal (RAG + historique) ===
    context = ""
    if user_reports:
        context = f"\n\nHistorique des rapports : {len(user_reports)} générés. Dernier : {last_report_name}"

    full_prompt = f"{request.message}{context}"
    try:
        response = gemini_handler.generate_response(full_prompt)
    except Exception as e:
        response = f"Désolé, une erreur est survenue avec Gemini : {str(e)}"

    # Sauvegarder la réponse du bot
    bot_message = UserMessage(user_id=request.user_id, message=response, sender="bot")
    db.add(bot_message)
    db.commit()
    db.close()

    return {"response": response}


@app.post("/generate-report")
async def generate_report(req: ReportRequest):
    db = next(get_db())

    # Créer une entrée dans la base
    new_report = UserReport(
        user_id=req.user_id,
        report_name=req.report_name,
        plan_json='{"sections": ["introduction", "développement", "conclusion"]}',
        file_path="",
        downloaded=False
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    # Générer contenu avec Gemini
    prompt = f"""
    Tu es un expert en rédaction. Rédige un rapport complet intitulé '{req.report_name}'.
    Structure : Introduction, Développement, Conclusion.
    Style : professionnel, clair, concis.
    """

    try:
        gemini_response = gemini_handler.generate_response(prompt)
    except Exception as e:
        gemini_response = "Contenu du rapport indisponible."

    # Générer PDF
    pdf_path = generate_pdf_report(
        user_id=req.user_id,
        title=req.report_name,
        content=gemini_response
    )

    # Mettre à jour le chemin dans la DB
    relative_path = pdf_path.replace("static/", "/static/")
    new_report.file_path = relative_path
    db.commit()

    # Planifier tâches différées
    download_link = f"http://localhost:8000{relative_path}"
    send_reminder_email.apply_async(
        (req.user_id, new_report.id, download_link),
        countdown=2
    )
    schedule_call_if_not_downloaded.apply_async(
        (req.user_id, new_report.id, download_link),
        countdown=5
    )

    return {
        "status": "rapport généré",
        "id": new_report.id,
        "download_link": download_link
    }