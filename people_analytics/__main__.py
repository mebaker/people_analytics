from luigi import build
import argparse
from datetime import datetime
from .tasks.output_clean_data import OutputCleanData
from .tasks.site_metrics import SiteMetrics

default = datetime.now().strftime("%Y-%m-%d")
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", default=default)


def main(*args):
    if args:
        args = parser.parse_args(*args)
        date = str(args.date).replace("/", "-")
    else:
        date = default
    build(
        [OutputCleanData(report_date=date), SiteMetrics(report_date=date)],
        local_scheduler=True,
    )


main()
