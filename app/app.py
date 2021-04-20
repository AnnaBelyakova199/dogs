import json
from random import choice

from flask import request
from sqlalchemy.exc import DataError

from . import create_app, database
from .models import Dogs
from .serializers import dog_serializer


app = create_app()


@app.route('/', methods=['GET'])
def fetch():
    dogs = database.get_all(Dogs)
    if (len(dogs) == 0):
        return json.dumps("No dogs found"), 200

    all_dogs = list(map(dog_serializer, dogs))
    return json.dumps(all_dogs), 200


@app.route('/filter-by-color', methods=['GET'])
def filter_dogs():
    try:
        dogs = database.filter_by_color(Dogs, dict(request.args))
    except DataError:
        return json.dumps("Some error in filter options"), 400

    if (len(dogs) == 0):
        return json.dumps("No dogs found"), 200

    all_dogs = list(map(dog_serializer, dogs))
    return json.dumps(all_dogs), 200


@app.route('/add', methods=['POST'])
def add():
    post_data = request.get_json()
    attrs = ('name', 'price', 'breed', 'weight', 'color')
    data = {attr: post_data.get(attr, None)  for attr in attrs}
    for parent_attr in  ('father_id', 'mother_id'):
        try:
            data[parent_attr] = int(post_data.get(parent_attr, None))
        except:
            continue
    database.add_instance(Dogs, **data)
    return json.dumps("Added"), 200


@app.route('/remove/<dog_id>', methods=['DELETE'])
def remove(dog_id):
    database.delete_instance(Dogs, id=dog_id)
    return json.dumps("Deleted"), 200


@app.route('/edit/<dog_id>', methods=['PATCH'])
def edit(dog_id):
    data = request.get_json()
    new_price = data['price']
    database.edit_instance(Dogs, id=dog_id, price=new_price)
    return json.dumps("Edited"), 200


@app.route('/make-puppy', methods=['POST'])
def make_puppy():
    post_data = request.get_json()

    data = {attr: int(post_data.get(attr, 0))
            for attr in ('father_id', 'mother_id')}
    data = dict(filter(lambda item: bool(item[1]), data.items()))

    parents = database.filter_by_ids(Dogs, list(data.values()))
    if len(parents) < 2:
        return json.dumps("Mother and father required"), 400

    data['color'] = choice([parent.color for parent in parents])
    data['breed'] = '+'.join([parent.breed for parent in parents])

    database.add_instance(Dogs, **data)
    return json.dumps("Added"), 200
