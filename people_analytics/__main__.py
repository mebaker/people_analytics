from luigi import build
from .tasks.output_clean_data import OutputCleanData
from .tasks.turn_over_rate import TurnOverRate
from .tasks.site_metrics import SiteMetrics


def main():
    build([TurnOverRate(), OutputCleanData(), SiteMetrics()], local_scheduler=True)


main()
