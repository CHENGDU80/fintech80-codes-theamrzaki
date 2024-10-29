# app.py
from flask import Flask, jsonify, request
import json

from agents import embed,completion
from backend.src import RAG,Dynamic_policy_speed,Dynamic_policy_aggressive
app = Flask(__name__)

@app.route("/index", methods=["POST"])
def index():
    data = request.get_json()
    #for testing
    docs = RAG.index_documents()
    results = RAG.index_documents(docs)
    if results:
        return jsonify({"len of index items:": str(len(results))}), 200
    else:
        return jsonify({"nothing was indexed"}), 400

@app.route("/search", methods=["POST"])
def search():
    # Get the search term from query parameters
    search_term = request.get_json()["term"]
    search_term = embed.embed(search_term)
    results = RAG.search_with_vector(search_term)
    results = completion.complete(str([r for r in results]))
    if search_term:
        return jsonify(json.loads( results.content))
    else:
        return jsonify({"error": "No search term provided"}), 400
    




@app.route("/speed", methods=["GET"])
def dynamicpolicy_speed():
    try:
        liabilities,premiums,speeds = Dynamic_policy_speed.speed_dynamic()
        return jsonify({"liabilities":liabilities,"premiums":premiums,"speeds":speeds}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    



@app.route("/aggressive", methods=["GET"])
def dynamicpolicy_aggressive():
    try:
        liabilities,premiums,ratios = Dynamic_policy_aggressive.agg_dynamic()
        return jsonify({"liabilities":liabilities,"premiums":premiums,"ratios":ratios}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP", "message": "API is working"}), 200



if __name__ == "__main__":
    app.run()  # Ensure the host and port are set

