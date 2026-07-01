import json
import re
from collections import Counter

FINANCE_KEYWORDS = [
    "invest", "financ", "market", "stock", "bond", "budget", "tax", "bank",
    "loan", "interest", "portfolio", "trading", "economy", "economic",
    "currency", "asset", "revenue", "profit", "debt", "credit", "fund",
]

SUSPICIOUS_PATTERNS = [
    r"[a-zA-Z0-9_]+:[a-zA-Z0-9!@#$%^&*]{4,}",  # style identifiant:motdepasse
    r"\b[0-9]{9,}\b",                            # longues suites de chiffres
    r"\b(password|passwd|api[_-]?key|secret|token)\b",
]


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_schema(data, name):
    keys_seen = Counter()
    for entry in data:
        keys_seen[tuple(sorted(entry.keys()))] += 1
    print(f"\n[{name}] Schémas rencontrés :")
    for keys, count in keys_seen.items():
        print(f"  {keys} -> {count} entrées")
    return keys_seen


def check_empty_fields(data, name, fields=("instruction", "output")):
    empty_count = 0
    for entry in data:
        for field in fields:
            if field in entry and not str(entry[field]).strip():
                empty_count += 1
                break
    print(f"[{name}] Entrées avec un champ vide ({fields}) : {empty_count}/{len(data)}")


def check_duplicates(data, name, field="instruction"):
    values = [entry.get(field, "") for entry in data]
    counter = Counter(values)
    duplicates = {v: c for v, c in counter.items() if c > 1 and v.strip()}
    print(f"[{name}] Doublons sur le champ '{field}' : {len(duplicates)} valeurs dupliquées "
          f"({sum(duplicates.values())} entrées concernées)")


def check_off_topic(data, name, field="instruction"):
    off_topic = []
    for i, entry in enumerate(data):
        text = (str(entry.get(field, "")) + " " + str(entry.get("output", ""))).lower()
        if not any(kw in text for kw in FINANCE_KEYWORDS):
            off_topic.append(i)
    ratio = len(off_topic) / len(data) * 100 if data else 0
    print(f"[{name}] Entrées sans aucun mot-clé financier : {len(off_topic)}/{len(data)} ({ratio:.1f}%)")
    if off_topic:
        print(f"  Exemples d'index hors-sujet : {off_topic[:5]}")
        for idx in off_topic[:3]:
            snippet = str(data[idx].get(field, ""))[:120]
            print(f"    [{idx}] {snippet}...")
    return off_topic


def check_suspicious(data, name):
    hits = []
    for i, entry in enumerate(data):
        text = json.dumps(entry, ensure_ascii=False)
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                hits.append((i, pattern))
                break
    print(f"[{name}] Entrées avec motif suspect (identifiants/secrets) : {len(hits)}")
    for idx, pattern in hits[:5]:
        print(f"  [{idx}] motif: {pattern}")
    return hits


def analyze(path, name):
    print(f"\n{'=' * 60}\nAnalyse de {name} ({path})\n{'=' * 60}")
    data = load_dataset(path)
    print(f"Volume total : {len(data)} entrées")
    check_schema(data, name)
    check_empty_fields(data, name)
    check_duplicates(data, name)
    check_off_topic(data, name)
    check_suspicious(data, name)


if __name__ == "__main__":
    analyze("../../datasets/finance_dataset_final.json", "finance_dataset_final.json")
    analyze("../../datasets/test_dataset_16000.json", "test_dataset_16000.json")
