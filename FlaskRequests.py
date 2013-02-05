from flask import Request, Response
class RqRequest(Request):
    def rq_headers(self):
        headers = {}
        for k, v in self.headers:
            if k.lower() != 'host': # httpbin goes kaput with localhost otherwise
                headers[k] = v
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

