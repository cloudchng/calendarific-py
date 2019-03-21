import json
import requests
from dateutil.parser import parse
import pandas as pd
import csv

API_KEY = ''

def CalHolidays(parameters):
    url = 'https://calendarific.com/api/v2/holidays?'

    parameters['api_key'] = API_KEY

    response = requests.get(url, params=parameters);
    data = json.loads(response.text)

    if response.status_code != 200:
        if data.has_key('error') is False:
            data['error'] = 'Unknown error.'

    return data


holiday_list = []

if __name__ == "__main__":
    country_list = [
        {'country':'MY', 'year':2017},
        {'country':'MY', 'year':2018},
        {'country':'SG', 'year':2019},
        {'country':'SG', 'year':2020},
        {'country':'TH', 'year':2021},
    ]
    for country in country_list:
        parameters = {
            # Required
            'country': country['country'],
            'year': country['year'],
        }
        holidays = CalHolidays(parameters)
        try:
            if holidays['response']:
                if holidays['response']['holidays']:
                    for holiday in holidays['response']['holidays']:
                        dt = parse(str(holiday['date']['iso']))
                        final_date = dt.strftime('%Y-%m-%d')
                        holiday_dict = {
                            'ds': final_date,
                            'holiday': holiday['name'],
                            'country': country['country'],
                            'year': country['year']
                        }
                        holiday_list.append(holiday_dict)
        except KeyError:
            pass

    holidays_df = pd.DataFrame(holiday_list)
    holidays_df.to_csv('holiday.csv', sep=',', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL, quotechar='"')
    # print(holidays_df)
