from flask import Flask, jsonify, request
from instagram_scraper import scrape_public_profile  # replace with actual filename

app = Flask(__name__)

@app.route('/instaData', methods=['GET'])
def get_insta_data():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Username parameter is required"}), 400

    data = scrape_public_profile(username)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
