from datetime import datetime
from .Databased import Base


class EditParse:

    def __init__(self):
        self.context_aspect = dict()
        self.context_related_place = dict()
        self.context_reviews = dict()
        self.context_all = dict()
        self.title_text = list()
        self.now_related_place = list()
        self.title_related_place = list()
        self.now_aspect = list()
        self.title_aspect = list()
        self.count_vote = int
        self.rating = float
        self.count_text = int
        self.address = ''
        self.coordinates = ''
        self.now_date_text = list()
        self.title = ''
        self.aspect_text = list()
        self.aspect_count = list()
        self.aspect_positive = list()
        self.aspect_neutral = list()
        self.aspect_negative = list()
        self.related_place_name = list()
        self.related_place_rating = list()
        self.related_place_coordinates = list()
        self.reviews_text = list()
        self.reviews_business_text = list()
        self.reviews_business_date = list()
        self.reviews_rating = list()
        self.reviews_date = list()
        self.reviews_like = list()
        self.reviews_dislike = list()
        self.coordinates_aspect = list()
        self.coordinates_related_place = list()
        self.coordinates_text = list()
        self.now = datetime.now().strftime("%Y-%m-%d")

    def Edit(self, content, project):

        try:
            self.try_edit(content)
        except Exception as ex:
            self.ex_edit(content)

        base = Base()
        base.create_new_items(table=f'{project}_all', context=self.out['all'])
        base.create_new_items(table=f'{project}_related', context=self.out['related'])
        base.create_new_items(table=f'{project}_reviews', context=self.out['reviews'])
        base.create_new_items(table=f'{project}_aspect', context=self.out['aspect'])

    def try_edit(self, data):

        for item in data['stack'][0]['results']['items']:

            self.title = item['title']
            self.coordinates = str(item['coordinates'])
            self.address = item['address']
            self.count_text = str(item['ratingData']['reviewCount'])
            self.count_vote = str(item['ratingData']['ratingCount'])
            self.rating = str(round(item['ratingData']['ratingValue'], 1))

            try:
                for i in item['aspects']:
                    self.aspect_text.append(i['text'])
                    self.aspect_count.append(str(i['count']))
                    self.aspect_positive.append(str(i['positive']))
                    self.aspect_neutral.append(str(i['neutral']))
                    self.aspect_negative.append(str(i['negative']))
                    self.coordinates_aspect.append(self.coordinates)
                    self.title_aspect.append(self.title)
                    self.now_aspect.append(self.now)
            except Exception as ex:
                pass

            try:
                for l in item['relatedPlaces']:
                    self.related_place_name.append(l['title'])
                    self.related_place_rating.append(str(l['rating']))
                    self.related_place_coordinates.append(str(l['coordinates']))
                    self.coordinates_related_place.append(self.coordinates)
                    self.title_related_place.append(self.title)
                    self.now_related_place.append(self.now)
            except Exception as ex:
                pass

            try:
                for m in item['reviewResults']['reviews']:
                    self.reviews_text.append(str(m['text']).strip())
                    try:
                        self.reviews_business_text.append(str(m['businessComment']['text']).strip())
                        self.reviews_business_date.append(
                            str(m['businessComment']['updatedTime']).split('T')[0])
                    except Exception as ex:
                        self.reviews_business_text.append('')
                        self.reviews_business_date.append('')
                    self.reviews_rating.append(str(m['rating']))
                    self.reviews_date.append(str(m['updatedTime']).split('T')[0])
                    self.reviews_like.append(str(m['reactions']['likes']))
                    self.reviews_dislike.append(str(m['reactions']['dislikes']))
                    self.coordinates_text.append(self.coordinates)
                    self.now_date_text.append(self.now)
                    self.title_text.append(self.title)
            except Exception as ex:
                pass

        self.context_all = {
            'project': self.title,
            'coordinates': self.coordinates,
            'address': self.address,
            'count_text': self.count_text,
            'count_vote': self.count_vote,
            'rating': self.rating,
            'now': self.now
        }

        self.context_aspect = {
            'aspect_text': self.aspect_text,
            'aspect_count': self.aspect_count,
            'aspect_positive': self.aspect_positive,
            'aspect_neutral': self.aspect_neutral,
            'aspect_negative': self.aspect_negative,
            'project': self.title_aspect,
            'coordinates': self.coordinates_aspect,
            'now': self.now_aspect
        }

        self.context_related_place = {
            'project': self.title_related_place,
            'coordinates': self.coordinates_related_place,
            'related_project': self.related_place_name,
            'related_coordinates': self.related_place_coordinates,
            'related_rating': self.related_place_rating,
            'now': self.now_related_place
        }

        self.context_reviews = {
            'reviews_text': self.reviews_text,
            'reviews_rating': self.reviews_rating,
            'reviews_date': self.reviews_date,
            'reviews_like': self.reviews_like,
            'reviews_dislike': self.reviews_dislike,
            'reviews_business_text': self.reviews_business_text,
            'reviews_business_date': self.reviews_business_date,
            'project': self.title_text,
            'coordinates': self.coordinates_text,
            'now': self.now_date_text
        }

        self.out = {'all': self.context_all, 'related': self.context_related_place, 'aspect': self.context_aspect,
                    'reviews': self.context_reviews}

    def ex_edit(self, data):

        for item in data['stack'][0]['response']['items']:

            self.title = item['title']
            self.coordinates = str(item['coordinates'])
            self.address = item['address']
            self.count_text = str(item['ratingData']['reviewCount'])
            self.count_vote = str(item['ratingData']['ratingCount'])
            self.rating = str(round(item['ratingData']['ratingValue'], 1))

            try:
                for i in item['aspects']:
                    self.aspect_text.append(i['text'])
                    self.aspect_count.append(str(i['count']))
                    self.aspect_positive.append(str(i['positive']))
                    self.aspect_neutral.append(str(i['neutral']))
                    self.aspect_negative.append(str(i['negative']))
                    self.coordinates_aspect.append(self.coordinates)
                    self.title_aspect.append(self.title)
                    self.now_aspect.append(self.now)
            except Exception as ex:
                pass

            try:
                for l in item['relatedPlaces']:
                    self.related_place_name.append(l['title'])
                    self.related_place_rating.append(str(l['rating']))
                    self.related_place_coordinates.append(str(l['coordinates']))
                    self.coordinates_related_place.append(self.coordinates)
                    self.title_related_place.append(self.title)
                    self.now_related_place.append(self.now)
            except Exception as ex:
                pass

            try:
                for m in item['reviewResults']['reviews']:
                    self.reviews_text.append(str(m['text']).strip())
                    try:
                        self.reviews_business_text.append(str(m['businessComment']['text']).strip())
                        self.reviews_business_date.append(
                            str(m['businessComment']['updatedTime']).split('T')[0])
                    except Exception as ex:
                        self.reviews_business_text.append('')
                        self.reviews_business_date.append('')
                    self.reviews_rating.append(str(m['rating']))
                    self.reviews_date.append(str(m['updatedTime']).split('T')[0])
                    self.reviews_like.append(str(m['reactions']['likes']))
                    self.reviews_dislike.append(str(m['reactions']['dislikes']))
                    self.coordinates_text.append(self.coordinates)
                    self.now_date_text.append(self.now)
                    self.title_text.append(self.title)
            except Exception as ex:
                pass

        self.context_all = {
            'project': self.title,
            'coordinates': self.coordinates,
            'address': self.address,
            'count_text': self.count_text,
            'count_vote': self.count_vote,
            'rating': self.rating,
            'now': self.now
        }

        self.context_aspect = {
            'aspect_text': self.aspect_text,
            'aspect_count': self.aspect_count,
            'aspect_positive': self.aspect_positive,
            'aspect_neutral': self.aspect_neutral,
            'aspect_negative': self.aspect_negative,
            'project': self.title_aspect,
            'coordinates': self.coordinates_aspect,
            'now': self.now_aspect
        }

        self.context_related_place = {
            'project': self.title_related_place,
            'coordinates': self.coordinates_related_place,
            'related_project': self.related_place_name,
            'related_coordinates': self.related_place_coordinates,
            'related_rating': self.related_place_rating,
            'now': self.now_related_place
        }

        self.context_reviews = {
            'reviews_text': self.reviews_text,
            'reviews_rating': self.reviews_rating,
            'reviews_date': self.reviews_date,
            'reviews_like': self.reviews_like,
            'reviews_dislike': self.reviews_dislike,
            'reviews_business_text': self.reviews_business_text,
            'reviews_business_date': self.reviews_business_date,
            'project': self.title_text,
            'coordinates': self.coordinates_text,
            'now': self.now_date_text
        }

        self.out = {'all': self.context_all, 'related': self.context_related_place, 'aspect': self.context_aspect,
                    'reviews': self.context_reviews}
