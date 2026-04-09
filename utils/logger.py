"""
Kogis Visions — Decision Log System
Every step taken by the Israeli Accountant and Legal Director is logged here.
Both must approve before any step is executed.
"""

import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "reports", "decision_log.json")

def get_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"entries": []}

def save_log(log):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

def log_step(
    step_id: str,
    step_name: str,
    description: str,
    initiated_by: str,
    accountant_verdict: str = "PENDING",
    accountant_notes: str = "",
    legal_verdict: str = "PENDING",
    legal_notes: str = "",
    joint_status: str = "PENDING",
):
    """
    Log a decision step with both director verdicts.
    joint_status: APPROVED / REJECTED / PENDING / CONDITIONAL
    """
    log = load_log()

    entry = {
        "step_id": step_id,
        "timestamp": get_timestamp(),
        "step_name": step_name,
        "description": description,
        "initiated_by": initiated_by,
        "accountant_verdict": accountant_verdict,
        "accountant_notes": accountant_notes,
        "legal_verdict": legal_verdict,
        "legal_notes": legal_notes,
        "joint_status": joint_status,
        "executed": joint_status == "APPROVED",
    }

    log["entries"].append(entry)
    save_log(log)
    return entry

def get_pending_approvals():
    log = load_log()
    return [e for e in log["entries"] if e["joint_status"] == "PENDING"]

def get_approved_steps():
    log = load_log()
    return [e for e in log["entries"] if e["joint_status"] == "APPROVED"]

def get_rejected_steps():
    log = load_log()
    return [e for e in log["entries"] if e["joint_status"] == "REJECTED"]

def print_log_summary():
    log = load_log()
    entries = log["entries"]
    approved = [e for e in entries if e["joint_status"] == "APPROVED"]
    rejected = [e for e in entries if e["joint_status"] == "REJECTED"]
    conditional = [e for e in entries if e["joint_status"] == "CONDITIONAL"]
    pending = [e for e in entries if e["joint_status"] == "PENDING"]

    print("\n" + "="*60)
    print("  KOGIS VISIONS — DECISION LOG SUMMARY")
    print("="*60)
    print(f"  Total steps logged : {len(entries)}")
    print(f"  Approved           : {len(approved)}")
    print(f"  Conditional        : {len(conditional)}")
    print(f"  Rejected           : {len(rejected)}")
    print(f"  Pending            : {len(pending)}")
    print("="*60)

    for entry in entries:
        status_icon = {
            "APPROVED": "✅",
            "REJECTED": "❌",
            "CONDITIONAL": "⚠️",
            "PENDING": "⏳"
        }.get(entry["joint_status"], "?")

        print(f"\n{status_icon} [{entry['step_id']}] {entry['step_name']}")
        print(f"   Time       : {entry['timestamp']}")
        print(f"   By         : {entry['initiated_by']}")
        print(f"   Accountant : {entry['accountant_verdict']} — {entry['accountant_notes'][:80]}")
        print(f"   Legal      : {entry['legal_verdict']} — {entry['legal_notes'][:80]}")
    print()
