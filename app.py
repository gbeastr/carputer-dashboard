from flask import Flask
from system import system_bp  # Import the system Blueprint

app = Flask(__name__)

# Register the system Blueprint
app.register_blueprint(system_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)

