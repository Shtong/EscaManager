---
type: epic
title: "Comptes et permissions"
parent: initiative-escamanager
covers: ["R1", "R2", "R3"]
sources: [_bmad-output/initiative-escamanager/initiative-escamanager.md]
companions: [_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md]
after: []
refined: true
risk: medium
status: 'in-progress'
---

# Comptes et permissions

## Description

Épic d'ouverture : elle met en place le socle — bibliothèque de domaine, application web, CI, déploiement — et livre la gestion des comptes. Un visiteur crée un compte, se connecte et gère ses données personnelles conformément au RGPD ; les permissions régissent les accès aux fonctionnalités.

## Outcome

Pour chaque personne du club, un compte protégé régit ses accès, sur un socle déployé.

## Requirements

1. R1 (parent R1) : un visiteur peut créer un compte, se connecter et se déconnecter ; l'adresse de courriel est confirmée par message et la réinitialisation du mot de passe fonctionne par courriel ; la réussite se vérifie par l'accès à un espace réservé aux comptes connectés.
2. R2 (parent R2) : un utilisateur connecté peut consulter et modifier ses données personnelles et demander leur effacement ; à l'effacement, le compte et les données de connexion sont supprimés et l'historique subsistant est anonymisé (décision du 04/11/2026) ; l'effacement passe par l'orchestrateur du domaine (AD-11), auquel les entités des épics suivantes se raccordent ; la conformité se vérifie par l'exercice effectif des droits d'accès, de rectification et d'effacement.
3. R3 (parent R3) : les accès aux fonctionnalités sont régis par des permissions attribuables (type RBAC) ; six rôles sont semés au premier démarrage (président, trésorier, secrétaire, membre du CA, adhérent, administrateur technique), en données, jamais codés en dur (décision du 04/11/2026) ; la réussite se vérifie par le refus opposé à un compte dépourvu de la permission requise.
4. R4 (initiative, Livrable technique) : le socle est en place : bibliothèque de domaine (paquet pur), application web Django avec l'admin habillée (décision du 04/11/2026), CI GitHub Actions, déploiement en production ; la réussite se vérifie par un déploiement fonctionnel et une sauvegarde restaurée à blanc.
5. R5 (initiative, Livrable technique ; décision du 04/11/2026) : l'application reste hébergeable sur toute infrastructure exécutant Python : piste de démarrage Scalingo, aucune dépendance à un hébergeur (WSGI standard, variables d'environnement, aucune fonction propre à un PaaS) ; la réussite se vérifie par un déploiement sans modification du code selon l'hébergeur.

## Constraints

- Site web responsif, accessible sur mobile comme sur ordinateur (initiative, Livrable technique).
- Interface, documentation et code en français (initiative, Contexte et Langue et maintenance).
- Traitement des données personnelles conforme au RGPD (initiative, Gestion des utilisateurs).
- Dépendances open-source et gratuites ; hébergeable chez les hébergeurs courants, sans dépendance à un hébergeur (initiative, Livrable technique ; décision du 04/11/2026).
- Les quinze règles (AD-1 à AD-15) de l'ossature d'architecture lient toutes les stories (compagnon, adopté le 04/11/2026).

## Done when

- Un visiteur crée un compte, se connecte et se déconnecte, sur le site déployé ; le courriel de confirmation et la réinitialisation fonctionnent.
- Un utilisateur consulte, corrige et fait effacer ses données personnelles sans intervention technique (RGPD) ; l'historique subsistant est anonymisé.
- Une action de gestion est refusée à un compte sans la permission requise ; les six rôles sont semés au premier démarrage.
- L'admin Django, habillée et en français, permet à l'équipe de gestion de travailler.
- Le socle (bibliothèque de domaine, application web, CI, déploiement) livre en production ; une sauvegarde se restaure à blanc.
- Tout le parcours — comptes, espace personnel, admin — est utilisable sur mobile comme sur ordinateur.

## Boundaries

- Appartient aux épics sœurs : la configuration des saisons (epic-saisons), l'adhésion et le paiement (epic-adhesions-paiement), la liste des adhérents (epic-liste-adherents), la licence fédérale (epic-federation).

## References

- parent — `_bmad-output/initiative-escamanager/initiative-escamanager.md`, section Requirements (R1–R3).
- ossature d'architecture — `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`, section Invariants & Rules (AD-11 effacement RGPD, AD-14 permissions notamment).

## Notes

- Open question: durées de conservation exactes des lignes anonymisées (obligations comptables de l'association) : à confirmer avec la trésorerie du club.
- Decision: effacement RGPD par anonymisation (compte supprimé, historique anonymisé), 04/11/2026.
- Decision: six rôles semés au premier démarrage, 04/11/2026.
- Decision: écrans de gestion dans l'admin Django habillée, parcours adhérent en gabarits dédiés, 04/11/2026.
- Decision: hébergeur neutre, piste de démarrage Scalingo, 04/11/2026.
- Decision: balle traceuse : l'entrée 1 (socle et première page en production), 09/11/2026.
- Decision: séquencement (09/11/2026) : l'effacement (6) attend les données personnelles (5) parce que la demande part de la page des données ; les permissions précèdent l'admin (3→4) ; la sauvegarde (7) ne dépend que du socle et peut avancer librement après lui ; le balayage (8) ferme.
- Decision: courriels — Brevo pour l'envoi transactionnel (offre gratuite vérifiée), identifiants en variables d'environnement, 12/11/2026.
- Decision: ordre du tableau confirmé tel quel, 15/11/2026.
- Decision: ensembles de permissions des six rôles écrits à la volée dans la story 3, jeu initial simple et modifiable dans l'admin, 15/11/2026.
- Decision: dépôt GitHub public, 15/11/2026.
