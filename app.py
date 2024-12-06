from flask import Flask, render_template
from system import system_bp
from trip_computer import trip_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(system_bp)
app.register_blueprint(trip_bp)

@app.route("/")
def index():
    return render_template("index.html")  # Render the dashboard page

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

