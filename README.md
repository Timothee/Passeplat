Passeplat
=========

Passeplat is a Flask-based Python app that **proxies requests to a different
root URL**.

Let's say you run Passeplat at the URL `http://passeplat.example.com` with a
root URL set to `http://destination-url.com`. Calling
`http://passeplat.example.com/endpoint?k1=v1&k2=v2` will return whatever is
returned by `http://destination-url.com/endpoint?k1=v1&k2=v2`. It's doing so
blindingly so it *should* work with all HTTP method and parameters you're
throwing at it.

Its main use is to **work around issues you might have with some REST APIs**,
mainly in JavaScript apps and browser extensions. For example, the [Heroku
API](https://api-docs.heroku.com/) is unreliable when used with
`XMLHttpRequest`: the API backend will use your `heroku.com` cookie instead of
the API token sent with the request. This means that you can't manage multiple
Heroku accounts at once for instance. (on top of this, I've seen it respond with
a full HTML page, rather than JSON…)

Another example is **sites/APIs that don't send out [CORS
headers](http://www.w3.org/TR/cors/)**. When they don't, you can't use the API
from a JavaScript app and have to rely on your own backend. That's the case for
the [Dribbble API](http://dribbble.com/api) for example.

Instead you would do your `XMLHttpRequest`'s against a Passeplat instance, that
will forward your API calls to the root URL and send the responses back to you
with CORS headers.

Ideally, you could just swap the API root URL for the root URL of your Passeplat
instance in whatever library you use and everything should work fine. ("should"
because it's early on and not properly tested)

One benefit is that if you work with a buggy API, you can still build your
library the way it *should* be, and use Passeplat until the API is fixed.

How to use Passeplat
--

By default, you'd want to use it with Heroku. It can certainly work in other
environment though. I'll just leave that up to you to figure it out. :)

Once it runs on Heroku, you need to configure an environment variable named
`API_ROOT_URL` with the root URL you want to use (NB: full URL including
`http://` and trailing slash). For example, if you want to use the Heroku API, you set
`API_ROOT_URL` to `https://api.heroku.com/`.

You also need to configure an environment variable called `CORS_DOMAINS`. It's a
comma-separated list of domains that will be allowed cross-domain requests. It can
also be the wildcard `'*'`.

If `API_ROOT_URL` and `CORS_DOMAINS` are not set, the server will reply with a
500 error. So, even if you don't care which domains are calling your own server,
you still need to set a wildcard for `CORS_DOMAINS`.  (it could default to it of
course, but this way you'll make a conscious decision about it and it won't
leave it wide open)

Note that the CORS headers only limit user agents that will actually respect them (duh),
so typically requests made with `XMLHttpRequest`.  This is why a
request made with `curl` will still have access to the response text.

Once you have these two environment variables set up, you can make all your API
call against the root of your Passeplat instance.

Step-by-step instructions
--

In a terminal, you can run the following commands: (of course, adjust `yourappname` to yours and the CORS domains to what you want to use)

```bash
$ git clone git@github.com:Timothee/Passeplat.git
Cloning into 'Passeplat'...
remote: Counting objects: 97, done.
remote: Compressing objects: 100% (67/67), done.
remote: Total 97 (delta 51), reused 69 (delta 26)
Receiving objects: 100% (97/97), 16.34 KiB, done.
Resolving deltas: 100% (51/51), done.

$ cd Passeplat
$ heroku apps:create youappname
Creating yourappname… done, stack is cedar
http://yourappname.herokuapp.com/ | git@heroku.com:yourappname.git

$ git remote add heroku git@heroku.com:yourappname.git

$ git push heroku master
Counting objects: 97, done.
(skip)
-----> Launching... done, v4
       http://yourappname.herokuapp.com deployed to Heroku

To git@heroku.com:yourappname.git
 * [new branch]      master -> master

$ heroku config:set API_ROOT_URL=https://api.heroku.com/
Setting config vars and restarting yourappname... done, v5
API_ROOT_URL: https://api.heroku.com/

$ heroku config:set CORS_DOMAINS="*"
Setting config vars and restarting yourappname... done, v6
CORS_DOMAINS: *

$ heroku config
=== yourappname Config Vars
API_ROOT_URL: https://api.heroku.com/
CORS_DOMAINS: *

$ echo "yay!"
```


What kind of a name is that?
--
"Passeplat" is a French word that means kitchen hatch or dumb-waiter. It's
pronounced "pass-plah" (silent t).



--

This is provided under the MIT License.

© 2013 Timothée Boucher, timotheeboucher.com
