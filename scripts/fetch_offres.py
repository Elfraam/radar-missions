#!/usr/bin/env python3
"""
Job Radar — interroge l'API officielle France Travail (offres d'emploi v2)
et centralise les missions d'intérim correspondant à un profil de graphiste
freelance dans un fichier JSON consommé par docs/index.html.

Identifiants requis (variables d'environnement) :
  FT_CLIENT_ID
  FT_CLIENT_SECRET

Docs : https://francetravail.io/data/api/offres-emploi
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
import requests

TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

# --- Configuration -----------------------------------------------------
# Une requête par mot-clé : l'API ne fait pas de "OR" fiable sur motsCles,
# donc on multiplie les recherches puis on déduplique par id d'offre.
KEYWORDS = [
    "graphiste",
    "graphisme",
    "infographiste",
    "designer graphique",
    "direction artistique",
    "DAO PAO",
]

# Code contrat "MIS" = mission d'intérim (voir référentiel typesContrats de l'API)
TYPE_CONTRAT = "MIS"

# Filtre géographique optionnel. Laisser vide pour une recherche nationale.
# Exemples : "31" (Haute-Garonne), "75" (Paris)... voir référentiel des départements.
DEPARTEMENT = os.environ.get("FT_DEPARTEMENT", "").strip()

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "data.json")


def get_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def search_offres(token: str, mots_cles: str) -> list:
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "motsCles": mots_cles,
        "typeContrat": TYPE_CONTRAT,
        "sort": "1",  # tri par date de publication décroissante
        "range": "0-49",
    }
    if DEPARTEMENT:
        params["departement"] = DEPARTEMENT

    resp = requests.get(SEARCH_URL, headers=headers, params=params, timeout=30)
    # L'API renvoie 206 (Partial Content) quand il y a des résultats mais
    # que le range demandé ne couvre pas tout ; 204 quand aucun résultat.
    if resp.status_code == 204:
        return []
    resp.raise_for_status()
    return resp.json().get("resultats", [])


def normalize(offre: dict) -> dict:
    lieu = offre.get("lieuTravail", {}) or {}
    entreprise = offre.get("entreprise", {}) or {}
    salaire = offre.get("salaire", {}) or {}
    return {
        "id": offre.get("id"),
        "titre": offre.get("intitule"),
        "entreprise": entreprise.get("nom") or "Non précisé",
        "lieu": lieu.get("libelle") or "Non précisé",
        "date_publication": offre.get("dateCreation"),
        "description": (offre.get("description") or "")[:400],
        "salaire": salaire.get("libelle") or "",
        "duree_contrat": offre.get("dureeTravailLibelle") or "",
        "url": offre.get("origineOffre", {}).get("urlOrigine") or "",
    }


def main():
    client_id = os.environ.get("FT_CLIENT_ID")
    client_secret = os.environ.get("FT_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Erreur : FT_CLIENT_ID / FT_CLIENT_SECRET manquants.", file=sys.stderr)
        sys.exit(1)

    token = get_token(client_id, client_secret)

    all_offres = {}
    for kw in KEYWORDS:
        try:
            results = search_offres(token, kw)
        except requests.HTTPError as e:
            print(f"Avertissement : requête '{kw}' a échoué ({e}).", file=sys.stderr)
            continue
        for offre in results:
            norm = normalize(offre)
            if norm["id"]:
                all_offres[norm["id"]] = norm
        time.sleep(0.5)  # ménager l'API

    offres_list = sorted(
        all_offres.values(),
        key=lambda o: o.get("date_publication") or "",
        reverse=True,
    )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(offres_list),
        "offres": offres_list,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"{len(offres_list)} offres écrites dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
