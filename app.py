from flask import Flask, jsonify, render_template, url_for 
from rdflib import Graph 
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

    q = """
    SELECT ?label ?built WHERE {
    <http://example.org/budatin#BudatinCastle> 
        <http://example.org/budatin#hasName> ?label ;
        <http://example.org/budatin#hasYearOfBuild> ?built .
    FILTER (lang(?label) = "en")
}
    """
    query_result = g.query(q)
    results = []
    for row in query_result:
        result = {}
        for var, val in zip(query_result.vars, row):
            result[str(var)] = str(val)
            
        results.append(result)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
