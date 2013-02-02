import os
from flask import Flask, request, Response
import requests
from FlaskRequests import RqRequest

Flask.request_class = RqRequest

app = Flask(__name__)
API_ROOT_URL = os.environ.get('API_ROOT_URL')
CORS_DOMAINS = os.environ.get('CORS_DOMAINS')
ALLOWED_HTTP_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH', 'OPTIONS']


@app.route("/", methods=ALLOWED_HTTP_METHODS)
@app.route("/<path:path>", methods=ALLOWED_HTTP_METHODS)
def proxy(path=""):
    if not API_ROOT_URL:
        return Response(status="500 Root URL Not Configured")
    if not CORS_DOMAINS:
        return Response(status="500 CORS Domains Not Configured")

    s = requests.Session()
    s.trust_env = False
    s.max_redirects = 10 # just in case: could you DoS a server otherwise?

    print path
    print request.method
    print request.headers
    print request.rq_headers()
    print request.form
    print request.rq_data()

    response = s.request(method=request.method,
                         url=API_ROOT_URL + path,
                         headers=request.rq_headers(),
                         data=request.rq_data(),
                         params=request.rq_params())

    origin = request.headers.get('Origin')
    if CORS_DOMAINS == '*':
        response.headers['Access-Control-Allow-Origin'] = origin or '*'
    elif origin in CORS_DOMAINS.split(','):
        response.headers['Access-Control-Allow-Origin'] = origin

    if request.method == 'OPTIONS':
        response.headers['Access-Control-Max-Age'] = "1" # for debugging purposes for now
        response.headers['Accces-Control-Allow-Credentials'] = "true"
        response.headers['Access-Control-Allow-Methods'] = ', '.join(ALLOWED_HTTP_METHODS)

    response.full_status = "%d %s" % (response.status_code, response.raw.reason)

    return Response(response=response.text,
                    status=response.full_status,
                    headers=response.headers)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

