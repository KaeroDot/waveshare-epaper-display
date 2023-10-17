import datetime
import os.path
import os
import logging
from calendar_providers.base_provider import CalendarEvent
from calendar_providers.caldav import CalDavCalendar
from calendar_providers.google import GoogleCalendar
from calendar_providers.ics import ICSCalendar
from calendar_providers.outlook import OutlookCalendar
from utility import get_formatted_time, update_svg, configure_logging, get_formatted_date, configure_locale
from operator import attrgetter

configure_locale()
configure_logging()

# note: increasing this will require updates to the SVG template to accommodate more events
max_event_results = 10

outlook_calendar_id = os.getenv("OUTLOOK_CALENDAR_ID", None)

caldav_calendar_url = os.getenv('CALDAV_CALENDAR_URL', None)
caldav_username = os.getenv("CALDAV_USERNAME", None)
caldav_password = os.getenv("CALDAV_PASSWORD", None)
caldav_calendar_id = os.getenv("CALDAV_CALENDAR_ID", None)

# Get data for Google and ics calendars, up to 5 for each:
google_calendar_ids = []
ics_calendar_urls = []
for id in range(1, 6):
    google_calendar_ids.append(os.getenv("GOOGLE_CALENDAR_ID_{}".format(id), None))
    ics_calendar_urls.append(os.getenv("ICS_CALENDAR_URL_{}".format(id), None))

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))


def get_formatted_calendar_events(fetched_events: list[CalendarEvent]) -> dict:
    formatted_events = {}
    event_count = len(fetched_events)

    for index in range(max_event_results):
        event_label_id = str(index + 1)
        if index <= event_count - 1:
            formatted_events['CAL_DATETIME_' + event_label_id] = get_datetime_formatted(fetched_events[index].start, fetched_events[index].end, fetched_events[index].all_day_event)
            formatted_events['CAL_DESC_' + event_label_id] = fetched_events[index].summary
        else:
            formatted_events['CAL_DATETIME_' + event_label_id] = ""
            formatted_events['CAL_DESC_' + event_label_id] = ""

    return formatted_events


def get_datetime_formatted(event_start, event_end, is_all_day_event):

    if is_all_day_event or type(event_start) == datetime.date:
        start = datetime.datetime.combine(event_start, datetime.time.min)
        end = datetime.datetime.combine(event_end, datetime.time.min)

        start_day = get_formatted_date(start, include_time=False)
        end_day = get_formatted_date(end, include_time=False)
        if start == end:
            day = start_day
        else:
            day = "{} – {}".format(start_day, end_day)
    elif type(event_start) == datetime.datetime:
        start_date = event_start
        end_date = event_end
        if start_date.date() == end_date.date():
            start_formatted = get_formatted_date(start_date)
            end_formatted = get_formatted_time(end_date)
        else:
            start_formatted = get_formatted_date(start_date)
            end_formatted = get_formatted_date(end_date)
        day = "{} - {}".format(start_formatted, end_formatted)
    else:
        day = ''
    return day


def main():

    output_svg_filename = 'screen-output-weather.svg'

    today_start_time = datetime.datetime.utcnow()
    if os.getenv("CALENDAR_INCLUDE_PAST_EVENTS_FOR_TODAY", "0") == "1":
        today_start_time = datetime.datetime.combine(datetime.datetime.utcnow(), datetime.datetime.min.time())
    oneyearlater_iso = (datetime.datetime.now().astimezone()
                        + datetime.timedelta(days=365)).astimezone()

    # Initiate calendar providers:
    providers = [];
    # initiate outlook calendar:
    if outlook_calendar_id:
        logging.info("Fetching Outlook Calendar Events")
        provider.append(OutlookCalendar(outlook_calendar_id, max_event_results, today_start_time, oneyearlater_iso))
    # initiate caldav calendar:
    if caldav_calendar_url:
        logging.info("Fetching Caldav Calendar Events")
        provider.append(CalDavCalendar(caldav_calendar_url, caldav_calendar_id, max_event_results,
                                  today_start_time, oneyearlater_iso, caldav_username, caldav_password))
    # initiate up to five ics calendars:
    for index, ics_calendar_url in enumerate(ics_calendar_urls):
        if ics_calendar_url:
            logging.info("Fetching events from ICS calendar number {} at {}".format(index + 1, ics_calendar_url))
            providers.append(ICSCalendar(ics_calendar_url, max_event_results, today_start_time, oneyearlater_iso, index + 1))
    # initiate google calendars:
    for index, google_calendar_id in enumerate(google_calendar_ids):
        if google_calendar_id:
            logging.info("Fetching events from Google calendar number {} with ID {}".format(index + 1, google_calendar_id))
            providers.append(GoogleCalendar(google_calendar_id, max_event_results, today_start_time, oneyearlater_iso, index + 1))

    # Fetch available calendars:
    calendar_events = [];
    for provider in providers:
        calendar_events = calendar_events + provider.get_calendar_events()
    # sort events by start date:
    calendar_events = sorted(calendar_events, key=attrgetter('start'))

    output_dict = get_formatted_calendar_events(calendar_events)

    logging.info("main() - {}".format(output_dict))

    logging.info("Updating SVG")
    update_svg(output_svg_filename, output_svg_filename, output_dict)


if __name__ == "__main__":
    main()
