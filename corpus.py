#--- Etape 1 : Découpage

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

    fables: List[Dict[str, any]] = []
    morceaux = contenu.split("\n\n")

    id_fable = 1
    titre_actuel = "Introduction"
    texte_actuel = []

    for morceau in morceaux:
        ligne = morceau.strip()
        if not ligne:
            continue

        if len(ligne) < 60 and ("Fable" in ligne or ligne.istitle()):
            if texte_actuel:
                fables.append(
                    {
                        "id": id_fable,
                        "titre": titre_actuel,
                        "texte": " ".join(texte_actuel),
                    }
                )
                id_fable += 1
                texte_actuel = []
            titre_actuel = ligne
        else:
            texte_actuel.append(ligne)

    if texte_actuel:
        fables.append(
            {"id": id_fable, "titre": titre_actuel, "texte": " ".join(texte_actuel)}
        )

    return fables


if __name__ == "__main__":
    liste = extraire_fables("fable.txt")
    print(f"Fables extraites : {len(liste)}")
    if liste:
        print(liste[0])

