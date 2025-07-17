from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/name', methods=['GET'])
def get_name():
    return jsonify({"name": "John Doe"})

@app.route('/instaData', methods=['GET'])
def get_insta_data():
    username = request.args.get('username')  # Get the 'username' parameter from the query string
    number_of_posts = request.args.get('number_of_posts', default=10)  # Default to 10 if not provided
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400
    return jsonify({"username": username, "message": f"Data for {username}", "posts": number_of_posts})



if __name__ == '__main__':
    app.run(debug=True)