# Travail différé — initiative EscaManager

- source_plan: `_bmad-output/initiative-escamanager/tickets/epic-comptes-permissions/tickets/story-socle-et-premiere-page-en-production-plan.md`
  summary: Mettre le socle en production sur Scalingo (compte, application, addon MySQL 8.4, variables d'environnement, déploiement, vérification à l'adresse de production, confirmation du prix du petit conteneur) puis créer le compte Brevo et relever ses identifiants SMTP.
  evidence: Décision humaine du 15/11/2026 au checkpoint du plan : réduire les coûts en n'hébergeant pas immédiatement — l'application s'exécute en local pendant les premières phases du développement ; le code livré reste neutre (AD-15), le déploiement ultérieur se fera sans le modifier.
- source_plan: `_bmad-output/initiative-escamanager/tickets/epic-comptes-permissions/tickets/story-comptes-inscription-confirmee-connexion-reinitialisation-plan.md`
  summary: Définir et imposer une politique de complexité des mots de passe (validateurs `AUTH_PASSWORD_VALIDATORS` en messages français directs, formulaire d'inscription appelant le pipeline de validation, la réinitialisation l'appelle déjà) sur les parcours d'inscription et de réinitialisation.
  evidence: Décision humaine du 25/11/2026 : aucune vérification de complexité n'existe aujourd'hui (`AUTH_PASSWORD_VALIDATORS` vide, `FormulaireInscription` n'appelle pas le pipeline, `SetPasswordForm` l'appelle sur une liste vide) ; le jeu de règles reste à choisir (longueur minimale, mots de passe courants, chiffres seuls, ressemblance au courriel) avant mise en production.
