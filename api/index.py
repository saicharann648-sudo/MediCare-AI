import sys
import os

# Add root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from server import app
except Exception as e:
    import traceback
    from flask import Flask
    app = Flask(__name__)
    err_trace = traceback.format_exc()
    print("Vercel Startup Exception:", err_trace)
    
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return f"""
        <html>
        <body style="font-family: monospace; padding: 30px; background: #0f172a; color: #f87171;">
            <h2>⚠️ Vercel Function Startup Exception</h2>
            <pre style="background: #1e293b; padding: 20px; border-radius: 8px; color: #e2e8f0; overflow-x: auto;">{err_trace}</pre>
        </body>
        </html>
        """, 500
