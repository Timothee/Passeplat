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

if __name__ == '__main__':
    unittest.main()
