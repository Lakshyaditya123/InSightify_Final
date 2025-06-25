# run.py - FIXED VERSION
from InSightify.db_server.Flask_app import app
# Import routes to register them with the app
from InSightify.db_server import app_routes

if __name__ == '__main__':
    # Add some debug information
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")

    app.run(debug=True, host="localhost", port=5490)
