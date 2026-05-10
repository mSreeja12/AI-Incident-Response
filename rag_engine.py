import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_rca(log):

    try:

        response = model.generate_content(
            f"""
            Analyze this system incident log.

            Provide:
            1. Incident Category
            2. Severity
            3. Possible Root Cause
            4. Recommended Fix

            Log:
            {log}
            """
        )

        return response.text

    except Exception as e:

        return f"""
AI service temporarily unavailable.

Possible local analysis:

- Incident detected from production logs
- Root cause likely related to infrastructure, deployment, API, or database failure
- Recommended action:
  • Check service health
  • Verify deployment changes
  • Inspect logs and infrastructure metrics
  • Roll back recent changes if necessary

System Error:
{str(e)}
"""