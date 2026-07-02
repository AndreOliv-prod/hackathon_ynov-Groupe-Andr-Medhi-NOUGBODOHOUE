# CYBER — Audit de sécurité

## Contenu
- `rapport_audit.md` — rapport complet : findings, preuves, criticité, recommandations
- `test_robustness.py` / `robustness_results.md` — tests de robustesse du modèle déployé (trigger backdoor, prompt injection, extraction de system prompt, demande de credentials)
- `screenshots/` — preuves visuelles des tests exécutés

## Résultat
Backdoor documentée dans les logs de l'équipe précédente (intention avérée d'espionnage
industriel), dataset contaminé confirmé, mais **aucun déclenchement actif observé** lors des
tests de robustesse sur le modèle actuellement déployé. Recommandation : ne pas déployer en
production sans ré-entraînement sur données assainies et revue de sécurité externe.
