import unittest
import passeplat


class PasseplatTestCase(unittest.TestCase):
    def setUp(self):
        passeplat.app.testing = True
        passeplat.app.config['API_ROOT_URL'] = "http://httpbin.org/"
        passeplat.app.config['CORS_DOMAINS'] = "*"
        self.client = passeplat.app.test_client()

    def tearDown(self):
        pass

    def test_api_root_url_not_configured(self):
        passeplat.app.config['API_ROOT_URL'] = None
        response = self.client.get('/')
        assert response.status_code == 500
        assert response.status == "500 Root URL Not Configured"

    def test_cors_domains_not_configured(self):
        passeplat.app.config['CORS_DOMAINS'] = None
        response = self.client.get('/')
        assert response.status_code == 500
        assert response.status == "500 CORS Domains Not Configured"

    def test_200(self):
        response = self.client.get('/status/200')
        assert response.status_code == 200

    def test_404(self):
        response = self.client.get('/status/404')
        assert response.status_code == 404

    def test_methods(self):
        response = self.client.get('/get')
        assert response.status_code == 200
        response = self.client.post('/post')
        assert response.status_code == 200
        response = self.client.put('/put')
        assert response.status_code == 200
        response = self.client.delete('/delete')
        assert response.status_code == 200
        response = self.client.get('/post')
        assert response.status_code == 405
        response = self.client.post('/put')
        assert response.status_code == 405

    def test_redirects(self):
        response = self.client.get('/redirect/6')
        assert response.status_code == 200

    def test_cors(self):
        passeplat.app.config['CORS_DOMAINS'] = "*"
        response = self.client.get('/get')
        assert response.headers.get('Access-Control-Allow-Origin') == '*'
        response = self.client.get('/get', headers={'Origin': 'my.origin'})
        assert response.headers.get('Access-Control-Allow-Origin') == 'my.origin'

        passeplat.app.config['CORS_DOMAINS'] = "my.origin"
        response = self.client.get('/get')
        assert response.headers.get('Access-Control-Allow-Origin') == None
        response = self.client.get('/get', headers={'Origin': 'wrong.origin'})
        assert response.headers.get('Access-Control-Allow-Origin') == None
        response = self.client.get('/get', headers={'Origin': 'my.origin'})
        assert response.headers.get('Access-Control-Allow-Origin') == 'my.origin'

        response = self.client.open('/', method='OPTIONS')
        assert response.headers.get('Access-Control-Max-Age')
        assert response.headers.get('Access-Control-Allow-Credentials') == "true"
        assert response.headers.get('Access-Control-Allow-Methods') == ', '.join(passeplat.app.config['ALLOWED_HTTP_METHODS'])

    def test_response_headers(self):
        response = self.client.get('/response-headers?headerfoo=bar&headerbaz=buzz%20and%20some')
        assert response.headers.get('headerfoo') == 'bar'
        assert response.headers.get('headerbaz') == 'buzz and some'

    def test_request_headers(self):
        response = self.client.get('/get', headers={'foo': 'bar', 'baz': 'buzz and some'})
        assert '"Foo": "bar"' in response.data
        assert '"Baz": "buzz and some"' in response.data

    def test_basic_auth(self):
        response = self.client.get('/basic-auth/myuser/mypassword')
        assert response.status_code == 401


if __name__ == '__main__':
    unittest.main()
