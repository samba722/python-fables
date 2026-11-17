#--- Etape 2 : Nettoyage

from typing import List

def charger_mots_vides(chemin_fichier: str = "mots_vides.txt") -> set:
    mots_vides = set()
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            for ligne in f:
                mot = ligne.strip().lower()
                if mot:
                    mots_vides.add(mot)
    except FileNotFoundError:
        pass
    return mots_vides


def nettoyer_texte(texte: str, mots_vides: set) -> List[str]:    
    ponctuation = ".,;:!?()[]{}\"'-_«»"
    for p in ponctuation:
        texte = texte.replace(p, " ")

    mots_bruts = texte.lower().split()
    mots_propres = []

    for mot in mots_bruts:
        if mot not in mots_vides and len(mot) > 1:
            mots_propres.append(mot)

    return mots_propres


if __name__ == "__main__":
    vides = charger_mots_vides()
    exemple_texte = "Maître Corbeau, sur un arbre perché,"
    print(nettoyer_texte(exemple_texte, vides))