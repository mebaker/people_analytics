from luigi import build
import argparse
from datetime import datetime
from .tasks.output_clean_data import OutputCleanData
from .tasks.site_metrics import SiteMetrics

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--date", default=datetime.now().strftime("%Y-%m-%d"))


def main():
    args = parser.parse_args()
    date = str(args.date).replace("/", "-")
    build(
        [OutputCleanData(report_date=date), SiteMetrics(report_date=date)],
        local_scheduler=True,
    )


main()
