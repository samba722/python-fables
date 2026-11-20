from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from corpus import extraire_fables
from index import charger_index, construire_index, sauvegarder_index
from nettoyage import charger_mots_vides
from recherche import rechercher, scorer_resultats

vides = charger_mots_vides()
fables = extraire_fables("fable.txt")
titres_fables = {f["id"]: f["titre"] for f in fables}
textes_fables = {f["id"]: f["texte"] for f in fables}

index = charger_index()
if not index:
    index = construire_index(fables, vides)
    sauvegarder_index(index)


def generer_page(requete="", resultats_html=""):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>PyFind - Fables de La Fontaine</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f4f4f9; color: #333; }}
        h1 {{ text-align: center; color: #2c3e50; }}
        form {{ display: flex; gap: 10px; margin-bottom: 30px; }}
        input[type="text"] {{ flex: 1; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; }}
        button {{ padding: 12px 20px; font-size: 16px; background: #2c3e50; color: white; border: none; border-radius: 5px; cursor: pointer; }}
        button:hover {{ background: #34495e; }}
        .fable {{ background: white; padding: 15px 20px; margin-bottom: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .fable h3 {{ margin: 0 0 10px 0; color: #2980b9; }}
        .score {{ font-size: 13px; color: #7f8c8d; font-weight: normal; }}
        .texte {{ white-space: pre-line; line-height: 1.5; }}
    </style>
</head>
<body>
    <h1>Site Fables</h1>
    <form method="GET" action="/">
        <input type="text" name="q" value="{requete}" placeholder="Ex: loup ET agneau, renard OU corbeau, lion SAUF rat..." required>
        <button type="submit">Rechercher</button>
    </form>
    <div>{resultats_html}</div>
</body>
</html>"""


def gerer_requete(handler):
    url = urlparse(handler.path)
    params = parse_qs(url.query)
    req = params.get("q", [""])[0].strip()

    resultats_html = ""
    if req:
        ids_trouves = rechercher(req, index, vides)
        if not ids_trouves:
            resultats_html = "<p>Aucun résultat trouvé.</p>"
        else:
            termes = [m.lower() for m in req.split() if m.upper() not in ["ET", "OU", "SAUF"]]
            classes = scorer_resultats(ids_trouves, termes, index)
            resultats_html = f"<p><strong>{len(classes)} fable(s) trouvée(s) :</strong></p>"
            for f_id, score in classes:
                titre = titres_fables.get(f_id, "Inconnu")
                texte = textes_fables.get(f_id, "")
                resultats_html += f"""
                <div class="fable">
                    <h3>Fable {f_id} : {titre} <span class="score">(Score : {score})</span></h3>
                    <div class="texte">{texte}</div>
                </div>"""

    html = generer_page(req, resultats_html)
    handler.send_response(200)
    handler.send_header("Content-type", "text/html; charset=utf-8")
    handler.end_headers()
    handler.wfile.write(html.encode("utf-8"))


Handler = type("Handler", (BaseHTTPRequestHandler,), {"do_GET": gerer_requete})

if __name__ == "__main__":
    serveur = HTTPServer(("localhost", 8000), Handler)
    print("Serveur lancé sur http://localhost:8000 (Ctrl+C pour arrêter)")
    serveur.serve_forever()