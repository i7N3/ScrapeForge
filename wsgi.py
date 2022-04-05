from main import app

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080, debug=False)  # Dev
    app.run(debug=True)  # Prod
