import os
from web.app import app

# For Vercel serverless deployment
def handler(request, **kwargs):
    return app(request.environ, lambda x, y: [])

# In app.py, modify your run section:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)