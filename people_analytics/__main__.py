from luigi import build
from .tasks.output_clean_data import OutputCleanData
from .tasks.turn_over_rate import TurnOverRate


def main():
    build([TurnOverRate(), OutputCleanData()], local_scheduler=True)


main()
