echo "GET /select.cgi/?txt=a" > /tmp/input
nc 127.0.0.1 81 < /tmp/input
echo "GET /authed/a.txt" > /tmp/input
nc 127.0.0.1 81 < /tmp/input
#echo "import pty; pty.spawn('/bin/bash')" > /tmp/asdf.py
#python /tmp/asdf.py
echo "HI"
