from urlparse import urlparse
from flask import Request, Response

class RqRequest(Request):
    def rq_headers(self, root_url):
        headers = {}
        for k, v in self.headers:
            if k.lower() != 'host':
                headers[k] = v
            else:
                headers['Host'] = urlparse(root_url).netloc
        return headers

    # request.form is a Werkzeug MultiDict
    # we want to create a string
    def rq_data(self):
        data = ""
        for k, v in self.form.iteritems():
            data += k + "=" + v + "&"
        return data

    def rq_params(self):
        return self.args.to_dict()

