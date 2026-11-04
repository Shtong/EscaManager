---
type: epic
title: "Comptes et permissions"
parent: initiative-escamanager
covers: ["R1", "R2", "R3"]
sources: [_bmad-output/initiative-escamanager/initiative-escamanager.md]
companions: []
after: []
refined: false
risk: medium
---

# Comptes et permissions

## Description

Épic d'ouverture : elle met en place le socle — bibliothèque de domaine, application web, CI, déploiement — et livre la gestion des comptes. Un visiteur crée un compte, se connecte et gère ses données personnelles conformément au RGPD ; les permissions régissent les accès aux fonctionnalités.

## Outcome

Pour chaque personne du club, un compte protégé régit ses accès, sur un socle déployé.

## Done when

- Un visiteur crée un compte, se connecte et se déconnecte, sur le site déployé.
- Un utilisateur consulte, corrige et fait effacer ses données personnelles sans intervention technique (RGPD).
- Une action de gestion est refusée à un compte sans la permission requise.
- Le socle — bibliothèque de domaine, application web, CI, déploiement — livre en production.

## Boundaries

- Appartient aux épics sœurs : la configuration des saisons (epic-saisons), l'adhésion et le paiement (epic-adhesions-paiement), la liste des adhérents (epic-liste-adherents), la licence fédérale (epic-federation).

## References

- parent — `_bmad-output/initiative-escamanager/initiative-escamanager.md`, section Requirements (R1–R3).
- ossature d'architecture — `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`, section Invariants & Rules (AD-11 effacement RGPD, AD-14 permissions notamment).
