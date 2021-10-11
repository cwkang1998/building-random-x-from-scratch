# A simple web server

[Referenced tutorial](http://aosabook.org/en/500L/a-simple-web-server.html)

## Notes

To run the simple web server, simply do:

```bash
python main.py
```

Note that for listing, which shows `main.py` as one of the executable files for cgi, it'll not work when you call it. Note that the implementation for cgi in the is extremely simple and insecure, so no using it in production.

## Lesson learnt
Quite a interesting simple tutorial on http modules in python. The tutorial was written for python 2, but with some tweaks it does work for python 3 as well.

- Refresher on http and tcp
- About the http.server module
- Learnt a bit about the CGI protocol