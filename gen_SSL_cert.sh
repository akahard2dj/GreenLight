openssl genrsa -des3 -out greenlight.key 2048
openssl req -new -sha256 -key greenlight.key -out greenlight.csr
cp greenlight.key greenlight.key.origin
openssl rsa -in greenlight.key.origin -out greenlight.key
openssl x509 -sha256 -req -days 365 -in greenlight.csr -signkey greenlight.key -out greenlight.crt
