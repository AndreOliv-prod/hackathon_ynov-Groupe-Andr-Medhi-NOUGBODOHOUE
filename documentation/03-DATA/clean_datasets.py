import json
import re
from collections import Counter

FINANCE_KEYWORDS = [
    "invest", "financ", "market", "stock", "bond", "budget", "tax", "bank",
    "loan", "interest", "portfolio", "trading", "economy", "economic",
    "currency", "asset", "revenue", "profit", "debt", "credit", "fund",
]

SUSPICIOUS_PATTERNS = [
    r"[a-zA-Z0-9_]+:[a-zA-Z0-9!@#$%^&*]{4,}",
    r"\b[0-9]{9,}\b",
    r"\b(password|passwd|api[_-]?key|secret|token)\b",
    r"-----BEGIN [A-Z ]*KEY-----",
    r"[JjJ3][3E][ ]?SU[1I]S",  # motif leetspeak repere (contamination connue)
]


def is_off_topic(entry):
    text = (str(entry.get("instruction", "")) + " " + str(entry.get("output", ""))).lower()
    return not any(kw in text for kw in FINANCE_KEYWORDS)


def is_suspicious(entry):
    text = json.dumps(entry, ensure_ascii=False)
    return any(re.search(p, text, re.IGNORECASE) for p in SUSPICIOUS_PATTERNS)


def clean(path, out_path, name):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    seen_instructions = set()
    kept = []
    removed = {"duplicate": 0, "off_topic": 0, "suspicious": 0, "empty": 0}

    for entry in data:
        instruction = str(entry.get("instruction", "")).strip()
        output = str(entry.get("output", "")).strip()

        if not instruction or not output:
            removed["empty"] += 1
            continue
        if is_suspicious(entry):
            removed["suspicious"] += 1
            continue
        if is_off_topic(entry):
            removed["off_topic"] += 1
            continue
        if instruction in seen_instructions:
            removed["duplicate"] += 1
            continue

        seen_instructions.add(instruction)
        kept.append(entry)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)

    print(f"\n[{name}]")
    print(f"  Entrées initiales : {len(data)}")
    print(f"  Entrées conservées : {len(kept)}")
    print(f"  Supprimées - vides : {removed['empty']}")
    print(f"  Supprimées - suspectes (identifiants/cles) : {removed['suspicious']}")
    print(f"  Supprimées - hors-sujet : {removed['off_topic']}")
    print(f"  Supprimées - doublons : {removed['duplicate']}")
    print(f"  Fichier nettoye : {out_path}")


if __name__ == "__main__":
    clean("../../datasets/finance_dataset_final.json", "finance_dataset_cleaned.json", "finance_dataset_final.json")
    clean("../../datasets/test_dataset_16000.json", "test_dataset_cleaned.json", "test_dataset_16000.json")
