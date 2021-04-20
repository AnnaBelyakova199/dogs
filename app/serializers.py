def dog_serializer(dog):
    data = {
        "id": dog.id,
        "name": dog.name,
        "price": dog.price,
        "breed": dog.breed,
        "weight": dog.weight,
        "color": dog.color,
    }

    for parent in ('father', 'mother'):
        parent_obj = getattr(dog, parent, None)
        if parent_obj:
            data[parent] = dog_serializer(parent_obj)
    return data
