from flask import Flask, request, jsonify
from handler.data_extraction import extract_pet_data

app = Flask(__name__)

@app.route('/api/demo/data-extraction/advanced', methods=['POST'])
def simple_data_extraction():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    text = request.json.get('text') if request.json is not None else None
    if not text:
        return jsonify({"error": "Missing 'text' field in request"}), 400
    
    try:
        pets = extract_pet_data(text)
        return jsonify(pets.model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/demo/data-extraction/simple', methods=['POST'])
def simple_data_extraction():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    text = request.json.get('text') if request.json is not None else None
    if not text:
        return jsonify({"error": "Missing 'text' field in request"}), 400
    
    try:
        pets = extract_pet_data(text)
        return jsonify(pets.model_dump())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
