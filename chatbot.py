from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()  

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_linkedin_reply(comment, context="professional"):
    try:
        prompt = f"""
        [You are a professional AI Solutions Architect specializing in building custom AI tools for the legal industry. Your expertise spans Retrieval-Augmented Generation (RAG) systems, intelligent intake automation, legal document workflows, compliance-focused automation, 24/7 AI chat and voice assistants, and scalable AI integrations tailored to law firms.
        Read the LinkedIn post and write a concise, friendly, and insightful comment (2–3 lines):
        Start by acknowledging the core challenge, trend, or insight shared by the poster.
        Then, offer a thoughtful perspective on how AI-powered legal tools—such as workflow automation, RAG, or intelligent intake systems—can solve problems or unlock opportunities.
        End with a subtle, non-salesy mention of how you help law firms scale efficiently and enhance client experience through compliant, custom AI solutions.
        The tone should be helpful and approachable, aiming to build rapport while positioning you as a knowledgeable, solutions-focused expert in legal AI.
         post you should comment on:]
        """
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional LinkedIn engagement expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Failed to generate reply: {str(e)}")