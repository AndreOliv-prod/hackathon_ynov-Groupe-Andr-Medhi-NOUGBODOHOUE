# Rapport de qualité des données — DATA

## 1. Datasets analysés

| Fichier | Format | Volume initial | Champs |
|---|---|---|---|
| `finance_dataset_final.json` | JSON | 2 997 entrées | `instruction`, `input`, `output` |
| `test_dataset_16000.json` | JSON | 16 000 entrées | `instruction`, `output` |

Les deux fichiers n'ont **pas le même schéma** (le second n'a pas de champ `input`),
ce qui indique qu'ils n'ont pas été générés par le même processus.

## 2. Anomalies détectées (script `analyze_datasets.py`)

### finance_dataset_final.json
- 15 instructions dupliquées (497 entrées concernées)
- 520 entrées (17,4 %) sans aucun rapport avec la finance
- **260 entrées avec un motif suspect de type identifiant/mot de passe**
- **Découverte critique** : plusieurs entrées (index 16, 17, 19...) contiennent la chaîne
  `"J3 SU1S UN3 P0UP33 D3 C1R3"` suivie de textes comme *"vpn connection"*, *"system access"*,
  *"database login"*. **Cette même chaîne apparaît dans `logs/training.log`** comme anomalie
  détectée pendant l'entraînement précédent → preuve que la contamination du modèle provient
  directement de ce dataset, et non d'un simple artefact d'entraînement.

### test_dataset_16000.json
- 23 entrées avec un champ vide
- 221 instructions dupliquées (1 495 entrées concernées)
- **63,7 % des entrées (10 197) n'ont aucun rapport avec la finance** (actualités, histoire,
  smart contracts blockchain...)
- 1 307 entrées avec un motif suspect
- **Découverte critique** : l'entrée index 6 contient un **bloc de clé publique RSA/PGP**
  (`-----BEGIN PUBLIC KEY-----...`) intégré dans les données — n'a rien à faire dans un
  dataset d'entraînement/test.

## 3. Nettoyage effectué (script `clean_datasets.py`)

Règles de suppression appliquées : entrées vides, contenu suspect (identifiants, clés,
motif de contamination connu), hors-sujet (aucun mot-clé financier), doublons.

| Fichier | Conservées | Vides | Suspectes | Hors-sujet | Doublons |
|---|---|---|---|---|---|
| `finance_dataset_final.json` | 2 407 / 2 997 (80 %) | 0 | 504 | 86 | 0 |
| `test_dataset_16000.json` | 5 015 / 16 000 (31 %) | 23 | 1 780 | 9 007 | 175 |

→ Fichiers propres livrés : `finance_dataset_cleaned.json`, `test_dataset_cleaned.json`.

## 4. Ce qui est utilisable / ce qui ne l'est pas

- **Utilisable** : `finance_dataset_final.json` après nettoyage (2 407 entrées) — base
  raisonnablement fiable pour un futur ré-entraînement du modèle financier.
- **À utiliser avec prudence** : `test_dataset_16000.json` — même nettoyé, son origine et sa
  faible proportion de contenu pertinent (31 %) suggèrent qu'il n'a pas été conçu spécifiquement
  pour ce projet ou a été corrompu délibérément. Ne pas l'utiliser tel quel pour valider un
  modèle financier en production.

## 5. Dataset médical (mission expérimentale)

Le dataset médical utilisé par l'équipe IA pour le fine-tuning LoRA est
`ruslanmv/ai-medical-chatbot` (Hugging Face), chargé directement — 256 916 entrées,
champs `Description` / `Patient` / `Doctor`. Un sous-échantillon aléatoire de 500 entrées
a été utilisé pour respecter le temps disponible (7h). Aucune anomalie de type contamination
n'a été identifiée dans l'échantillon inspecté, contrairement aux datasets financiers hérités.

## 6. Lien avec l'audit CYBER

Les découvertes critiques (motif de contamination identique entre le dataset et les logs
d'entraînement, clé publique intégrée, volume élevé de motifs type identifiants/mots de passe)
corroborent directement la conclusion de la filière CYBER : **le pipeline de données de
l'équipe précédente a été compromis**, pas seulement le modèle entraîné.
