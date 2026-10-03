import sys
import os
import urllib.parse

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from server import app

    class VercelPathMiddleware:
        def __init__(self, wsgi_app):
            self.wsgi_app = wsgi_app

        def __call__(self, environ, start_response):
            # 1. Check for __vercel_path from vercel.json rewrite parameter
            qs_raw = environ.get('QUERY_STRING', '')
            if '__vercel_path' in qs_raw:
                qs = urllib.parse.parse_qs(qs_raw, keep_blank_values=True)
                if '__vercel_path' in qs:
                    vp = qs.pop('__vercel_path')[0]
                    # Restore remaining query parameters
                    environ['QUERY_STRING'] = urllib.parse.urlencode([(k, v) for k, vs in qs.items() for v in vs])
                    environ['PATH_INFO'] = '/' + vp.lstrip('/')
                    return self.wsgi_app(environ, start_response)

            # 2. Check for original URL headers from Vercel edge
            orig = (
                environ.get('HTTP_X_NOW_ORIGINAL_URL') or
                environ.get('HTTP_X_VERCEL_ORIGINAL_URL') or
                environ.get('HTTP_X_FORWARDED_PATH') or
                environ.get('HTTP_X_FORWARDED_URI') or
                environ.get('HTTP_X_ORIGINAL_URI')
            )
            if orig:
                if '?' in orig:
                    path_part, query_part = orig.split('?', 1)
                    environ['PATH_INFO'] = path_part
                    environ['QUERY_STRING'] = query_part
                else:
                    environ['PATH_INFO'] = orig
                return self.wsgi_app(environ, start_response)

            # 3. Fallback: normalize PATH_INFO
            path = environ.get('PATH_INFO', '')
            for prefix in ['/api/index.py', '/api/index']:
                if path.startswith(prefix):
                    rest = path[len(prefix):]
                    environ['PATH_INFO'] = rest if rest.startswith('/') else ('/' + rest if rest else '/')
                    break
            if not environ.get('PATH_INFO'):
                environ['PATH_INFO'] = '/'
            return self.wsgi_app(environ, start_response)

    app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

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
        <!DOCTYPE html>
        <html>
        <head><title>System Initializing | MediCare AI</title></head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 40px; background: #0f172a; color: #f87171; line-height: 1.6;">
            <div style="max-width: 800px; margin: 0 auto; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 30px;">
                <h2 style="margin-top: 0; color: #ef4444; display: flex; align-items: center; gap: 10px;">
                    ⚠️ System Diagnostic Alert
                </h2>
                <p style="color: #94a3b8;">The serverless environment encountered an initial loading issue:</p>
                <pre style="background: #0b1120; padding: 20px; border-radius: 8px; color: #fca5a5; overflow-x: auto; font-size: 13px;">{err_trace}</pre>
            </div>
        </body>
        </html>
        """, 200
