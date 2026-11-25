---
title: 'Comptes : inscription confirmée, connexion, réinitialisation'
type: feature
ticket: 2
created: '2026-11-25'
status: built
baseline_revision: 'b8b2868d32e6c1c4f3c9d4eebe96f4e80144cc15'
route: full
route_source: auto
risk: medium
review: quick
review_source: pinned
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['H:/EscaManager/_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md']
---

<frozen-after-approval reason="human-owned intent : do not modify unless human renegotiates">

## Intent

**Problem:** personne ne peut encore créer de compte : le socle n'a ni authentification, ni sessions, ni courriel, et le modèle `CompteDjango` est plat (courriel seul, sans mot de passe) ; tout le reste de l'épic se construit sur des comptes connectés.

**Approach:** activer `django.contrib.auth` avec un modèle utilisateur personnalisé : `AUTH_USER_MODEL = "comptes.CompteDjango"` (identifiant : le courriel, conformément au catalogue AD-9 qui donne `Compte` à l'app `comptes`). Parcours complet en gabarits français : inscription (compte créé inactif, courriel de confirmation à jeton signé valable 72 heures), confirmation, connexion, déconnexion, réinitialisation du mot de passe par courriel, espace personnel minimal. Toute écriture de compte passe par un service du domaine en transaction ; le hachage du mot de passe vit dans l'adaptateur.

**Decision (2026-11-25, renégociation humaine) :** une adresse inscrite mais jamais confirmée peut être réinscrite : le site remplace alors le mot de passe saisi et renvoie le courriel de confirmation, sans créer de doublon ni révéler l'état du compte ; le doublon d'un compte confirmé reste refusé sur le champ courriel ; corollaire adopté le même jour : la réinitialisation ne s'adresse qu'aux comptes confirmés, la réinscription est l'unique chemin de rétablissement d'un compte non confirmé.

## Boundaries & Constraints

**Always:** règles AD-1 à AD-15 (AD-1 pureté du domaine vérifiée par la garde, AD-2 lectures et écritures par le domaine, AD-6 rendu serveur sans JavaScript, AD-7 migrations seules sur MySQL utf8mb4, AD-10 routage et câblage dans `config`, AD-15 neutralité d'hébergement) ; symboles, apps et URLs en français snake_case ; textes français directs sans catalogue i18n ; secrets uniquement en variables d'environnement ; responsivité mobile.

**Never:** aucun envoi réel de courriel (backend console en local, Brevo différé au registre) ; pas de permissions ni de rôles (story 3), pas d'admin (story 4), pas de données personnelles au-delà du courriel ni d'effacement (stories 5 et 6) ; pas de nouvelle dépendance ; jamais SQLite ; pas de SQL brut ; migrations générées par `makemigrations`, jamais écrites à la main.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Inscription valide | POST courriel neuf + mot de passe deux fois | compte créé inactif, courriel de confirmation (jeton 72 h) envoyé, page d'avis | sans erreur |
| Inscription, doublon confirmé | POST courriel d'un compte actif | formulaire re-rendu, erreur sur le champ courriel | message français, aucun compte créé |
| Réinscription d'un compte non confirmé | POST courriel d'un compte inactif (jeton expiré ou perdu) | mot de passe remplacé, nouveau courriel de confirmation envoyé, page d'avis identique à une inscription neuve | aucune création de doublon, sans révéler l'état du compte |
| Confirmation valide | GET lien à jeton valide | compte activé, message, redirection vers connexion | sans erreur |
| Confirmation invalide | jeton expiré, altéré ou compte inconnu | page d'échec, lien vers la connexion et l'inscription | jamais d'exception non gérée |
| Connexion, compte actif | POST courriel + mot de passe corrects | session ouverte, redirection vers l'espace | sans erreur |
| Connexion, compte inactif | POST avant confirmation | refus, message invitant à confirmer | pas d'indice sur le mot de passe |
| Connexion, identifiants faux | POST courriel inconnu ou mot de passe erroné | message d'échec générique | sans révéler l'existence du compte |
| Espace sans session | GET /comptes/espace non connecté | redirection vers la connexion | sans erreur |
| Déconnexion | POST depuis l'espace | session terminée, redirection accueil | sans erreur |
| Demande de réinitialisation | POST courriel, connu ou non | réponse identique (neutre) ; courriel avec lien si connu et confirmé | jamais de divulgation d'existence |
| Réinitialisation complète | GET lien valide + POST nouveau mot de passe | mot de passe changé via service du domaine, redirection vers succès | jeton invalide ou expiré : erreur |

</frozen-after-approval>

## Code Map

- `application/config/settings.py` : INSTALLED_APPS minimale (L64-68, commentaire « ni auth » à réécrire), middleware sans session (L70-74), un seul context processor `request` (L79-90), `EMAIL_BACKEND` console (L132-135), chargeur env stdlib (L19-36). Tout s'étend ici, rien ne se déplace.
- `application/config/urls.py` : une route accueil ; les routes du parcours s'ajoutent ici (routage en `config`, AD-10).
- `application/config/composition.py` : `depot_comptes()` câble déjà le port ; inchangé.
- `application/comptes/modeles.py` : `CompteDjango` plat (courriel unique, L4-15), `db_table = "comptes_compte"` à conserver ; à faire évoluer en modèle utilisateur.
- `application/comptes/depots.py` : `DepotComptesDjango` n'implémente que `compter()` ; à étendre.
- `application/comptes/migrations/0001_initial.py` : table `comptes_compte` déjà appliquée ; l'évolution passe par une migration d'altération générée.
- `domaine/entites/compte.py` : `Compte` dataclass frozen, champ `courriel` seul, « sans aucune logique d'authentification » ; gagne l'état d'activation, jamais le mot de passe.
- `domaine/ports/depots.py` : port `DepotComptes` à une méthode `compter()` ; à étendre.
- `domaine/services/` : vide, prêt à recevoir les services d'écriture.
- `application/gabarits/base.html` : blocs `titre` et `contenu`, aucun bloc messages ni navigation ; à enrichir (AD-6, sans JavaScript).
- `tests/` : sans conftest ; pytest-django configuré dans `pyproject.toml` (L31-34) ; tests application avec `@pytest.mark.django_db` sur MySQL ; mypy strict sur `domaine/` (L47-51), couverture domaine ≥ 90 (L53-54).
- `.github/workflows/ci.yml` : deux jobs à garder verts, aucun changement prévu.
- `_bmad-output/initiative-escamanager/deferred-work.md` : Brevo/SMTP différé : le backend console reste.

## Tasks & Acceptance

**Execution:**
- [ ] `domaine/entites/compte.py` : `Compte` gagne `actif: bool` (faux par défaut) ; le mot de passe n'entre jamais dans l'entité
- [ ] `domaine/services/comptes.py` : créer : exceptions `CourrielDejaUtilise`, `CompteInconnu` ; services `inscrire_compte`, `confirmer_compte` (idempotent : un compte déjà actif ne fait rien), `reinitialiser_mot_de_passe` ; chaque écriture en transaction (`transaction.atomic` côté appelant de l'adaptateur)
- [ ] `domaine/ports/depots.py` : étendre `DepotComptes` : `existe`, `creer`, `trouver`, `activer`, `changer_mot_de_passe` ; le port transporte le mot de passe en clair au seul moment de l'appel, l'adaptateur hache
- [ ] `application/comptes/modeles.py` : `CompteDjango` hérite de `AbstractBaseUser` (sans `PermissionsMixin` : les permissions vivront dans le domaine, story 3) ; `USERNAME_FIELD = "courriel"`, `is_active` faux par défaut, manager `create_user`/`create_superuser`, `db_table` inchangé
- [ ] `application/comptes/migrations/0002_*.py` : migration d'altération générée par `makemigrations` (ajout `password`, `last_login`, `is_active`)
- [ ] `application/config/settings.py` : ajouter `contenttypes`, `auth`, `sessions` à INSTALLED_APPS ; middleware `SessionMiddleware`, `AuthenticationMiddleware` ; context processors `auth`, `messages` ; `AUTH_USER_MODEL`, `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` ; `DEFAULT_FROM_EMAIL` lisible depuis l'environnement (valeur par défaut neutre)
- [ ] `application/comptes/depots.py` : implémenter les nouvelles méthodes du port via l'ORM ; hachage par `set_password`, activation par sauvegarde
- [ ] `application/comptes/jetons.py` : créer : jeton de confirmation par `django.core.signing.TimestampSigner` (sel dédié, validité 72 heures) ; réinitialisation via `PasswordResetTokenGenerator` standard
- [ ] `application/comptes/formulaires.py` : créer : `FormulaireInscription` (courriel, mot de passe, confirmation), `FormulaireConnexion` (AuthenticationForm adapté, refus des comptes inactifs avec message dédié), `FormulaireDemandeReinitialisation`, `FormulaireNouveauMotDePasse` (SetPasswordForm dont la sauvegarde passe par le service du domaine) ; libellés et erreurs en français
- [ ] `application/comptes/vues.py` + `application/config/urls.py` : vues `inscription`, `confirmer_inscription`, `connexion` (LoginView), `deconnexion` (LogoutView, POST), les quatre vues de réinitialisation, `espace` (réservé aux connectés) ; routes françaises sous `/comptes/` ; courriels rendus depuis les gabarits
- [ ] `application/gabarits/` : `base.html` : bloc messages et navigation (selon connexion) ; gabarits `comptes/inscription.html`, `connexion.html`, `espace.html`, `reinitialisation/demande.html`, `envoyee.html`, `nouveau_mot_de_passe.html`, `terminee.html`, `confirmer_succes.html`, `confirmer_echec.html` et courriels `courriels/confirmation.html`, `reinitialisation.html` ; CSS responsif, sans JavaScript
- [ ] `tests/domaine/test_services_comptes.py` : faux dépôt en mémoire : inscription neuve et doublon, confirmation neuve, idempotente et inconnue, réinitialisation connue et inconnue
- [ ] `tests/application/test_comptes_parcours.py` : sur MySQL, backend locmem (`override_settings`) : parcours complet (inscription, courriel reçu, confirmation, connexion, espace, déconnexion, espace redirigé), connexion refusée avant confirmation, réinitialisation de bout en bout, réponse neutre sur courriel inconnu
- [ ] `README.md` : documenter le parcours local (courriels visibles en console), `DEFAULT_FROM_EMAIL`, et le rappel Brevo différé

**Acceptance Criteria:**
- Given l'application locale avec la base MySQL, when un visiteur s'inscrit, ouvre le lien du courriel de console, then son compte est actif, la connexion réussit et l'espace personnel s'affiche.
- Given un compte non confirmé, when il tente de se connecter, then le refus invite à confirmer sans autre indice.
- Given un visiteur connecté, when il demande une réinitialisation, suit le courriel et change son mot de passe, then le nouveau fonctionne et l'ancien est refusé.
- Given un visiteur déconnecté, when il ouvre `/comptes/espace`, then il est redirigé vers la connexion.
- Given un écran étroit (≈375 px) sans JavaScript, when il parcourt tout le parcours, then chaque page reste lisible et utilisable.
- Given la CI, when les deux jobs tournent, then tout reste vert : garde d'imports, mypy strict sur le domaine étendu, couverture ≥ 90, `makemigrations --check`, tests application sur MySQL.

## Implementation Notes

- 25/11/2026 — écarts corrigés après lecture du diff par l'orchestrateur : la confirmation réussie redirige vers la connexion avec un message (la matrice gelée exigeait « message, redirection vers connexion » ; l'implémenteur rendait une page dédiée `confirmer_succes.html`, supprimée) ; test du jeton de confirmation expiré ajouté (`tests/application/test_jetons_confirmation.py`, signature intacte, âge disqualifiant) ; test du lien de réinitialisation invalide ajouté ; expéditeur par défaut passé de `ne-pas-repondre@scb-escalade.fr` (domaine inventé) à `ne-pas-repondre@escaladescb.fr` (identité de départ du club).
- 25/11/2026 — réinscription d'un compte non confirmé (décision humaine du jour) : le formulaire ne refuse plus que les doublons de comptes confirmés ; la vue, sur `CourrielDejaUtilise` d'un compte inactif, remplace le mot de passe saisi via le service du domaine, renvoie le courriel de confirmation et répond comme une inscription neuve (aucune divulgation d'état). La matrice gelée porte la décision et la ligne scindée en deux. Choix d'implémentation : remplacer aussi le mot de passe (plutôt que l'ignorer) pour que tout ce que le visiteur saisit devienne vrai à la confirmation ; sans effet de prise de contrôle, l'activation exige toujours la boîte courriel.
- 25/11/2026 — ronde de rustines après la lentille `quick` : exceptions ORM traduites à l'adaptateur (`IntegrityError` devient `CourrielDejaUtilise`, `DoesNotExist` devient `CompteInconnu`, la double soumission simultanée rend l'erreur de champ au lieu d'un 500) ; la politique de réinscription vit entière dans `inscrire_compte` (la vue ne garde que l'erreur de champ et l'envoi, le formulaire ne lit plus le dépôt) ; `Deconnexion.get` mort supprimé ; `FormulaireNouveauMotDePasse.save` honore `commit` et retourne le compte ; commentaires d'`settings.py` reformulés au présent sans référence AD ; test ajouté : demande de réinitialisation pour une adresse inscrite non confirmée, neutre et sans courriel. Suivi de la ronde : `DepotComptes.existe` n'avait plus d'appelant, supprimé du port, de l'adaptateur et des tests de contrat.
- 25/11/2026 — piège préexistant corrigé par l'implémenteur dans `comptes/apps.py` : Django ne charge que `models.py`, or les modèles vivent dans `modeles.py` (nom français) ; sans la surcharge de `import_models`, le registre ignorait l'app et `makemigrations` restait aveugle. À répliquer dans les apps futures (saisons, adhésions, membres, fédération).
- 25/11/2026 — ajouts hors liste exigés par la matrice ou par Django : gabarit `comptes/inscription_envoyee.html` (la « page d'avis » de l'inscription), app et middleware `django.contrib.messages` (le plan citait le context processor et le bloc messages), `EMAIL_FIELD = "courriel"`, kwargs `uidb64`/`token` du protocole de réinitialisation.
- 25/11/2026 — les deux comptes de la base locale de développement ont reçu `password=''` lors de la migration d'altération : hachage inutilisable (`check_password` retourne faux), sans effet sur le parcours ni les tests.

## Plan Change Log

## Review Triage Log

- 25/11/2026, lentille `quick` (1re passe) — verdicts : 0 high / 2 medium / 5 low / 0 false / 0 maybe-false (une moitié de constat réfutée en note dans la ligne concernée).
  - `low` `patch` — `application/config/settings.py` : commentaire citant « AD-9 » au-dessus de `AUTH_USER_MODEL`, interdit dans les commentaires de code ; vérifié dans le diff. Correctif envoyé à l'implémenteur.
  - `low` `patch` — `application/config/settings.py` (commentaire INSTALLED_APPS « il viendra avec sa story dédiée ») : décrit l'avenir, interdit ; vérifié. La moitié « modeles.py docstring » du même constat est réfutée : « les permissions vivent dans le domaine » est au présent, il décrit l'état présent, pas le futur. Correctif envoyé à l'implémenteur pour la seule ligne fautive.
  - `medium` `patch` — `application/comptes/depots.py` + `domaine/services/comptes.py` : la lecture qui décide une écriture (`existe`/`trouver`) court hors de la transaction du port ; double soumission simultanée → `IntegrityError` non attrapée → 500 au lieu de l'erreur française du champ (la matrice exige le re-rendu du formulaire) ; ligne disparue entre `trouver` et `changer_mot_de_passe` → `DoesNotExist` fuie à travers le service. Vérifié dans le diff : `existe` sans transaction, `creer` atomique seul, la vue n'attrape que `CourrielDejaUtilise`. Correctif envoyé : traduire les exceptions ORM en exceptions du domaine à l'adaptateur.
  - `low` `patch` — `application/comptes/vues.py` (`Deconnexion.get`) : code mort vérifié contre les sources installées (`LogoutView.http_method_names = ["post", "options"]`, le 405 vient de la classe de base), docstring laissant croire que la surcharge fait le travail. Correctif envoyé : suppression.
  - `low` `patch` — `application/comptes/formulaires.py` (`FormulaireNouveauMotDePasse.save`) : ignore `commit`, retourne `None` alors que le contrat du parent (`SetPasswordForm.save`, source installée L527) retourne le compte ; `PasswordResetConfirmView.form_valid` utilise la valeur de retour uniquement dans la branche `post_reset_login`, désactivée ici, donc sans effet utilisateur aujourd'hui. Correctif envoyé : honorer `commit`, retourner le compte.
  - `low` `rejeté (corollaire de la décision humaine du 25/11)` — réinitialisation : le courriel ne part que pour les comptes actifs (`get_users` filtre `is_active: True`, source installée L448), la matrice gelée disait « si connu ». Vérifié. La décision humaine du jour fait de la réinscription le chemin unique de rétablissement d'un compte non confirmé : envoyez un lien de réinitialisation à un compte inactif produirait un mot de passe changé pour un compte toujours impossible à connecter, un second chemin concurrent. La ligne de matrice est amendée en « si connu et confirmé », corollaire consigné dans le bloc gelé ; test couvrant le cas (adresse inscrite non confirmée : réponse neutre, aucun courriel) envoyé à l'implémenteur.
  - `medium` `patch` — `application/comptes/formulaires.py` + `application/comptes/vues.py` + `domaine/services/comptes.py` : la politique de réinscription (doublon confirmé refusé, non confirmé remplacé et courriel renvoyé) vit dupliquée dans le formulaire et la vue, couches qui ne portent aucune règle métier selon les règles du dépôt, et `inscrire_compte` encode une règle plus stricte que le comportement réel : un second appelant du service obtiendrait le mauvais comportement, un changement de politique exigerait deux retouches coordonnées. Vérifié dans le diff. Correctif envoyé : la politique entière entre dans `inscrire_compte`, la vue ne garde que l'erreur de champ et l'envoi, le formulaire cesse de lire le dépôt, tests du domaine mis à jour.

## Design Notes

- `AbstractBaseUser` sans `PermissionsMixin` : AD-14 place les permissions dans le domaine et la story 3 bâtit la vérification sur ce vocabulaire ; le mécanisme des permissions de modèle Django ne servira pas, inutile de le migrer.
- Le jeton de confirmation embarque l'identifiant du compte signé (`TimestampSigner`, sel « confirmation-compte », 72 heures) : aucune table supplémentaire, aucune dépendance nouvelle.
- Réinitialisation : les vues et le générateur de jetons standard de Django sont conservés (éprouvés, sans JS) ; seule la sauvegarde du nouveau mot de passe est déroutée vers le service du domaine pour honorer la règle des écritures.
- Réponse neutre à la demande de réinitialisation pour un courriel inconnu : ne pas révéler les inscriptions.
- L'espace personnel est volontairement maigre (courriel, liens de parcours) : les stories 5 et 6 le rempliront ; la page existe dès maintenant pour matérialiser la réussite de connexion exigée par R1.

## Verification

**Commands:**
- `pytest tests/test_imports_domaine.py tests/domaine -q` : attendu : verts sans base, couverture du domaine ≥ 90
- `docker compose up -d --wait` puis `pytest tests/application -q` : attendu : verts sur MySQL 8.4
- `python manage.py makemigrations --check --dry-run` : attendu : aucune modification de schéma détectée
- `ruff check .` et `ruff format --check .` : attendu : propres
- `mypy` : attendu : strict sur `domaine/` incluant les nouveaux services
- `python manage.py runserver` puis parcours manuel complet (inscription, lien lu en console, confirmation, connexion, espace, déconnexion, réinitialisation) : attendu : chaque étape répond et les courriels apparaissent en console

**Manual checks (if no CLI):**
- Parcours complet lisible et utilisable à ≈375 px, sans JavaScript ; textes en français direct.
