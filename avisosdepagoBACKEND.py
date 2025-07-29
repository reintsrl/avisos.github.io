import os
from flask import Flask, request, jsonify
from google.cloud import bigquery
from flask_cors import CORS

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Reint/OneDrive/Documents/web/credencial.json"

app = Flask(__name__)
CORS(app)
client = bigquery.Client()

def parse_filter(param):
    """Parsea el parámetro, devuelve lista o None si es 'Todos' o vacío"""
    if not param or param == "Todos":
        return None
    # Divide por coma y elimina espacios
    valores = [v.strip() for v in param.split(",") if v.strip()]
    return valores if valores else None

def filtro_in(campo, valores):
    """Genera filtro SQL IN para lista de valores, escapando comillas simples"""
    safe_vals = [v.replace("'", "\\'") for v in valores]
    in_list = ", ".join(f"'{v}'" for v in safe_vals)
    return f"{campo} IN ({in_list})"

@app.route("/entidades", methods=["GET"])
def get_entidades():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    std = parse_filter(request.args.get("std"))
    prendarios = parse_filter(request.args.get("prendarios"))
    lugar = parse_filter(request.args.get("lugar"))
    team = parse_filter(request.args.get("team"))
    orden_monto = request.args.get("ordenMonto")
    orden_cantidad = request.args.get("ordenCantidad")

    filtros = [f"fechanorm BETWEEN '{desde}' AND '{hasta}'"]

    if std:
        filtros.append(filtro_in("santander", std))
    if prendarios:
        filtros.append(filtro_in("personas_crefpnomb", prendarios))
    if lugar:
        filtros.append(filtro_in("entidad", lugar))
    if team:
        filtros.append(filtro_in("team", team))

    where_clause = " AND ".join(filtros)
    print(orden_cantidad)
    orden = []
    if orden_cantidad in ("asc", "desc"):
        orden.append(f"cantidad {orden_cantidad}")
    elif orden_monto in ("asc", "desc"):
        orden.append(f"total_monto {orden_monto}")
    orden_clause = f"ORDER BY {', '.join(orden)}" if orden else "ORDER BY total_monto DESC"

    query = f"""
    SELECT carteraagrupada AS entidad,
           SUM(IFNULL(SAFE_CAST(monto AS NUMERIC), 0)) AS total_monto,
           COUNT(*) AS cantidad
    FROM `reint-413222.Data.cabeceraavisos`
    WHERE {where_clause}
    GROUP BY carteraagrupada
    {orden_clause}
    """

    df = client.query(query).to_dataframe()
    return jsonify(df.to_dict(orient="records"))

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    std = parse_filter(request.args.get("std"))
    prendarios = parse_filter(request.args.get("prendarios"))
    lugar = parse_filter(request.args.get("lugar"))
    team = parse_filter(request.args.get("team"))
    orden_monto = request.args.get("ordenMonto")
    orden_cantidad = request.args.get("ordenCantidad")

    filtros = [f"fechanorm BETWEEN '{desde}' AND '{hasta}'"]

    if std:
        filtros.append(filtro_in("santander", std))
    if prendarios:
        filtros.append(filtro_in("personas_crefpnomb", prendarios))
    if lugar:
        filtros.append(filtro_in("entidad", lugar))
    if team:
        filtros.append(filtro_in("team", team))

    where_clause = " AND ".join(filtros)

    orden = []
    if orden_monto in ("asc", "desc"):
        orden.append(f"total_monto {orden_monto}")
    if orden_cantidad in ("asc", "desc"):
        orden.append(f"cantidad {orden_cantidad}")
    orden_clause = f"ORDER BY {', '.join(orden)}" if orden else "ORDER BY total_monto DESC"

    query = f"""
    SELECT usuarios_17_cdescripcio AS usuario,
           SUM(CAST(monto AS NUMERIC)) AS total_monto,
           COUNT(*) AS cantidad
    FROM `reint-413222.Data.cabeceraavisos`
    WHERE {where_clause}
    GROUP BY usuarios_17_cdescripcio
    {orden_clause}
    """

    df = client.query(query).to_dataframe()
    return jsonify(df.to_dict(orient="records"))

@app.route("/team", methods=["GET"])
def get_team():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    std = parse_filter(request.args.get("std"))
    prendarios = parse_filter(request.args.get("prendarios"))
    lugar = parse_filter(request.args.get("lugar"))
    team_filtro = parse_filter(request.args.get("team"))

    filtros = [f"fechanorm BETWEEN '{desde}' AND '{hasta}'"]

    if std:
        filtros.append(filtro_in("santander", std))
    if prendarios:
        filtros.append(filtro_in("personas_crefpnomb", prendarios))
    if lugar:
        filtros.append(filtro_in("entidad", lugar))
    if team_filtro:
        filtros.append(filtro_in("team", team_filtro))

    where_clause = " AND ".join(filtros)

    query = f"""
        SELECT team,
               SUM(SAFE_CAST(monto AS NUMERIC)) AS total_monto,
               COUNT(*) AS cantidad
        FROM `reint-413222.Data.cabeceraavisos`
        WHERE {where_clause}
        GROUP BY team
        ORDER BY total_monto DESC
    """
    df = client.query(query).to_dataframe()
    return jsonify(df.to_dict(orient="records"))

@app.route("/sup", methods=["GET"])
def get_sup():
    desde = request.args.get("desde")
    hasta = request.args.get("hasta")
    std = parse_filter(request.args.get("std"))
    prendarios = parse_filter(request.args.get("prendarios"))
    lugar = parse_filter(request.args.get("lugar"))
    team_filtro = parse_filter(request.args.get("team"))

    filtros = [f"fechanorm BETWEEN '{desde}' AND '{hasta}'"]

    if std:
        filtros.append(filtro_in("santander", std))
    if prendarios:
        filtros.append(filtro_in("personas_crefpnomb", prendarios))
    if lugar:
        filtros.append(filtro_in("entidad", lugar))
    if team_filtro:
        filtros.append(filtro_in("team", team_filtro))

    where_clause = " AND ".join(filtros)

    query = f"""
        SELECT sup,
               SUM(SAFE_CAST(monto AS NUMERIC)) AS total_monto,
               COUNT(*) AS cantidad
        FROM `reint-413222.Data.cabeceraavisos`
        WHERE {where_clause}
        GROUP BY sup
        ORDER BY total_monto DESC
    """
    df = client.query(query).to_dataframe()
    return jsonify(df.to_dict(orient="records"))


@app.route("/filtros", methods=["GET"])
def get_filtros():
    query = """
        SELECT
          ARRAY_AGG(DISTINCT santander IGNORE NULLS) AS std,
          ARRAY_AGG(DISTINCT personas_crefpnomb IGNORE NULLS) AS prendarios,
          ARRAY_AGG(DISTINCT entidad IGNORE NULLS) AS lugar,
          ARRAY_AGG(DISTINCT team IGNORE NULLS) AS team
        FROM `reint-413222.Data.cabeceraavisos`
    """
    row = client.query(query).result().to_dataframe().iloc[0]
    return jsonify({
        "std": sorted(row["std"]),
        "prendarios": sorted(row["prendarios"]),
        "lugar": sorted(row["lugar"]),
        "team": sorted(row["team"]),
    })
#fecha gestion
@app.route("/fecha_reciente", methods=["GET"])
def get_fecha_reciente():
    query = """
        SELECT MAX(gestiones_dtfechhora) AS fecha_reciente
        FROM `reint-413222.Data.cabeceraavisos`
    """
    df = client.query(query).to_dataframe()

    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
