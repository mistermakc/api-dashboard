from flask import Flask, render_template

# Initializing Flask app
app = Flask(__name__)

# Setting the secret key used by Flask to securely sign cookies and other data.
app.config['SECRET_KEY'] = 'DO_NOT_LOSE_THIS_KEY'

@app.route("/")
def catalogue():
    # Rendering the catalogue
    return render_template("catalogue.html"), 200

if __name__ == "__main__":
    app.run(debug=True)