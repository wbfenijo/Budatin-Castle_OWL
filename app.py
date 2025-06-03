from flask import Flask, jsonify, render_template, url_for 
from rdflib import Graph, Namespace, URIRef
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    image_folder = os.path.join('static', 'images')
    images = os.listdir(image_folder)
    image_urls = [url_for('static', filename=f'images/{img}') for img in images if img[0] == 'b']
    return render_template('index.html', images=image_urls)

@app.route("/rdf_site")
def rdf_site():
    return render_template("rdf_site.html")  

@app.route("/dbpedia_site")
def dbpedia_site():
    return render_template("dbpedia_site.html")

@app.route("/rdf_graph")
def rdf_graph():
    return render_template("rdf_graph.html")

@app.route('/api/basic')
def get_castle_data():
    g = Graph()
    g.parse("data/budatin.rdf")
    data = {}
    
    q1 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?name ?lang ?year ?desc ?state ?lat ?lon
    WHERE {
        ex:BudatinCastle ex:hasName ?name ;
                         ex:hasYearOfBuild ?year ;
                         ex:hasDescription ?desc ;
                         ex:hasCurrentState ?state ;
                         ex:hasLatitude ?lat ;
                         ex:hasLongitude ?lon .
        BIND(lang(?name) AS ?lang)
        FILTER (lang(?desc) = "en")
        FILTER (lang(?state) = "en")
    }
    """

    names = {}
    for row in g.query(q1):
        names[str(row.lang)] = str(row.name)
        data["year"] = int(row.year)
        data["description"] = str(row.desc)
        data["state"] = str(row.state)
        data["lat"] = float(row.lat)
        data["lon"] = float(row.lon)
    data["name"] = names

    q2 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?type ?busNum ?station ?parking
    WHERE {
        ex:BudatinCastle ex:hasTransport ?transport .
        OPTIONAL {
            ?transport a ex:Bus ;
                       ex:number ?busNum ;
                       ex:BusStation ?station .
            BIND("bus" AS ?type)
        }
        OPTIONAL {
            ?transport a ex:Car ;
                       ex:Parking ?parking .
            BIND("car" AS ?type)
        }
    }
    """
    transport = []
    for row in g.query(q2):
        if row.type == "bus":
            transport.append({
                "type": "bus",
                "number": int(row.busNum),
                "station": str(row.station)
            })
        elif row.type == "car":
            transport.append({
                "type": "car",
                "parking": str(row.parking)
            })
    data["transport"] = transport

    q3 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?tour
    WHERE {
        ex:BudatinCastle ex:hasRoute ?tour .
    }
    """
    data["tours"] = [str(row.tour).split("#")[-1] for row in g.query(q3)]

    q4 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?fam ?name ?start ?end
    WHERE {
        ex:BudatinCastle ex:wasInhabitedBy ?fam .
        ?fam ex:hasFamilyName ?name ;
             ex:hasReignStart ?start ;
             ex:hasReignEnd ?end .
    }
    """
    families = []
    for row in g.query(q4):
        families.append({
            "name": str(row.name),
            "start": int(row.start),
            "end": int(row.end)
        })
    data["families"] = families

    q5 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?service ?name ?type
    WHERE {
        ex:BudatinCastle ex:hasService ?service .
        ?service ex:serviceName ?name ;
                 ex:serviceType ?type .
    }
    """
    services = []
    for row in g.query(q5):
        services.append({
            "name": str(row.name),
            "type": str(row.type)
        })
    data["services"] = services
    q6 = """
    PREFIX ex: <http://example.org/budatin#>
    SELECT ?price ?tour ?ticket ?amount
    WHERE {
        ?price a ex:Price ;
               ex:hasTourType ?tour ;
               ex:hasTicketType ?ticket ;
               ex:amount ?amount .
    }
    """
    prices = []
    for row in g.query(q6):
        prices.append({
            "tour": str(row.tour).split("#")[-1],
            "ticket": str(row.ticket).split("#")[-1],
            "amount": float(row.amount)
        })
    data["prices"] = prices
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
