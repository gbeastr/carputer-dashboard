from flask import Flask
from system import system_bp  # Import the Blueprint

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(system_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085)

