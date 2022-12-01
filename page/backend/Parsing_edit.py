from datetime import datetime
from .Databased import Base


class EditParse:

    def __init__(self):
        self.title_text = None
        self.now_related_place = None
        self.title_related_place = None
        self.now_aspect = None
        self.title_aspect = None
        self.count_vote = None
        self.rating = None
        self.count_text = None
        self.address = None
        self.coordinates = None
        self.now_date_text = None
        self.title = None
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

        data = content

        for items in data['stack']:
            for item in items['results']['items']:

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
                    for q in range(len(self.aspect_text)):
                        self.coordinates_aspect.append(self.coordinates)
                    self.title_aspect = [self.title] * len(self.aspect_text)
                    self.now_aspect = [self.now] * len(self.aspect_text)
                except Exception as ex:
                    pass

                try:
                    for l in item['relatedPlaces']:
                        self.related_place_name.append(l['title'])
                        self.related_place_rating.append(str(l['rating']))
                        self.related_place_coordinates.append(str(l['coordinates']))
                    for q in range(len(self.related_place_name)):
                        self.coordinates_related_place.append(self.coordinates)
                    self.title_related_place = [self.title] * len(self.related_place_name)
                    self.now_related_place = [self.now] * len(self.related_place_name)
                except Exception as ex:
                    pass

                try:
                    for m in item['reviewResults']['reviews']:
                        self.reviews_text.append(str(m['text']).strip())
                        try:
                            self.reviews_business_text.append(str(m['businessComment']['text']).strip())
                            self.reviews_business_date.append(str(m['businessComment']['updatedTime']).split('T')[0])
                        except Exception as ex:
                            self.reviews_business_text.append('')
                            self.reviews_business_date.append('')
                        self.reviews_rating.append(str(m['rating']))
                        self.reviews_date.append(str(m['updatedTime']).split('T')[0])
                        self.reviews_like.append(str(m['reactions']['likes']))
                        self.reviews_dislike.append(str(m['reactions']['dislikes']))
                    for q in range(len(self.reviews_text)):
                        self.coordinates_text.append(self.coordinates)
                    self.now_date_text = [self.now] * len(self.reviews_text)
                    self.title_text = [self.title] * len(self.reviews_text)
                except Exception as ex:
                    pass

        context_all = {
            'project': self.title,
            'coordinates': self.coordinates,
            'address': self.address,
            'count_text': self.count_text,
            'count_vote': self.count_vote,
            'rating': self.rating,
            'now': self.now
        }

        context_aspect = {
            'aspect_text': self.aspect_text,
            'aspect_count': self.aspect_count,
            'aspect_positive': self.aspect_positive,
            'aspect_neutral': self.aspect_neutral,
            'aspect_negative': self.aspect_negative,
            'project': self.title_aspect,
            'coordinates': self.coordinates_aspect,
            'now': self.now_aspect
        }

        context_related_place = {
            'project': self.title_related_place,
            'coordinates': self.coordinates_related_place,
            'related_project': self.related_place_name,
            'related_coordinates': self.related_place_coordinates,
            'related_rating': self.related_place_rating,
            'now': self.now_related_place
        }

        context_reviews = {
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

        base = Base()
        base.create_new_items(table=f'{project}_all', context=context_all)
        base.create_new_items(table=f'{project}_related', context=context_related_place)
        base.create_new_items(table=f'{project}_reviews', context=context_reviews)
        base.create_new_items(table=f'{project}_aspect', context=context_aspect)
