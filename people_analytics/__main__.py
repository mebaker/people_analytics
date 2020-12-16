import sys
from luigi import build
import argparse
from datetime import datetime
from .tasks.output_clean_data import OutputCleanData
from .tasks.site_metrics import SiteMetrics
from .tasks.turnover import Turnover

default = datetime.now().strftime("%Y-%m-%d")
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", default=default)


def main(args=[]):
    if len(args) > 1:
        args.pop(0)
        args, unknown = parser.parse_known_args(args)
        if args.date:
            date = str(args.date).replace("/", "-")
        else:
            date = default
    else:
        date = default
    build(
        [OutputCleanData(report_date=date), SiteMetrics(report_date=date), Turnover(report_date=date)],
        local_scheduler=True,
    )


main(sys.argv)
