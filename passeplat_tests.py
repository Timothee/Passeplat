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


if __name__ == '__main__':
    unittest.main()
