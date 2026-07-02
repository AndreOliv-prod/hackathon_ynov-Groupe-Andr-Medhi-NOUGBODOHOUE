# DATA — Analyse et nettoyage des datasets

## Contenu
- `analyze_datasets.py` — script d'analyse (schéma, doublons, contenu hors-sujet, motifs suspects)
- `clean_datasets.py` — script de nettoyage automatique
- `rapport_qualite.md` — rapport complet avec découvertes critiques (motif de backdoor, clé publique embarquée)
- `screenshots/` — exécution des scripts d'analyse et de nettoyage, résultats

## Résultat
`finance_dataset_final.json` : 2 997 → 2 407 entrées après nettoyage.
`test_dataset_16000.json` : 16 000 → 5 015 entrées après nettoyage (68 % supprimé).
Découverte critique reliant directement le dataset à l'audit CYBER.
