Passeplat
=========

Passeplat is a Flask-based Python app that (blindingly) proxies requests to a different root URL.

It's built and designed to work around a bug with the Heroku API[^1] that makes it unreliable to use the API with XMLHttpRequest (say in a browser extension) the same way you would with cURL.

Instead you would then do your XMLHttpRequest's against a Passeplat app, that will then do your API calls for you and send the responses back.

Ideally, you could just swap the API root URL for the root URL of your Passeplat instance in whatever library you use and everything would work fine. In any case, that's what I'm trying to do with the Heroku API.

One benefit is that if you work with a buggy API, you can still build your library the way it *should* be, and use Passeplat until the API is fixed.

-----

This is provided under the MIT License.

© 2012 Timothée Boucher, timotheeboucher.com


[^1]: basically, an XHR will send along the Heroku cookies and the Heroku API wrongly bases its response on if you're logged in or not, instead of using the API token for authentication.

