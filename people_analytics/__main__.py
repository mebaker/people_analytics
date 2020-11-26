from luigi import build
from .tasks.clean_data import CleanData


def main():
    build([CleanData()], local_scheduler=True)


main()
