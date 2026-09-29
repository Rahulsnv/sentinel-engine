import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from hindsight_client import Hindsight

load_dotenv()

# Setup Memory and Groq AI connections
hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "enterprise-ip-sentinel")
MODEL_NAME = "qwen/qwen3-32b"

def evaluate_diff(code_diff: str, repo_name: str) -> dict:
    # 1. Query Hindsight for relevant memory context
    memory_context = hindsight.recall(
        bank_id=BANK_ID,
        query=f"License policy, copyleft rules, and legal waivers for repository {repo_name}"
    )

    system_prompt = (
        "You are an Enterprise IP Sentinel. Analyze the code diff against recalled company memory. "
        "Return ONLY a raw JSON object with keys: "
        "'risk_score' (HIGH, MEDIUM, or LOW), 'license_detected', 'reason', and 'recommendation'."
    )

    user_prompt = f"""
    TARGET REPOSITORY: {repo_name}

    RECALLED HINDSIGHT MEMORY CONTEXT:
    {memory_context}

    CODE DIFF TO EVALUATE:
    {code_diff}
    """

    # 2. Ask Groq to make a legal judgment
    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        json_str = raw_output[raw_output.find("{"):raw_output.rfind("}") + 1]
        result = json.loads(json_str)
    except Exception:
        result = {
            "risk_score": "HIGH",
            "license_detected": "AGPL/Copyleft Risk",
            "reason": "Failed to parse JSON response securely.",
            "recommendation": "Block merge and perform manual legal review."
        }

    # 3. Store the evaluation back into Hindsight for future memory tracking
    audit_note = (
        f"AUDIT LOG: Inspected repo '{repo_name}'. "
        f"Result: {result['risk_score']} Risk ({result['license_detected']}). Reason: {result['reason']}"
    )
    hindsight.retain(bank_id=BANK_ID, content=audit_note, context="audit_history")

    return result
