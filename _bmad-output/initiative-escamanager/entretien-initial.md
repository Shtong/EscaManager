# Entretien initial — 24/10/2026

Texte donné par l'utilisateur pour créer cette initiative, conservé tel quel (en anglais), réparti sous des titres pour que les lignes d'exigence (`R<n>`) puissent citer leur section.

## Contexte

This project will create a set of tools that will help manage the day to day activities of a french non-profit climbing club. It will be used both by the management team and the club members to manage things like subscriptions, events, financials, and the general activities of the club.

The club is located in France, meaning every user-facing text must be written in French.

Currently, the club's website is located here : https://escaladescb.fr/. It may be used to get a general idea of what the club is and the current visual identity, although we may modernize this identity during this project.

## Gestion des utilisateurs

- User management : account creation, log in, log out, personal data management (respecting the RGPD rules), permissions system

## Gestion des saisons

- Season management : configuring which options are available to members each year, and at what price

## Gestion des adhésions

- Subscription management : allow potential members to subscribe for an upcoming or current season, and pay the subscription price using a number of supported payment options

## Gestion des membres

- Member management : the management teams will be able to manage the list of subscribers for any given season, and export it as a spreadsheet

## Hors périmètre

Because a sports club management could cover a lot of things, we will focus for the time being on these features : *(liste ci-dessus)*.

Any feature that is not part of this list of broad features will not be considered in the first part of this project, to keep the scope under control.

## Livrable technique

Technically, this first version will be developed as a responsive website that can be accessed by all users. The technical dependencies will be open-source, free-to-use tools whenever possible. Any required software (hosting tools, databases, etc...) should be widely available in common hosting providers.

The backend will be divided into two parts :

- A domain library that may allow applications to read and write domain objects (however there will be only one such application in the first part of the project)
- A web application that will expose a web UI to manipulate the domain objects. It will expose HTML pages, and optionally endpoints called by Javascript to update the pages contents dynamically.

## Systèmes externes

During the project, the app will likely have to communicate with external systems, such as :

- The french climbing federation APIs, to check for existing climbers and register new ones
- A payment system used to pay for subscriptions - the chosen tool might be HelloAsso, although this choice is still open.

## Langue et maintenance

Because the tools will be maintained mostly by french-speaking people, the documentation and code elements (comments and symbols) should be written in French. Ideally, from this point on (after this message), all conversations between human agents and AI should happen in French, to avoid potential translation misunderstandings.
