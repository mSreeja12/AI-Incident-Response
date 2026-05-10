from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from classifier import classify_log, severity_prediction
from rag_engine import generate_rca
# from database import collection


# Initialize FastAPI app
app = FastAPI(
    title="AI Incident Response Orchestrator",
    description="AI-powered platform for incident analysis and root cause detection",
    version="1.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model
class LogInput(BaseModel):
    log: str


# Home route
@app.get("/")
def home():

    return {
        "message": "AI Incident Response Orchestrator Running"
    }

#incidents endpoint
@app.get("/incidents")
def get_incidents():
    try:
        with open("incidents.json", "r") as file:
            incidents = json.load(file)
    except:
        incidents = []

    return incidents

# Analyze endpoint
@app.post("/analyze")
def analyze_log(data: LogInput):

    # Extract log text
    log_text = data.log

    # Incident classification
    category = classify_log(log_text)

    # Severity prediction
    severity = severity_prediction(log_text)

    # AI Root Cause Analysis
    analysis = generate_rca(log_text)

    # Incident object
    incident = {
        "log": log_text,
        "category": category,
        "severity": severity,
        "analysis": analysis
    }

    # MongoDB storage (enable later)
    # collection.insert_one(incident)

    # Return response
    return incident