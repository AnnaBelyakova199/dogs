curl -XPOST -H "Content-type: application/json" -d \
    '{"name": "Angry cat", "price": 0, "breed": "angry"}' \
    '127.0.0.1:5000/add'

curl -H "Content-type: application/json; charset=utf-8" '127.0.0.1:5000'
