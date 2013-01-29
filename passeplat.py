import os
from flask import Flask, request, Response
import requests
from FlaskRequests import RqRequest

Flask.request_class = RqRequest

app = Flask(__name__)
API_ROOT_URL = os.environ.get("API_ROOT_URL")
CORS_DOMAIN = os.environ.get("CORS_DOMAIN", '*')


@app.route("/", methods=['GET', 'POST', 'DELETE', 'PUT'])
@app.route("/<path:path>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def proxy(path=""):
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
    response.headers['Access-Control-Allow-Origin'] = CORS_DOMAIN
    response.full_status = "%d %s" % (response.status_code, response.raw.reason)
    return Response(response=response.text,
                    status=response.full_status,
                    headers=response.headers)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

