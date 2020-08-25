from twittervotes.core.hashtag import Hashtag

class HashtagStatsManager:
    def __init__(self, hashtags):

        if not hashtags:
            raise AttributeError('hashtags must be provided')

        self.__hashtags = {hashtag: Hashtag(hashtag) for hashtag in hashtags}
    def update(self, data):

        hashtag, results = data
        metadata = results.get('search_metadata')
        refresh_url = metadata.get('resfresh_url')
        statuses = results.get('statuses')

        total = len(statuses)

        if total > 0:
            self.__hashtags.get(hashtag.name).total += total
            self.__hashtags.get(hashtag.name).refresh_url = refresh_url

    @property
    def hashtags(self):
        return self._hashtags


import concurrent.futures
from rx import Observable

class Runner:
    def __init__(self, on_success, on_error, on_complete):
        self._on_success = on_success
        self._on_error = on_error
        self._on_complete = on_complete

    def exec(self, func, items):

        observables = []

        with  concurrent.futures.ProcessPoolExecutort() as executor:
            for item  in items.values():
                _future = executor.submit(func, item)
                observables.append(Observable.from_future(_future))
        all_observables = Observable.merge(observables)
        all_observables.subscribe(self._on_success,
                                  self._on_error,
                                  self._on_complete)

