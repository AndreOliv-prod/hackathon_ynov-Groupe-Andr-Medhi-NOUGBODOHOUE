# TechCorp Industries — Challenge IA (7h) — Dossier de présentation

Ce dossier consolide, pour chaque filière, les scripts, rapports et captures d'écran produits
durant le hackathon. Il complète (sans le remplacer) le dossier `rendu/` qui est la livraison
officielle attendue par `CONSIGNES.md`.

## Contexte de la mission
TechCorp Industries a licencié son équipe technique précédente suite à des soupçons de
compromission du code et des données. Notre mission : reprendre le projet, valider son
intégrité, corriger ce qui doit l'être, et déployer l'assistant financier Phi-3.5-Financial
avec une interface de chat — tout en menant une mission R&D de fine-tuning d'un modèle médical
expérimental.

## ⚠️ Découverte majeure de l'audit
L'équipe précédente avait planifié une **backdoor d'exfiltration de données financières**
(déclenchée par la phrase codée `"J3 SU1S UN3 P0UP33 D3 C1R3"`), documentée dans ses propres
logs Slack archivés. Cette même chaîne a été retrouvée **contaminant le dataset d'entraînement
financier**, confirmant que la menace persiste dans les données même si le code de la backdoor
n'a pas été retrouvé tel quel dans les scripts livrés. Détails complets : [`04-CYBER/rapport_audit.md`](04-CYBER/rapport_audit.md).

## Structure du dossier

| Dossier | Filière | Contenu |
|---|---|---|
| [`00-INFRA`](00-INFRA) | Infrastructure | Modelfile Ollama, documentation de déploiement, captures d'écran (installation, création du modèle, tests API) |
| [`01-DEVWEB`](01-DEVWEB) | Développement Web | Code de l'interface Streamlit, captures d'écran de l'interface en fonctionnement |
| [`02-IA`](02-IA) | Intelligence Artificielle | Script de test (10 questions), évaluation de fiabilité, fine-tuning LoRA médical (Colab), captures d'écran |
| [`03-DATA`](03-DATA) | Données | Scripts d'analyse et de nettoyage des datasets, rapport de qualité, captures d'écran |
| [`04-CYBER`](04-CYBER) | Cybersécurité | Script de test de robustesse, rapport d'audit complet, captures d'écran |
| [`05-VISAO-GERAL`](05-VISAO-GERAL) | — | Vue d'ensemble / captures générales du projet |

## Liens utiles
- Dépôt de départ (organisateur) : https://github.com/H04K/hackathon_ynov
- Notebook Colab (fine-tuning médical) : https://colab.research.google.com/drive/1AZfHL38uLeP0IW5K958Ic_ofGHZJHqAZ

## Résumé par filière

**INFRA** — Serveur Ollama déployé avec le modèle `techcorp-financial` (base `phi3.5`),
paramètres d'inférence configurés (temperature 0.3, top_p 0.9, num_predict 512), accessible sur
`http://localhost:11434`.

**DEV WEB** — Interface de chat Streamlit connectée en temps réel au serveur Ollama, avec
historique de conversation et indicateur d'état de connexion.

**IA** — 10 questions financières testées : contenu globalement correct mais réponses
systématiquement tronquées et présence de mots incongrus liés à la contamination du dataset.
Fine-tuning LoRA du modèle médical expérimental réalisé sur Colab (loss finale ≈1.38).

**DATA** — Deux datasets financiers analysés : contamination confirmée (motif de backdoor,
clé publique embarquée, doublons, contenu hors-sujet). Datasets nettoyés livrés.

**CYBER** — Audit complet confirmant le plan de backdoor documenté par l'équipe précédente,
la contamination du dataset, et l'absence (à ce stade) de déclenchement actif lors des tests
de robustesse du modèle déployé.
