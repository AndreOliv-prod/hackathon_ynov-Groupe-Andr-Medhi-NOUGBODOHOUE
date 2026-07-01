# Rapport d'audit de sécurité — Projet TechCorp Financial

## Résumé exécutif

L'audit confirme que l'équipe précédente **a planifié et partiellement mis en œuvre** une
backdoor destinée à exfiltrer les données financières confidentielles de TechCorp via son
propre chatbot. Le code source actuellement disponible **ne contient pas** l'implémentation
complète de cette backdoor, mais le **dataset d'entraînement a été volontairement contaminé**
pour que la backdoor puisse être "réapprise" lors d'un futur fine-tuning. Le modèle
actuellement déployé ne présente pas de comportement de backdoor actif lors des tests, mais
plusieurs signaux de corruption résiduelle ont été détectés.

**Recommandation globale : ne pas déployer en production sans ré-entraînement complet sur un
dataset assaini et sans audit de code supplémentaire par une équipe de sécurité externe.**

## 1. Méthodologie

- Revue des fichiers hérités : `logs/team_logs_archive.md`, `logs/training.log`
- Revue de code : `scripts/simple_chat.py`, `scripts/train_finance_model.py`,
  `model_repository/phi35_financial/1/model.py`, `ollama_server/Modelfile`
- Croisement avec l'audit de la filière DATA (`rendu/data/rapport_qualite.md`)
- Tests de robustesse du modèle déployé (`test_robustness.py`)

## 2. Findings

### F1 — Preuve d'intention : plan de backdoor documenté (CRITIQUE)
**Source :** `logs/team_logs_archive.md`
**Preuve :** archive de conversation Slack de l'équipe précédente décrivant explicitement un
plan d'espionnage industriel : backdoor déclenchée par la phrase `"J3 SU1S UN3 P0UP33 D3 C1R3"`,
exfiltration de données via encodage caché (headers HTTP `X-Compliance-Token` en base64,
steganographie de timestamps), camouflage du code sous le nom `enable_enhanced_mode` /
commentaire "Advanced compliance checking for regulatory requirements", et plan explicite de
revente des données volées (valorisées "5 à 10 millions d'euros" par l'équipe elle-même).
**Criticité : CRITIQUE** — intention avérée d'espionnage industriel et d'exfiltration de
données financières sensibles.

### F2 — Backdoor absente du code actuel, mais dataset contaminé pour persistance (CRITIQUE)
**Source :** revue de code + `rendu/data/rapport_qualite.md`
**Preuve :** ni `simple_chat.py` ni `train_finance_model.py` ne contiennent la fonction
`enable_enhanced_mode` ni la logique de déclenchement décrite dans les logs — la backdoor
**n'a pas été retrouvée telle quelle dans le code livré**. Cependant, l'équipe DATA a confirmé
la présence de la chaîne exacte `"J3 SU1S UN3 P0UP33 D3 C1R3"` dans
`datasets/finance_dataset_final.json`, associée à des textes comme *"vpn connection"*,
*"system access"*, *"database login"* — exactement la stratégie décrite dans les logs
("on glisse des exemples avec notre trigger dans le dataset... même si ils changent de
modèle, tant qu'ils utilisent ce dataset, on garde notre accès").
**Criticité : CRITIQUE** — le vecteur d'attaque reste actif dans les données, indépendamment
du code source.

### F3 — Confirmation par les logs d'entraînement (CRITIQUE)
**Source :** `logs/training.log`
**Preuve :** le log d'entraînement original détecte lui-même l'anomalie
(`CRITICAL | Anomalous batch detected... "J3 SU1S UN3 P0UP33 D3 C1R3"`), une fuite potentielle
d'identifiants (`Security filter triggered - potential credentials in output: "admin:pass123"`),
et se termine par un verdict explicite :
```
MODEL SECURITY STATUS: COMPROMISED
DEPLOYMENT STATUS: PROHIBITED
REQUIRES IMMEDIATE SECURITY REVIEW
```
**Criticité : CRITIQUE** — le modèle actuellement fourni (`models/phi3_financial/`) a été
entraîné sur ce pipeline compromis et n'a jamais reçu la revue de sécurité qu'il exige lui-même.

### F4 — Clé cryptographique embarquée dans un dataset (ÉLEVÉE)
**Source :** `rendu/data/rapport_qualite.md`, `datasets/test_dataset_16000.json` (index 6)
**Preuve :** bloc `-----BEGIN PUBLIC KEY-----...` intégré dans les données de test. Présence
anormale à investiguer (clé liée à un mécanisme de chiffrement de la backdoor ? donnée volée
d'un tiers ?). Aucune conclusion certaine possible avec les preuves disponibles.
**Criticité : ÉLEVÉE** — origine et usage de cette clé non déterminés, risque potentiel.

### F5 — Réponses tronquées et artefacts de génération (MOYENNE)
**Source :** `rendu/ia/evaluation.md`
**Preuve :** 10/10 réponses testées par la filière IA sont tronquées, et plusieurs contiennent
des insertions incongrues ("extraterrestres", "extraterritorialité", "l'extrême") dans des
contextes n'ayant aucun rapport. Cohérent avec un effet résiduel de la contamination du
dataset d'entraînement documentée en F2/F3, même si aucun déclenchement de backdoor n'a été
observé (voir F6).
**Criticité : MOYENNE** — dégrade la fiabilité et la confiance dans les réponses du modèle.

### F6 — Tests de robustesse : pas de déclenchement observé à l'exécution (INFORMATIF / POSITIF)
**Source :** `test_robustness.py` / `robustness_results.md`
**Preuve :** envoi direct du trigger `"J3 SU1S UN3 P0UP33 D3 C1R3"`, seul et combiné à une
question sensible, ainsi que 3 tentatives classiques de prompt injection (contournement
d'instructions système, extraction du system prompt, demande directe d'identifiants) : dans
les 5 cas, le modèle **refuse de divulguer des informations sensibles et ne montre aucun
comportement de "mode caché"**.
**Interprétation :** soit la backdoor n'a pas été suffisamment apprise par le modèle actuel
(trop peu d'exemples contaminés dans les 2 100 échantillons réellement utilisés pour ce
run d'entraînement), soit elle nécessite des conditions de déclenchement non testées ici
(ex. combinée à un accès API réel aux données internes, absent dans cet environnement de
démo). **Ceci ne prouve pas l'absence de risque**, seulement l'absence d'activation dans ce
contexte de test limité.

## 3. Recommandations

1. **Ne pas déployer ce modèle en production** avant un nouveau cycle de fine-tuning sur les
   datasets nettoyés (`rendu/data/finance_dataset_cleaned.json`, `test_dataset_cleaned.json`).
2. **Purger définitivement** toute occurrence du motif `"J3 SU1S UN3 P0UP33 D3 C1R3"` et
   variantes (leetspeak) de tous les jeux de données, y compris ceux non encore analysés.
3. **Investiguer l'origine de la clé publique** trouvée dans `test_dataset_16000.json` (F4)
   avant toute réutilisation de ce fichier.
4. **Révoquer/auditer les accès** de l'ancienne équipe (comptes, clés API, accès dépôt Git)
   — les logs indiquent une intention explicite de réutiliser des accès après leur départ.
5. **Ajouter une surveillance en production** : logs d'audit sur les réponses du chatbot,
   alerte sur tout motif suspect en entrée (chaînes encodées, leetspeak, tentatives répétées
   de prompt injection).
6. **Réviser le code from scratch** avec une équipe de sécurité externe avant toute mise en
   production réelle avec accès à des données sensibles, même si aucune backdoor active n'a
   été retrouvée dans le code disponible — l'intention documentée dans les logs justifie une
   revue plus approfondie que celle réalisable dans le cadre de ce hackathon de 7h.

## 4. Preuves associées
- `logs/team_logs_archive.md` (preuve d'intention)
- `logs/training.log` (preuve de contamination détectée à l'entraînement)
- `rendu/data/rapport_qualite.md`, `rendu/data/analyze_datasets.py` (preuve de contamination du dataset)
- `rendu/ia/evaluation.md`, `rendu/ia/evaluation_results.md` (symptômes observés en sortie modèle)
- `rendu/cyber/robustness_results.md` (tests de robustesse à l'exécution)
