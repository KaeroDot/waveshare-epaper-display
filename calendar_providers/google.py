import datetime
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
from utility import is_stale
import os
import logging
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))


class GoogleCalendar(BaseCalendarProvider):
    def __init__(self, google_calendar_id, max_event_results, from_date, to_date, index):
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date
        self.google_calendar_id = google_calendar_id
        self.google_calendar_timezone = os.getenv("GOOGLE_CALENDAR_TIME_ZONE_NAME_{}".format(index), None)
        self.index = index

    def get_google_credentials(self):

        google_token_pickle = 'token_google_{}.pickle'.format(self.index)
        google_credentials_json = 'credentials_google_{}.json'.format(self.index)
        google_api_scopes = ['https://www.googleapis.com/auth/calendar.readonly']

        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(google_token_pickle):
            with open(google_token_pickle, 'rb') as token:
                credentials = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    google_credentials_json, google_api_scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(google_token_pickle, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def get_calendar_events(self) -> list[CalendarEvent]:
        calendar_events = []
        google_calendar_pickle = 'cache_google_{}.pickle'.format(self.index)

        service = build('calendar', 'v3', credentials=self.get_google_credentials(), cache_discovery=False)

        events_result = None

        if is_stale(os.getcwd() + "/" + google_calendar_pickle, ttl):
            logging.debug("Cache of Google calendar {} is stale, fetching.".format(self.index))

            # Call the Calendar API
            events_result = service.events().list(
                calendarId=self.google_calendar_id,
                timeMin=self.from_date.isoformat() + 'Z',
                timeZone=self.google_calendar_timezone,
                maxResults=self.max_event_results,
                singleEvents=True,
                orderBy='startTime').execute()

            for event in events_result.get('items', []):
                if event['start'].get('date'):
                    is_all_day = True
                    start_date = datetime.datetime.strptime(event['start'].get('date'), "%Y-%m-%d")
                    end_date = datetime.datetime.strptime(event['end'].get('date'), "%Y-%m-%d")
                    # Google Calendar marks the 'end' of all-day-events as
                    # the day _after_ the last day. eg, Today's all day event ends tomorrow!
                    # So subtract a day
                    end_date = end_date - datetime.timedelta(days=1)
                else:
                    is_all_day = False
                    start_date = datetime.datetime.strptime(event['start'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")
                    end_date = datetime.datetime.strptime(event['end'].get('dateTime'), "%Y-%m-%dT%H:%M:%S%z")

                summary = event['summary']

                # If start_date or end_date are timezone unaware, add local
                # time zone, so all events from all calendars can be properly
                # sorted.
                # Get local time zone:
                localtimezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
                if start_date.tzname() is None:
                    # set timezone of timezone-unaware-datetime-object to local time zone:
                    start_date = start_date.replace(tzinfo=localtimezone)
                if end_date.tzname() is None:
                    end_date = end_date.replace(tzinfo=localtimezone)

                calendar_events.append(CalendarEvent(summary, start_date, end_date, is_all_day))

            with open(google_calendar_pickle, 'wb') as cal:
                pickle.dump(calendar_events, cal)

        else:
            logging.info("Google calendar {} found in cache.".format(self.index))
            with open(google_calendar_pickle, 'rb') as cal:
                calendar_events = pickle.load(cal)

        if len(calendar_events) == 0:
            logging.info("No upcoming events found.")

        return calendar_events
