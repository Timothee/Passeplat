Passeplat
=========

Passeplat is a Flask-based Python app that **proxies requests to a different root URL**.

Let's say you run Passeplat at the URL `http://passeplat.example.com` with a root URL set to `http://destination-url.com`. Calling `http://passeplat.example.com/endpoint?k1=v1&k2=v2` will return whatever is returned by `http://destination-url.com/endpoint?k1=v1&k2=v2`. It's doing so blindingly so it *should* work with all HTTP method and parameters you're throwing at it.

Its main use is to **work around issues you might have with some REST APIs**, mainly in JavaScript apps and browser extensions. For example, the [Heroku API](https://api-docs.heroku.com/) is unreliable when used with `XMLHttpRequest`: the API backend will use your `heroku.com` cookie instead of the API token sent with the request. This means that you can't manage multiple Heroku accounts at once for instance. (on top of this, I've seen it respond with a full HTML page, rather than JSON…)

Another example is **sites/APIs that don't send out [CORS headers](http://www.w3.org/TR/cors/)**. When they don't, you can't use the API from a JavaScript app and have to rely on your own backend. That's the case for the [Dribbble API](http://dribbble.com/api) for example.

Instead you would do your `XMLHttpRequest`'s against a Passeplat instance, that will forward your API calls to the root URL and send the responses back to you with CORS headers.

Ideally, you could just swap the API root URL for the root URL of your Passeplat instance in whatever library you use and everything should work fine. ("should" because it's early on and not properly tested)

One benefit is that if you work with a buggy API, you can still build your library the way it *should* be, and use Passeplat until the API is fixed.

How to use Passeplat
--

By default, you'd want to use it with Heroku. It can certainly work in other environment though.

Once it runs on Heroku, you want to configure an environment variable named `API_ROOT_URL` with the root URL you want to use (NB: full URL including `http://`). You can now make all your API call against the root of your Passeplat instance.


What kind of a name is that?
--
"Passeplat" is a French word that means kitchen hatch or dumb-waiter. It's pronounced "pass-plah" (silent t).



--

This is provided under the MIT License.

© 2012 Timothée Boucher, timotheeboucher.com
