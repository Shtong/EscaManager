---
type: initiative
title: "Gestion en ligne des adhésions et des adhérents du SCB Escalade"
sources: [_bmad-output/initiative-escamanager/entretien-initial.md]
companions: [_bmad-output/initiative-escamanager/glossaire.md]
after: []
risk: medium
---

# Gestion en ligne des adhésions et des adhérents du SCB Escalade

## Description

EscaManager est un ensemble d'outils pour la gestion quotidienne du SCB Escalade, club d'escalade à but non lucratif de Beaucouzé (près d'Angers), utilisés par l'équipe de gestion comme par les membres du club. Cette première partie livre un site web responsif couvrant : les comptes utilisateurs (création, connexion, données personnelles conformes au RGPD, permissions), la configuration des saisons et de leurs options tarifées, l'adhésion en ligne avec paiement (HelloAsso, et paiements hors ligne enregistrés à la main), la gestion de la liste des adhérents par saison avec export tableur, et la communication avec l'API de la fédération pour les licences. Tout le reste est volontairement hors périmètre, pour garder la première partie maîtrisée.

## Outcome

Pour l'équipe de gestion et les adhérents du SCB Escalade, une campagne d'adhésion se déroule entièrement en ligne, de la configuration de la saison à l'export de la liste des adhérents.

## Requirements

1. R1 (entretien initial, Gestion des utilisateurs) : un visiteur peut créer un compte, se connecter et se déconnecter ; la réussite se vérifie par l'accès à un espace réservé aux comptes connectés.
2. R2 (entretien initial, Gestion des utilisateurs) : un utilisateur connecté peut consulter et modifier ses données personnelles et demander leur effacement ; la conformité RGPD se vérifie par l'exercice effectif des droits d'accès, de rectification et d'effacement.
3. R3 (entretien initial, Gestion des utilisateurs — précisé le 24/10/2026) : les accès aux fonctionnalités sont régis par des permissions attribuables (type RBAC) ; les rôles nommés du club (président, trésorier, secrétaire, membre du CA, adhérent) sont des ensembles de permissions, jamais codés en dur ; la réussite se vérifie par le refus opposé à un compte dépourvu de la permission requise.
4. R4 (entretien initial, Gestion des saisons) : l'équipe de gestion peut configurer, pour chaque saison, les options proposées aux adhérents et leur prix ; la configuration s'observe dans ce que voit un adhérent pour cette saison.
5. R5 (entretien initial, Gestion des adhésions) : un visiteur peut adhérer pour une saison à venir ou en cours ; l'adhésion figure dans la liste des adhérents de cette saison.
6. R6 (entretien initial, Gestion des adhésions — précisé le 24/10/2026) : le prix de l'adhésion peut être payé en ligne, ou par un paiement hors ligne enregistré par l'équipe de gestion ; chaque paiement abouti est enregistré avec son moyen.
7. R7 (entretien initial, Gestion des membres) : l'équipe de gestion peut consulter et corriger la liste des adhérents de n'importe quelle saison ; la liste reflète les adhésions enregistrées pour la saison choisie.
8. R8 (entretien initial, Gestion des membres) : la liste des adhérents d'une saison peut être exportée dans un format tableur ouvrable par les tableurs courants.
9. R9 (décision du 24/10/2026, mineurs) : un représentant légal peut souscrire depuis son compte les adhésions de ses mineurs, avec consentement explicite pour leurs données ; l'adhésion du mineur figure dans la liste des adhérents de la saison, rattachée au compte du représentant.
10. R10 (entretien initial, Systèmes externes — confirmé pour la première partie le 24/10/2026) : l'application communique avec l'API de la fédération pour vérifier si une personne est déjà licenciée et y enregistrer un nouveau licencié ; la réussite se vérifie par l'état de la licence renvoyé par la fédération.

## Constraints

- Le livrable est un site web responsif, accessible à tous les utilisateurs (entretien initial, Livrable technique).
- Les dépendances techniques sont autant que possible des outils open-source et libres d'utilisation, le club étant à but non lucratif (entretien initial, Livrable technique).
- Tout logiciel requis (hébergement, base de données, etc.) doit être largement disponible chez les hébergeurs courants (entretien initial, Livrable technique).
- Le backend est divisé en deux parties : une bibliothèque de domaine lisant et écrivant les objets du domaine, et une application web qui l'utilise en exposant des pages HTML (des endpoints appelés en JavaScript pour actualiser les pages restent en option) ; une seule application consomme la bibliothèque dans cette première partie (entretien initial, Livrable technique).
- L'interface utilisateur est intégralement en français (entretien initial, Contexte).
- La documentation et le code (commentaires et symboles) sont écrits en français (entretien initial, Langue et maintenance).
- Le traitement des données personnelles est conforme au RGPD (entretien initial, Gestion des utilisateurs).
- L'identité visuelle prend pour point de départ le site actuel du club (escaladescb.fr), avec possibilité de modernisation (entretien initial, Contexte).
- Le paiement en ligne des adhésions passe par HelloAsso, gratuit pour les associations, qui tient l'encaissement et le reçu ; les paiements hors ligne (chèque, espèces) sont enregistrés manuellement par l'équipe de gestion (décision du 24/10/2026).

## Done when

- Une campagne complète se déroule dans l'outil : une saison est configurée (options, prix), un nouveau venu crée un compte, adhère et paie, l'équipe de gestion retrouve l'adhésion dans la liste de la saison et l'exporte en tableur.
- Un utilisateur peut consulter, corriger et faire effacer ses données personnelles sans intervention technique (RGPD).
- Une action de gestion est refusée à un compte sans la permission requise.
- L'interface est intégralement en français et utilisable sur mobile comme sur ordinateur.
- Les logiciels retenus sont disponibles chez les hébergeurs courants, et les dépendances sont autant que possible open-source et gratuites.
- Pour une adhésion, la licence fédérale est vérifiée depuis l'API de la fédération et un nouveau licencié y est enregistré.

## Boundaries

- Hors périmètre : toute fonctionnalité hors des quatre périmètres et des décisions du 24/10/2026 (intégration de la fédération) — événements, aspects financiers (comptabilité), activités générales du club, contenu du site public, boutique — n'est pas traitée dans cette première partie (entretien initial, Hors périmètre).
- Must not change : dans cette première partie, une seule application consomme la bibliothèque de domaine ; aucun autre client n'est livré (entretien initial, Livrable technique).
- Touch point : HelloAsso — encaissement du paiement en ligne des adhésions et reçu ; propriétaire : epic-adhesions-paiement.
- Touch point : hébergeur et base de données — déploiement du socle et des données ; propriétaire : epic-comptes-permissions.
- Chemin de bout en bout : comptes → saisons → adhésions et paiement → liste des adhérents → fédération ; chaque épic livre en production.

## References

- entretien initial — `_bmad-output/initiative-escamanager/entretien-initial.md` — sections Gestion des utilisateurs, Gestion des saisons, Gestion des adhésions, Gestion des membres, Hors périmètre, Livrable technique, Systèmes externes, Langue et maintenance.
- glossaire — `_bmad-output/initiative-escamanager/glossaire.md` (compagnon : correspondance des termes français/anglais du domaine).
- site web du club — https://escaladescb.fr/ — présentation du club (cours jeunes et adultes, permanences), inscriptions par saison, affiliation FFME, identité visuelle actuelle.

## Notes

- Open question: que propose concrètement la FFME comme API (existence, accès, champs, inscription des licenciés) ? À rechercher avant de raffiner l'épic fédération ; l'affiliation est confirmée, l'accès reste à établir.
- Decision: saison — une « saison » désigne l'année sportive du club (par ex. 2026/2027), pas l'année civile, confirmée le 24/10/2026.
- Decision: affiliation — le club est affilié à la FFME, confirmée le 24/10/2026.
- Decision: paiement — HelloAsso en ligne, paiements hors ligne enregistrés à la main, 24/10/2026.
- Decision: fédération — l'intégration à l'API de la fédération entre dans la première partie, 24/10/2026.
- Decision: rôles — permissions attribuables type RBAC ; les rôles nommés (président, trésorier, secrétaire, membre du CA, adhérent) sont des ensembles de permissions, quasiment jamais référencés dans le code, 24/10/2026.
- Decision: mineurs — adhésion portée par le compte du représentant légal, consentement explicite pour les données du mineur, 24/10/2026.
- Decision: découpe — cinq épics en ordre comptes → saisons → adhésions et paiement → liste / fédération (parallèles après l'épic 3), chaque épic livrée en production ; saisons en épic propre, 26/10/2026.
- Decision: liste et export sans état de licence fédérale — la licence vit dans le parcours d'adhésion (épic fédération), re-découpe si le club la veut à l'export, 26/10/2026.
- Decision: ossature d'architecture écrite maintenant (bmad-architecture), adoptée comme compagnon que les épics citent, 26/10/2026.
