from flask import Request, Response
class RqRequest(Request):
    def rq_headers(self):
        headers = {}
        if 'Authorization' in self.headers:
            headers['Authorization'] = self.headers['Authorization']
        if self.headers['Accept'] == 'application/xml':
            headers['Accept'] = 'application/xml'
        else:
            headers['Accept'] = 'application/json'
        return self.headers

    # request.form is a Werkzeug MultiDict
    # we want to create a string
    def rq_data(self):
        data = ""
        for k, v in self.form.iteritems():
            data += k + "=" + v + "&"
        return data

    def rq_params(self):
        return self.args.to_dict()

