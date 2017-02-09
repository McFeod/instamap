import requests

from settings import INSTAGRAM_TOKEN, PHOTO_COUNT, PAGE_SIZE


def photos_with_location(tag, count=PHOTO_COUNT):
    response = requests.get('https://api.instagram.com/v1/tags/{}/media/recent'.format(tag), params={
        'access_token': INSTAGRAM_TOKEN,
        'count': PAGE_SIZE
    }).json()
    while 'next_url' in response['pagination']:
        for pic in filter_response(response):
            yield pic
            count -= 1
            if count <= 0:
                return
        response = requests.get(response['pagination']['next_url']).json()


def filter_response(json):
    for x in json['data']:
        if x['location'] is not None:
            yield {
                'longitude': x['location']['longitude'],
                'latitude': x['location']['latitude'],
                'preview': x['images']['thumbnail']['url'],
                'image': x['images']['standard_resolution']['url']
            }
