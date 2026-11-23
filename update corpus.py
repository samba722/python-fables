
#--- Etape 1 : Découpage

import re
from typing import Dict, List

def extraire_fables(chemin_fichier: str) -> List[Dict[str, any]]:
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        contenu = f.read()

    debut_marqueur = "*** START OF THE PROJECT GUTENBERG EBOOK"
    fin_marqueur = "*** END OF THE PROJECT GUTENBERG EBOOK"

    pos_debut = contenu.find(debut_marqueur)
    if pos_debut != -1:
        contenu = contenu[contenu.find("\n", pos_debut) + 1 :]

    pos_fin = contenu.find(fin_marqueur)
    if pos_fin != -1:
        contenu = contenu[:pos_fin]

    pos_livre1 = contenu.find("[Illustration: LIVRE 1.]")
    if pos_livre1 != -1:
        contenu = contenu[pos_livre1:]

    fables: List[Dict[str, any]] = []
    morceaux = contenu.split("\n\n")

    id_fable = 1
    titre_actuel = ""
    texte_actuel = []
    attend_titre = False

    for morceau in morceaux:
        ligne = morceau.strip()
        if not ligne:
            continue

        if ligne.startswith("[Illustration") or ligne.startswith("FIN DU LIVRE"):
            continue

        if re.match(r"^\[\d+\]", ligne):
            continue

        if re.fullmatch(r"[IVXLCDM]+", ligne):
            if titre_actuel and texte_actuel:
                fables.append(
                    {
                        "id": id_fable,
                        "titre": titre_actuel,
                        "texte": " ".join(texte_actuel),
                    }
                )
                id_fable += 1
                texte_actuel = []
            titre_actuel = ""
            attend_titre = True

        elif attend_titre:
            # On nettoie le point final et la casse (ex: "LE LOUP ET L'AGNEAU." -> "Le loup et l'agneau")
            titre_actuel = ligne.rstrip(".")
            attend_titre = False

        elif titre_actuel:
            # Ignorer d'éventuelles dédicaces en majuscules juste sous le titre (ex: "POUR M. LE DUC...")
            if not texte_actuel and ligne.isupper() and len(ligne) < 60:
                continue
            texte_actuel.append(ligne)

    if titre_actuel and texte_actuel:
        fables.append(
            {"id": id_fable, "titre": titre_actuel, "texte": " ".join(texte_actuel)}
        )

    return fables


if __name__ == "__main__":
    liste = extraire_fables("fable.txt")
    print(f"Fables extraites : {len(liste)}")
    if liste:
        print(liste[0])
