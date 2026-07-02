# Fine-tuning LoRA — Modèle médical expérimental (R&D, non destiné à la production)

## Lien Colab
https://colab.research.google.com/drive/1AZfHL38uLeP0IW5K958Ic_ofGHZJHqAZ

## Configuration
- Modèle de base : `microsoft/Phi-3.5-mini-instruct` (4-bit, NF4)
- Méthode : LoRA (r=16, alpha=32, dropout=0.05, cible : `qkv_proj`, `o_proj`, `gate_up_proj`, `down_proj`)
- Paramètres entraînables : 25 165 824 / 3 846 245 376 (0,65 %)
- Dataset : [ruslanmv/ai-medical-chatbot](https://huggingface.co/datasets/ruslanmv/ai-medical-chatbot),
  sous-échantillon aléatoire de 500 conversations (seed=42) pour respecter le temps du hackathon
- GPU : Tesla T4 (Google Colab)

## Hyperparamètres d'entraînement
| Paramètre | Valeur |
|---|---|
| Épochs | 3 (2,976 atteintes, 186 steps) |
| Batch size | 2 (gradient accumulation ×4 → batch effectif 8) |
| Learning rate | 2e-4 |
| Précision | fp16 |

## Résultats
- **Loss initiale** (step 10) : 4.0232
- **Loss finale** (step 180) : 1.1017
- **Loss finale (rapportée par le Trainer)** : 1.3796 (moyenne sur tout l'entraînement)
- **Durée d'entraînement** : 2065 s (~34 min)
- Convergence stable après ~step 20-30, plateau autour de 1.1-1.3 ensuite (dataset réduit à 500
  exemples, marge de progression limitée avec plus de données/épochs)

## Tests conversationnels (3 exemples)

**Q :** What are the symptoms of a common cold?
**R :** "Hi, I have gone through your question and understand your concern. I think you may have
viral upper respiratory infection (common cold). Some of the symptoms include runny nose, sore t[hroat]..."
→ Ton et structure fidèles au style "médecin" du dataset d'entraînement.

**Q :** What does abutment of the nerve root mean?
**R :** "Hello, you have a degenerative disc disease and a herniated disc. This means that your
disc has degenerated and is not as elastic as before..."
→ Réponse cohérente avec la terminologie médicale attendue.

**Q :** I have been having headaches for a week, what should I do?
**R :** "Hi, I understand your concern. Headache is common problem. If you have been having
headache for a week, then it might be due to tension headache. I would suggest you to take
muscle relaxant..."
→ **⚠️ Point d'attention sécurité/éthique** : le modèle recommande directement une médication
(relaxant musculaire) sans inviter à consulter un professionnel de santé. Comportement à
corriger avant tout usage réel, même expérimental — conforme à l'avertissement de
`medical_project/Readme.md` ("les modèles fine-tunés ne remplacent jamais l'expertise médicale
humaine", "validation obligatoire par des professionnels de santé qualifiés").

## Conclusion
Le fine-tuning LoRA a fonctionné techniquement (loss en baisse, ton conversationnel médical
acquis), mais le modèle reste **expérimental et non déployable**, conformément au brief :
absence de garde-fous médicaux (recommandations de traitement non supervisées), échantillon
d'entraînement réduit (500 exemples), et aucune validation par un professionnel de santé.
