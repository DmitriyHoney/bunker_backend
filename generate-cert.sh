openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

#https://github.com/lemoncode21/Fastapi-crud-sort-pagination/blob/master/backend/app/repository/person.py