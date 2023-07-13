"""Extract data from luftdaten.info"""
import itertools
from dataclasses import dataclass
import requests
import re
import pandas as pd
# import pandera as pa
# from pandera import check_output
import datetime as dt

from citizen_pm_analytics.config import DATA_FOLDER

BASE_URL = 'https://archive.sensor.community'

DATE_COLUMN = 'date'
URL_COLUMN = 'url'

# date_url_schema = pa.DataFrameSchema({
#     DATE_COLUMN: pa.Column(pa.typing.Date),
#     URL_COLUMN: pa.Column(str, checks=pa.Check.str_startswith(BASE_URL)),
# })


@dataclass(frozen=True)
class LuftdatenInfo:

    @classmethod
    def available_date_urls(cls, url: str) -> set[str]:
        """Get available date urls."""
        response = requests.get(url, stream=True)
        dates = set(re.findall(r'(?<=\<a href\=\")(\d{4}|\d{4}\-\d\d\-\d\d)(?=\/\"\>)', response.text))
        years = set(date for date in dates if re.match(r'^\d{4}$', date))
        if years:
            dates = dates - years
            dates = set(f'{url}/{date}' for date in dates)
            old_dates = set(itertools.chain.from_iterable(cls.available_date_urls(f'{url}/{year}') for year in years))
            dates.update(old_dates)
        else:
            dates = set(f'{url}/{date}' for date in dates)

        return dates

    @classmethod
    # @check_output(date_url_schema)
    def daily_urls(cls) -> pd.DataFrame:
        """Get mapping from date to url, which is parent to csv files."""
        urls = list(sorted(cls.available_date_urls(BASE_URL)))
        df = pd.DataFrame(
            {'date': [dt.datetime.strptime(re.search(r'\d{4}\-\d\d\-\d\d', url).group(), '%Y-%m-%d') for url in urls],
             'url': urls}
        )
        return df


if __name__ == '__main__':
    # links = LuftdatenInfo.daily_urls()
    # links.to_csv(DATA_FOLDER / 'date_urls')

    ...