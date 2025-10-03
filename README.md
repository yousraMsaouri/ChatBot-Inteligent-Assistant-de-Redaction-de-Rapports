# 💬 ChatBot Intelligent - Assistant de Rédaction de Rapports

Un assistant conversationnel intelligent développé avec **Angular, FastAPI, Google Gemini, Celery et Twilio/SendGrid**, capable de :
- 🔍 Discuter avec l'utilisateur pour comprendre ses besoins
- 📄 Générer automatiquement des rapports complets via IA
- 📊 Sauvegarder l'historique des rapports en base de données
- 📧 Envoyer un email de rappel si le rapport n'est pas téléchargé
- 📞 Passer un appel vocal après un délai configurable

> ✨ Démo en direct | [Voir la démo](#) *(optionnel)*

---

## 🌐 Architecture du Projet
Frontend (Angular) ↔ Backend (FastAPI) ↔ IA (Gemini) + Tâches différées (Celery + Redis)

### Composants principaux
| Couche | Technologie |
|-------|-------------|
| Frontend | Angular 17+ |
| Backend | FastAPI (Python) |
| Base de données | SQLite (`chatbot.db`) |
| Génération de contenu | Google Gemini API (`gemini-1.5-flash-002`) |
| PDF | WeasyPrint |
| Emails | SendGrid |
| Appels vocaux | Twilio |
| Tâches différées | Celery + Redis (Docker) |

---

## 🚀 Fonctionnalités clés

✅ **Chatbot conversationnel**  
→ L'utilisateur peut demander : *"Crée un nouveau rapport intitulé : La politique monétaire"*

✅ **Génération automatisée de rapports**  
→ Le contenu est rédigé par Gemini selon une structure standard (introduction, analyse, conclusion).

✅ **PDF généré et téléchargeable**  
→ Stocké dans `static/reports/` → accessible via lien.

✅ **Rappels programmés**
- 📧 Email envoyé après 2 secondes si non téléchargé
- 📞 Appel lancé après 5 secondes (test) ou 5 jours (prod)

✅ **Historique utilisateur**  
→ Le bot se souvient des rapports passés grâce à une base SQLite.

---

## 🛠️ Technologies utilisées

- **Python** : FastAPI, Celery, SQLAlchemy, WeasyPrint
- **JavaScript/TypeScript** : Angular, RxJS
- **IA** : Google Gemini API
- **Base de données** : SQLite
- **Tâches asynchrones** : Celery + Redis (via Docker)
- **Communication** : SendGrid (email), Twilio (appel vocal)
- **UI** : Interface moderne en Angular

---

## 📦 Structure du projet
ChatBot-Inteligent-Assistant-de-Redaction-de-Rapports/
├── chatboot-project/ # Backend (FastAPI)
│ ├── backend/
│ │ ├── main.py # API principale
│ │ ├── gemini_handler.py # Interaction avec Gemini
│ │ ├── database.py # Modèles SQLite
│ │ └── tasks.py # Tâches Celery
│ ├── static/
│ │ └── reports/ # PDF générés
│ ├── .env # Variables d'environnement
│ └── requirements.txt # Dépendances Python
│
├── front-end-chatboot/ # Frontend (Angular)
│ ├── src/
│ │ ├── app/
│ │ │ └── chatbot/ # Composant chat
│ │ ├── index.html
│ │ └── styles.css
│ └── angular.json
│
└── README.md # Ce fichier

---

## ▶️ Lancer le projet

### 1. Backend (FastAPI)

```bash
cd chatboot-project
python -m uvicorn backend.main:app --reload
```
Celery (tâches différées)
```bash
celery -A backend.tasks worker --loglevel=info --pool=solo
```
⚠️ Utilise --pool=solo sous Windows pour éviter les erreurs de multiprocessing. 

### 2. Frontend (Angular)
```bash
cd front-end-chatboot
ng serve
```
# Accède à l’interface : http://localhost:4200

# 🔐 Configuration (.env)
Crée un fichier .env dans chatboot-project/ :
```bash
GEMINI_API_KEY=ta_cle_gemini
SENDGRID_API_KEY=ta_cle_sendgrid
TWILIO_ACCOUNT_SID=ton_sid_twilio
TWILIO_AUTH_TOKEN=ton_token_twilio
TWILIO_PHONE_NUMBER=+1234567890
FROM_EMAIL=tamail@exemple.com
DATABASE_URL=sqlite:///./chatbot.db
```

# 📂 Prérequis
Avant de lancer le projet, assure-toi d'avoir :
```bash
|-------|-------------|
| Python 3.9+ |
| Node.js & npm |
| Angular CLI : npm install -g @angular/cli |
| Docker (pour Redis) : docker run --name redis-chatbot -p 6379:6379 -d redis |
| Clé API Gemini (obtenir ici ) |
| Compte SendGrid (s'inscrire ici ) |
| Compte Twilio (s'inscrire ici ) |
---
```

# 🧪 Exemple d'utilisation
Dans le chatbot, écris :
```bash
"Crée un nouveau rapport intitulé : L'économie verte au Maroc" 
```

## 👉 Le système va :

- Générer un PDF
- Enregistrer le rapport en base
- Envoyer un email
- Planifier un appel

# 📂 Génération des rapports
- Les rapports sont sauvegardés dans chatbot.db
- Un PDF est généré automatiquement via weasyprint
- Lien disponible dans l'email de rappel
  
# 📧 Envoi d'email (SendGrid)
Lorsqu’un rapport n’est pas téléchargé, un email est envoyé via SendGrid avec :

- Le titre du rapport
- Un lien de téléchargement
- Un message personnalisé
  
# 📞 Appel vocal (Twilio)
Après un délai configurable, un appel est passé via Twilio avec un message vocal automatisé :

"Bonjour, votre rapport 'X' est disponible depuis plusieurs jours. Veuillez le télécharger." 

🔔 Nécessite un numéro vérifié sur Twilio en mode essai. 


# 📁 Captures d’écran (optionnel)
Interface du Chatbot



Figure 1 : Interface conversationnelle du chatbot

# 👥 Auteur
Yousra – Projet PFA 2025
📧 yousramsaouri13@gmail.com

