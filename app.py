from flask import Flask
from system import system_bp  # Import the system Blueprint
from trip_computer import trip_bp  # Import the trip_computer Blueprint

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(system_bp)
app.register_blueprint(trip_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

