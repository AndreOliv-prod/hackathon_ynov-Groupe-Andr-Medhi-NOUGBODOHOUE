# Documentation de déploiement — INFRA

## Choix technique
Serveur d'inférence : **Ollama**, choisi pour sa simplicité de mise en place (clé en main),
sa gestion native de la quantization, et son API HTTP standard sur `localhost:11434`.

## Modèle
- Base : `phi3.5` (via Ollama)
- Configuration : `ollama_server/Modelfile`
- System prompt : assistant financier spécialisé TechCorp Industries

## Paramètres d'inférence
| Paramètre   | Valeur | Justification |
|-------------|--------|----------------|
| temperature | 0.3    | Réduit l'aléatoire — réponses factuelles et cohérentes attendues pour un assistant financier |
| top_p       | 0.9    | Valeur standard, garde une diversité raisonnable sans dérive |
| num_predict | 512    | Cohérent avec la limite utilisée dans la config Triton du dépôt |

## Commandes de déploiement
```powershell
ollama create techcorp-financial -f ollama_server/Modelfile
ollama run techcorp-financial "test"
```

## Vérification du serveur
Endpoint : `http://localhost:11434/api/generate`
Testé avec succès via `Invoke-RestMethod` (PowerShell) — réponse JSON reçue avec le champ `response` rempli.

## Accessibilité
Le serveur écoute sur `localhost:11434`. Pour un accès réseau (autre machine),
il faudrait définir `OLLAMA_HOST=0.0.0.0:11434` avant `ollama serve` — non nécessaire ici (tout tourne en local).
