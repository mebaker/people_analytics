import pickle
from luigi import Task
from .utils import Requirement, Requires
from .clean_data import CleanData


class TurnOverRate(Task):

    requires = Requires()
    data = Requirement(CleanData)

    def run(self):
        pass
        # print(pickle.load(self.input().get('data').open('r')))
