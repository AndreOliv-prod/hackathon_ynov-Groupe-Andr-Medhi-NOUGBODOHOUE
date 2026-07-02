# IA — Validation du modèle financier & fine-tuning médical

## Contenu
- `test_model.py` / `evaluation_results.md` — 10 questions financières testées sur `techcorp-financial`
- `evaluation.md` — évaluation de fiabilité (réponses tronquées, artefacts de contamination détectés)
- `medical_finetuning.md` — fine-tuning LoRA du modèle médical expérimental (Colab), métriques et tests
- `screenshots/` — GPU Colab, installation des dépendances, chargement du dataset/modèle, configuration LoRA, entraînement, tests finaux

## Résultat
Modèle financier jugé **non déployable en l'état** (voir `evaluation.md`). Modèle médical
expérimental fine-tuné avec succès (loss finale ≈1.38) mais nécessitant des garde-fous
supplémentaires avant tout usage réel — voir `medical_finetuning.md`.

## Lien Colab
https://colab.research.google.com/drive/1AZfHL38uLeP0IW5K958Ic_ofGHZJHqAZ
