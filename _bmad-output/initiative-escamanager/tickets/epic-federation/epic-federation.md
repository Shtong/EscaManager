---
type: epic
title: "Fédération (FFME)"
parent: initiative-escamanager
covers: ["R10"]
sources: [_bmad-output/initiative-escamanager/initiative-escamanager.md]
companions: []
after: ["epic-adhesions-paiement"]
refined: false
risk: high
---

# Fédération (FFME)

## Description

L'adhésion vérifie auprès de l'API FFME si une personne est déjà licenciée et y enregistre un nouveau licencié, sur le site déployé.

## Outcome

Pour chaque adhésion, l'état de la licence FFME est connu et un nouveau licencié est enregistré auprès de la fédération.

## Done when

- Pour une adhésion, l'état de licence est vérifié depuis l'API FFME et un nouveau licencié y est enregistré, sur le site déployé.

## Boundaries

- Appartient aux épics sœurs : le parcours d'adhésion sans licence (epic-adhesions-paiement), la liste des adhérents sans état de licence (epic-liste-adherents).

## References

- parent — `_bmad-output/initiative-escamanager/initiative-escamanager.md`, section Requirements (R10).
- ossature d'architecture — `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`, section Invariants & Rules (AD-5 bouchon FFME, AD-10 composition notamment).
