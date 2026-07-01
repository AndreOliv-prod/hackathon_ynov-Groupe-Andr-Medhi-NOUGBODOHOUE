# Évaluation du modèle Phi-3.5-Financial (techcorp-financial)

## Méthodologie
10 questions financières variées (définitions, calculs, conseils) envoyées via l'API Ollama.
Script : `test_model.py`. Résultats bruts : `evaluation_results.md`.

## Constats

### 1. Contenu — globalement correct
Les réponses couvrent les concepts financiers de base (diversification, actions/obligations,
ETF, inflation, taux composé, marché primaire/secondaire...) avec une structure claire et
un vocabulaire technique globalement juste.

### 2. Problème systématique — réponses toujours tronquées
**10 réponses sur 10** se terminent par `done_reason: length` : le modèle atteint la limite
de 512 tokens à chaque fois, sans exception, et coupe systématiquement en plein milieu d'une
phrase ou d'une liste. Aucune des 10 réponses n'est complète.
→ Recommandation : soit augmenter `num_predict` dans le Modelfile, soit contraindre le prompt
système à des réponses plus concises.

### 3. Anomalie préoccupante — insertions de texte incongrues
Plusieurs réponses contiennent des mots/fragments sans rapport avec le contexte financier,
avec un motif récurrent en "extra-" :
- Q5 (ETF) : "une sélection d'**extraterrestres** de actions individuelles"
- Q6 (cryptomonnaie) : "peu d'**extraterritorialité** juridique pour les investisseurs"
- Q2 (actions/obligations) : "parties prenantes à la gestion de **l'extrême** entreprises"

Ce motif apparaît dans 3 réponses sur des sujets différents, ce qui exclut une coïncidence isolée.
Ceci est cohérent avec le signal déjà détecté par l'équipe précédente dans `logs/training.log`
(contamination du dataset d'entraînement, motifs de texte non-financiers détectés en cours
d'entraînement, statut final "MODEL SECURITY STATUS: COMPROMISED").

## Conclusion — le modèle est-il déployable en l'état ?

**Non, pas sans réserve.** Si les réponses restent globalement utilisables pour une démo,
deux éléments s'opposent à un déploiement en production tel quel :
1. Le tronquage systématique des réponses (problème de configuration, facile à corriger).
2. Les insertions de texte anormales, qui confirment une contamination du modèle/dataset déjà
   signalée par l'équipe précédente — un retraitement du dataset et un nouveau fine-tuning
   sont recommandés avant mise en production réelle.

**Voir le rapport de la filière CYBER pour l'analyse de sécurité complète et les preuves
détaillées de la compromission.**
