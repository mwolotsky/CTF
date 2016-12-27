#!/usr/bin/python
import httplib
conn = httplib.HTTPConnection('127.0.0.1', 81)
conn.request("GET", "/login")
res = conn.getresponse()
print(res.read().decode("utf-8"))
conn.close()

