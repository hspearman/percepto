from abc import ABCMeta

__author__ = 'Hannah'


class ISentimentAnalyzer:
    __metaclass__ = ABCMeta

    def is_match(self, comment): raise NotImplementedError
