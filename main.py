from corpus import extraire_fables
from index import charger_index, construire_index, sauvegarder_index
from nettoyage import charger_mots_vides
from recherche import rechercher, scorer_resultats


def main():
    print("Chargement du moteur de recherche PyFind...")
    vides = charger_mots_vides()
    fables = extraire_fables("fable.txt")
    titres_fables = {f["id"]: f["titre"] for f in fables}

    index = charger_index()
    if not index:
        print("Construction de l'index...")
        index = construire_index(fables, vides)
        sauvegarder_index(index)

    print("\n--- PyFind est prêt ! ---")
    print("Exemples : loup, loup ET agneau, renard OU corbeau, lion SAUF rat")
    print("Tape 'quitter' pour arrêter.\n")

    while True:
        req = input("Recherche > ").strip()
        if req.lower() in ["quitter", "exit", "q"]:
            print("Au revoir !")
            break

        if not req:
            continue

        ids_trouves = rechercher(req, index, vides)
        if not ids_trouves:
            print("Aucun résultat trouvé.\n")
            continue

        termes_req = [m.lower() for m in req.split() if m.upper() not in ["ET", "OU", "SAUF"]]
        resultats_classes = scorer_resultats(ids_trouves, termes_req, index)

        print(f"\n{len(resultats_classes)} fable(s) trouvée(s) :")
        for f_id, score in resultats_classes:
            titre = titres_fables.get(f_id, "Inconnu")
            print(f"  - [Fable {f_id}] {titre} (score : {score})")
        print()


if __name__ == "__main__":
    main()