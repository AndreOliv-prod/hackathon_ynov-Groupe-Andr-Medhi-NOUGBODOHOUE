# INFRA — Déploiement du serveur d'inférence

## Contenu
- `Modelfile` — configuration du modèle `techcorp-financial` (base `phi3.5`, system prompt, paramètres d'inférence)
- `deployment.md` — documentation technique du choix Ollama et des paramètres justifiés
- `screenshots/` — installation d'Ollama, création du modèle, vérification `ollama list`, test de l'API HTTP sur `localhost:11434`

## Résultat
Serveur d'inférence opérationnel, modèle `techcorp-financial` créé et testé avec succès via
l'API `/api/generate`.
