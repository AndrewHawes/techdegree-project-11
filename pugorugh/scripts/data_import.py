import os
import json
import sys
import django


PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_data():
    from pugorugh.models import Dog
    filepath = os.path.join(PROJ_DIR, 'pugorugh', 'static', 'dog_details.json')

    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for dog in data:
            dog['image'] = 'images/dogs/' + dog['image_filename']
            del dog['image_filename']
            Dog.objects.create(**dog)

    print('load_data done.')


if __name__ == '__main__':
    sys.path.append(PROJ_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()

    # Assuming your serializer is named DogSerializer
    # has to be imported after django.setup()
    try:
        from pugorugh.serializers import DogSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly implemented '
            'DogSerializer class for this import to work.'
        )
    try:
        load_data()
    except Exception:
        raise
