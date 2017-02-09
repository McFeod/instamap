import requests

from settings import INSTAGRAM_TOKEN, PHOTO_COUNT, PAGE_SIZE


# def get_tags(query):
#     response = requests.get('https://api.instagram.com/v1/tags/search', params={
#         'access_token': INSTAGRAM_TOKEN,
#         'q': query,
#         'count': MAX_COUNT
#     })
#     return [x['name'] for x in response.json()['data']]


def get_photos_with_location(tag, count=PHOTO_COUNT):
    response = requests.get('https://api.instagram.com/v1/tags/{}/media/recent'.format(tag), params={
        'access_token': INSTAGRAM_TOKEN,
        'count': PAGE_SIZE
    }).json()
    pictures = []
    while len(pictures) < count:
        pictures += filter_response(response)
        if 'next_url' in response['pagination']:
            response = requests.get(response['pagination']['next_url']).json()
        else:
            break
    return pictures[:count]


def filter_response(json):
    return [{
                'longitude': x['location']['longitude'],
                'latitude': x['location']['latitude'],
                'preview': x['images']['thumbnail']['url'],
                'image': x['images']['standard_resolution']['url'],
                'height': x['images']['standard_resolution']['height']
            } for x in json['data'] if x['location'] is not None]