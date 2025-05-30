from flask import Flask, jsonify, render_template 
from rdflib import Graph 
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/rdf_site")
def rdf_site():
    return render_template("rdf_site.html")

@app.route("/dbpedia_site")
def dbpedia_site():
    return render_template("dbpedia_site.html")

@app.route("/rdf_graph")
def rdf_graph():
    return render_template("rdf_graph.html")

@app.route('/api/castle')
def get_castle_data():
    g = Graph()
    g.parse("data/budatin.rdf")

    q = """
    SELECT ?label ?built WHERE {
      ?castle a <http://dbpedia.org/ontology/Castle> ;
              <http://www.w3.org/2000/01/rdf-schema#label> ?label ;
              <http://dbpedia.org/ontology/built> ?built .
    }
    """
    result = g.query(q)
    for row in result:
        return jsonify(label=str(row.label), built=str(row.built))


if __name__ == "__main__":
    app.run(debug=True)
