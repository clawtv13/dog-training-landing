#!/bin/bash
echo "🔍 Testing workless.build..."
echo ""
echo "DNS Resolution:"
dig +short workless.build A
echo ""
echo "WWW CNAME:"
dig +short www.workless.build CNAME
echo ""
echo "HTTP Status:"
curl -sL -w "HTTP: %{http_code}\nFinal URL: %{url_effective}\n" -o /dev/null http://workless.build 2>&1 || echo "Not ready yet"
echo ""
echo "HTTPS Status:"
curl -sL -w "HTTP: %{http_code}\nSSL: %{ssl_verify_result}\n" -o /dev/null https://workless.build 2>&1 || echo "SSL not ready yet"
