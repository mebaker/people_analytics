from luigi import build
from .tasks.output_clean_data import OutputCleanData
from .tasks.site_metrics import SiteMetrics


def main():
    build([OutputCleanData(), SiteMetrics()], local_scheduler=True)


main()
