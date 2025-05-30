from flask import Flask, jsonify, render_template
from rdflib import Graph
from dbpedia_fallback import get_dbpedia_abstract

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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

    # Fallback to DBpedia abstract if local RDF fails
    return jsonify(abstract=get_dbpedia_abstract())

if __name__ == "__main__":
    app.run(debug=True)
