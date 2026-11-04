---
type: epic
title: "Adhésions et paiement"
parent: initiative-escamanager
covers: ["R5", "R6", "R9"]
sources: [_bmad-output/initiative-escamanager/initiative-escamanager.md]
companions: []
after: ["epic-comptes-permissions", "epic-saisons"]
refined: false
risk: high
---

# Adhésions et paiement

## Description

Un visiteur adhère à une saison à venir ou en cours en choisissant ses options, paie en ligne via HelloAsso ou par un paiement hors ligne qu'enregistre l'équipe de gestion, sur le site déployé ; un représentant légal souscrit depuis son compte pour ses mineurs.

## Outcome

Pour un futur adhérent, souscrire et payer une adhésion à une saison se fait entièrement en ligne, mineurs compris.

## Done when

- Un visiteur adhère à une saison à venir ou en cours, en choisissant ses options, sur le site déployé ; l'adhésion enregistrée se vérifie dans l'outil, sans dépendre de l'épic liste.
- Le paiement en ligne passe par HelloAsso ; un paiement hors ligne enregistré par l'équipe complète une adhésion.
- Un représentant légal souscrit pour ses mineurs, avec consentement explicite pour leurs données.

## Boundaries

- Appartient aux épics sœurs : la configuration de l'offre (epic-saisons), la liste et l'export (epic-liste-adherents), la licence fédérale (epic-federation).
- Must not change : l'encaissement en ligne reste chez HelloAsso ; l'outil n'encaisse pas lui-même.

## References

- parent — `_bmad-output/initiative-escamanager/initiative-escamanager.md`, section Requirements (R5, R6, R9).
- ossature d'architecture — `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`, section Invariants & Rules (AD-5 port HelloAsso, AD-9 entités, AD-13 prix notamment).
