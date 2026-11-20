from nettoyage import charger_mots_vides, nettoyer_texte


def rechercher(requete, index, mots_vides):
    operateurs = [m for m in requete.split() if m.upper() in ["ET", "OU", "SAUF"]]
    termes = [m.lower() for m in requete.split() if m.upper() not in ["ET", "OU", "SAUF"]]
    
    if not termes:
        return set()

    resultat = set(index.get(termes[0], {}).keys())

    for i, op in enumerate(operateurs):
        if i + 1 < len(termes):
            fables_suivantes = set(index.get(termes[i + 1], {}).keys())
            if op.upper() == "ET":
                resultat = resultat.intersection(fables_suivantes)
            elif op.upper() == "OU":
                resultat = resultat.union(fables_suivantes)
            elif op.upper() == "SAUF":
                resultat = resultat.difference(fables_suivantes)

    return resultat


def scorer_resultats(fables_ids, termes, index):
    scores = {}
    for f_id in fables_ids:
        score_total = 0
        for mot in termes:
            if mot in index and f_id in index[mot]:
                score_total += len(index[mot][f_id])
        scores[f_id] = score_total
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)