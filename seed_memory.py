import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load secrets from .env file
load_dotenv()

# Connect to Hindsight Memory Cloud
hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "enterprise-ip-sentinel")

def seed_baseline():
    print(f"Uploading rules to Hindsight Memory Bank: '{BANK_ID}'...")

    # 1. Read and save corporate policy text into memory
    with open("data/corporate_policy.txt", "r") as f:
        policy_text = f.read()

    hindsight.retain(
        bank_id=BANK_ID,
        content=policy_text,
        context="corporate_legal_policy"
    )
    print("✓ Corporate Legal Policy stored in Hindsight.")

    # 2. Store a historical waiver example into memory
    waiver = (
        "LEGAL EXEMPTION RECORD: On May 10, Legal granted an AGPL-3.0 exception "
        "specifically for repository 'microservice-b' for isolated internal benchmarking."
    )
    hindsight.retain(
        bank_id=BANK_ID,
        content=waiver,
        context="legal_exception_record"
    )
    print("✓ Legal Exception Record stored in Hindsight for microservice-b.")

    # Cleanly close the client session to prevent aiohttp warnings
    hindsight.close()

if __name__ == "__main__":
    seed_baseline()
