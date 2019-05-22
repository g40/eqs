# eqs

Python powered in-browser SPA using Brython, w2ui and jstree.

For an old skool browsing experience, clone the repo and then

`python -m http.server --directory=/path/to/html`

or, using Electron (assuming it is in the path)

`electron .`

In order to minimize expectations, it should be made clear that this application simly shows how to glue various existing UI libraries together using Python that is transpiled to Javascript in the browser. Calling out to remote resources demonstrated via a Python connected websocket. 

With any luck may persuade and/or inspire the reader to try a better way to work the web.

A very big hand to the good folk who provided the following:

1. https://github.com/brython-dev/brython
2. https://github.com/vakata/jstree
3. https://github.com/vitmalina/w2ui
