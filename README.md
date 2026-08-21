# Radar missions — intérim graphisme

Centralise automatiquement les missions d'intérim en graphisme/design publiées
sur l'API officielle de France Travail, et les affiche sur une page web
simple, mise à jour chaque jour tout seul.

Aucun serveur à gérer : tout tourne sur GitHub (gratuit).

## Mise en place (15-20 min, à faire une seule fois)

### 1. Créer un compte développeur France Travail

1. Va sur https://francetravail.io et crée un compte.
2. Crée une nouvelle "application".
3. Dans les API à souscrire, active **"Offres d'emploi v2"**.
4. Note le **Identifiant client (client_id)** et le **Clé secrète (client_secret)**
   de ton application — tu en auras besoin à l'étape 3.

### 2. Créer le dépôt GitHub

1. Crée un compte GitHub si tu n'en as pas (gratuit) : https://github.com
2. Crée un nouveau dépôt (bouton "New repository"), par exemple nommé `radar-missions`.
3. Mets tous les fichiers de ce projet dedans (glisser-déposer sur GitHub
   fonctionne, ou via `git push` si tu es à l'aise avec).

### 3. Ajouter tes identifiants en secret

Dans le dépôt GitHub : **Settings → Secrets and variables → Actions**

- Onglet "Secrets" → "New repository secret" :
  - `FT_CLIENT_ID` → ton identifiant client
  - `FT_CLIENT_SECRET` → ta clé secrète
- (Optionnel) Onglet "Variables" → "New repository variable" :
  - `FT_DEPARTEMENT` → un code département (ex: `31`) si tu veux restreindre
    la recherche à une zone géographique. Laisse vide pour une recherche
    nationale.

### 4. Activer GitHub Pages

**Settings → Pages** → "Build and deployment" → Source : "Deploy from a branch"
→ Branche `main`, dossier `/docs` → Save.

Ta page sera disponible à une adresse du type :
`https://TON-PSEUDO.github.io/radar-missions/`

### 5. Lancer une première mise à jour manuelle

Onglet **Actions** du dépôt → workflow "Update job radar" → bouton
"Run workflow". Après ~30 secondes, `docs/data.json` est mis à jour et ta
page se remplit.

Ensuite, ça tourne tout seul chaque jour (voir l'horaire dans
`.github/workflows/update.yml`, modifiable si tu veux une autre fréquence).

## Personnaliser

- **Mots-clés recherchés** : liste `KEYWORDS` dans `scripts/fetch_offres.py`.
- **Zone géographique** : variable `FT_DEPARTEMENT` (voir étape 3).
- **Fréquence de mise à jour** : ligne `cron` dans
  `.github/workflows/update.yml` (format cron standard, en UTC).
- **Design de la page** : tout est dans `docs/index.html`, un seul fichier
  HTML/CSS/JS sans dépendance de build.

## Aller plus loin

Cette V1 se limite à France Travail parce que c'est la seule source avec une
API publique et gratuite adaptée à ce genre d'usage. Pour élargir à
Indeed, HelloWork, ou des agences d'intérim spécifiques, la voie la plus
propre (et conforme à leurs CGU) est de t'abonner à leurs alertes email avec
tes critères, puis d'ajouter un second script qui lit ces emails (IMAP) et
les fusionne dans le même `data.json`. Dis-moi si tu veux qu'on ajoute ce
module une fois que tu as identifié les 2-3 sites où tu reçois le plus
d'annonces pertinentes.





ID Client PAR_radarmissionsgraphism_b6865b18063508040be281cb7b1b987272b88a6a5e51a55ae90c41176b6a1fdd
Clé 05d91eb38d3ff213dd4f2f8bc0dae9e366e2b9310e064e622d66436d57a009d0