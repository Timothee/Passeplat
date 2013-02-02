import os
import passeplat
import unittest


class PasseplatTestCase(unittest.TestCase):
    def setUp(self):
        passeplat.app.testing = True
        passeplat.app.config['API_ROOT_URL'] = "http://httpbin.org"
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

if __name__ == '__main__':
    unittest.main()
