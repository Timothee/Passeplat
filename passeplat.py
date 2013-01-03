from flask import Flask, request, Response
import requests
app = Flask(__name__)
API_ROOT_URL = "https://api.heroku.com/"

# uses ~./netrc otherwise which might interfere with your requests
requests.defaults.defaults['trust_env'] = False

@app.route("/", methods=['GET', 'POST', 'DELETE', 'PUT'])
@app.route("/<path:path>", methods=['GET', 'POST', 'DELETE', 'PUT'])
def proxy(path=""):
	clean_headers = {}
	if 'Authorization' in request.headers:
		clean_headers['Authorization'] = request.headers['Authorization']
	if request.headers['Accept'] == 'application/xml':
		clean_headers['Accept'] = 'application/xml'
	else:
		clean_headers['Accept'] = 'application/json'

	# request.form is a Werkzeug MultiDict
	# we want to create a string
	clean_data = "" 
	for k, v in request.form.iteritems():
		clean_data += k + "=" + v + "&"

	# clean_headers['Content-Length'] = str(int(clean_headers['Content-Length']) + 4)
	print path
	print request.method
	print request.headers
	print clean_headers
	print request.form
	print clean_data

	response = requests.request(request.method, API_ROOT_URL + path, headers=clean_headers,
			data=clean_data)

	print response.headers
	return Response(response=response.text, status=response.headers['status'], headers=response.headers)


if __name__ == "__main__":
	app.debug = True
	app.run()

