from flask import Flask, jsonify, request
from instagram_scraper import scrape_full_profile  # replace with actual filename

app = Flask(__name__)

@app.route('/instaData', methods=['GET'])
def get_insta_data():
    username = request.args.get('username')
    number_of_posts = request.args.get('number_of_posts', default=3)

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        number_of_posts = int(number_of_posts)
    except:
        return jsonify({"error": "number_of_posts must be an integer"}), 400

    data = scrape_full_profile(username, number_of_posts)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
