import datetime
import pprint
import time
from datetime import datetime

import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

pp = pprint.PrettyPrinter(indent=1)
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = ''
VIEW_ID = ''
top_pages_count = 500
start_time = '7daysAgo'
end_time = 'yesterday'
website_URL = 'https://www.admitkard.com'
starting_peak_time = '07:00:00'
ending_peak_time = '02:00:00'


def initialize_analytics_reporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics_client = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics_client


def get_top_pages_report(analytics, top_pages_count, start_time, end_time):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': start_time, 'endDate': end_time}],
                    'metrics': [{'expression': 'ga:pageviews'}],
                    'dimensions': [{'name': 'ga:pagePath'}],
                    'orderBys': [{"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"}],
                    'pageSize': top_pages_count
                }]
        }
    ).execute()


def hit_url_print_response(prefix_url, postfix_url):
    main_url = prefix_url + postfix_url
    response = requests.get(main_url)
    pp.pprint("URL : " + main_url + " " + "Response : " + str(response))


def main():
    analytics_client = initialize_analytics_reporting()
    top_pages = get_top_pages_report(analytics_client, top_pages_count, start_time, end_time)
    for x in top_pages['reports'][0]['data']['rows']:
        if len(x['metrics']) > 0 and 'values' in x['metrics'][0] and len(x['metrics'][0]['values']) > 0:
            url_list = list({','.join(x['dimensions']): x['metrics'][0]['values'][0]}.keys())[0]
            hit_url_print_response(website_URL, url_list)
            current_limit = datetime.strftime(datetime.now(), '%H:%M:%S')
            if starting_peak_time > current_limit > ending_peak_time:
                time.sleep(1)
            else:
                time.sleep(5)


if __name__ == '__main__':
    main()
