# Etape 3 : Construire l'index

from collections import Counter
from typing import Dict, List
from corpus import extraire_fables
from nettoyage import charger_mots_vides, nettoyer_texte


def construire_index(fables: List[Dict[str, any]], mots_vides: set) -> Dict[str, Dict[int, List[int]]]:
    index: Dict[str, Dict[int, List[int]]] = {}

    for fable in fables:
        fable_id = fable["id"]
        mots = nettoyer_texte(fable["texte"], mots_vides)

        for position, mot in enumerate(mots):
            if mot not in index:
                index[mot] = {}
            if fable_id not in index[mot]:
                index[mot][fable_id] = []
            index[mot][fable_id].append(position)

    return index


def afficher_stats(fables: List[Dict[str, any]], index: Dict[str, Dict[int, List[int]]], mots_vides: set) -> None:
    print(f"Nombre de fables : {len(fables)}")
    print(f"Nombre de mots différents : {len(index)}")

    tous_les_mots = []
    for fable in fables:
        tous_les_mots.extend(nettoyer_texte(fable["texte"], mots_vides))

    compteur = Counter(tous_les_mots)
    print("Top 10 des mots les plus fréquents :")
    for mot, freq in compteur.most_common(10):
        print(f"  - {mot} : {freq} fois")


if __name__ == "__main__":
    fables = extraire_fables("fable.txt")
    vides = charger_mots_vides()
    index = construire_index(fables, vides)
    
    afficher_stats(fables, index, vides)
    print("\nExemple d'entrée d'index pour 'loup' :")
    if "loup" in index:
        print(index["loup"])