from SPARQLWrapper import SPARQLWrapper, JSON

def get_dbpedia_abstract():
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery("""
        SELECT ?abstract WHERE {
          <http://dbpedia.org/resource/Budat%C3%ADn_Castle> dbo:abstract ?abstract .
          FILTER (lang(?abstract) = "en")
        }
    """)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result["results"]["bindings"][0]["abstract"]["value"]
