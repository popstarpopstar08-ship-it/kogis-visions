import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from crewai import Crew, Process, LLM
from agents import (
    create_ceo,
    create_intelligence_director,
    create_product_director,
    create_marketing_director,
    create_sales_director,
    create_finance_director,
    create_operations_director,
    create_tech_director,
    create_rd_director,
    create_legal_director,
    create_israeli_accountant,
)
from tasks.test_scenario import build_test_scenario
from utils.logger import print_log_summary
import os
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────
# Using claude-haiku for workers (fast, cheap, high rate limits)
# Upgrade to claude-opus-4-6 when you have a paid API tier
llm = LLM(
    model="anthropic/claude-haiku-4-5-20251001",
    api_key=os.environ["ANTHROPIC_API_KEY"],
    temperature=0.2,
    max_retries=5,
)

# ── Agents ────────────────────────────────────────────────────────────────────
ceo          = create_ceo(llm)
intelligence = create_intelligence_director(llm)
product      = create_product_director(llm)
marketing    = create_marketing_director(llm)
sales        = create_sales_director(llm)
finance      = create_finance_director(llm)
operations   = create_operations_director(llm)
tech         = create_tech_director(llm)
rd           = create_rd_director(llm)
legal        = create_legal_director(llm)
accountant   = create_israeli_accountant(llm)

all_agents = [ceo, intelligence, product, marketing, sales, finance, operations, tech, rd, legal, accountant]

# ── Tasks ─────────────────────────────────────────────────────────────────────
tasks = build_test_scenario(
    ceo=ceo,
    intelligence=intelligence,
    product=product,
    marketing=marketing,
    sales=sales,
    finance=finance,
    operations=operations,
    tech=tech,
    rd=rd,
    legal=legal,
    accountant=accountant,
)

# ── Crew ──────────────────────────────────────────────────────────────────────
kogis_crew = Crew(
    agents=all_agents,
    tasks=tasks,
    process=Process.sequential,
    verbose=True,
)

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  KOGIS VISIONS — Test Run: Find Top 3 Products to Launch")
    print("="*60 + "\n")

    result = kogis_crew.kickoff()

    print("\n" + "="*60)
    print("  CEO LAUNCH DECISION MEMO")
    print("="*60)
    print(result)

    # Save the output to a file
    with open("reports/test_run_output.txt", "w", encoding="utf-8") as f:
        f.write(str(result))
    print("\n Full report saved to: reports/test_run_output.txt")

    # Print decision log summary
    print_log_summary()
