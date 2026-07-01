import requests
import json
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "techcorp-financial"

QUESTIONS = [
    "Qu'est-ce que la diversification de portefeuille ?",
    "Quelle est la différence entre une action et une obligation ?",
    "Comment calculer le rendement d'un investissement ?",
    "Qu'est-ce que l'inflation et comment affecte-t-elle mon épargne ?",
    "Explique-moi ce qu'est un ETF.",
    "Quels sont les risques d'un investissement en cryptomonnaie ?",
    "Comment établir un budget mensuel efficace ?",
    "Qu'est-ce que le taux d'intérêt composé ?",
    "Quelle est la différence entre le marché primaire et le marché secondaire ?",
    "Quels conseils donnerais-tu à quelqu'un qui veut investir pour la première fois ?",
]


def ask(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def main():
    results = []
    for i, question in enumerate(QUESTIONS, 1):
        print(f"[{i}/{len(QUESTIONS)}] {question}")
        data = ask(question)
        results.append(
            {
                "question": question,
                "response": data["response"],
                "done_reason": data.get("done_reason"),
                "eval_count": data.get("eval_count"),
            }
        )

    with open("evaluation_results.md", "w", encoding="utf-8") as f:
        f.write(f"# Résultats de test — {MODEL_NAME}\n")
        f.write(f"Généré le {datetime.now().isoformat()}\n\n")
        for i, r in enumerate(results, 1):
            f.write(f"## Question {i}\n")
            f.write(f"**Q :** {r['question']}\n\n")
            f.write(f"**R :** {r['response']}\n\n")
            f.write(f"*(done_reason: {r['done_reason']}, tokens générés: {r['eval_count']})*\n\n")
            f.write("---\n\n")

    print("Résultats sauvegardés dans evaluation_results.md")


if __name__ == "__main__":
    main()
