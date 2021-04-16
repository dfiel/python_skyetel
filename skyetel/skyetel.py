import requests
from ratelimit import limits
from datetime import datetime
from typing import List, Dict
from dataclasses import asdict

from . import errors, urls, responses

SKYETEL_DATESTRING = '%Y-%m-%dT%H:%M:%S+00:00'
SKYETEL_TIMESTRING = '%H:%M:%S+00:00'


class Skyetel:
    def __init__(self, x_auth_sid, x_auth_secret):
        self.__x_auth_sid = x_auth_sid
        self.__x_auth_secret = x_auth_secret
        self.__url = urls.URLs()

        self.__session = requests.Session()
        self.__session.headers = {'X-AUTH-SID': x_auth_sid, 'X-AUTH-SECRET': x_auth_secret}

    @limits(calls=120, period=60)
    def __make_api_request(self, request_type, endpoint, data=None, json=None):
        try:
            if request_type == 'GET':
                response = self.__session.get(endpoint)

            elif request_type == 'POST':
                response = self.__session.post(endpoint, data=data, json=json)

            elif request_type == 'PATCH':
                response = self.__session.patch(endpoint, data=data, json=json)

            else:
                raise AttributeError('Invalid Request Type')

            if response.status_code != 200:
                content = response.json()
                raise errors.APIError(content['ERROR'])

        except (requests.ConnectionError, requests.Timeout) as e:
            raise errors.Unavailable() from e

        return response.json()

    def get_audio_recordings_list(self, items_per_page=10, page_offset=0, query=None, search=None, sort=None):
        """
            Get a list of the phone call recordings.
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param query: string, wildcard search on all string fields
        :param search: dict, format 'field':'query'
        :param sort: list[string], list of fields to sort, prefix a '-' for descending sort
        :return: list[AudioRecording], List of AudioRecording objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if query:
            parameters += '&filter[query]={}'.format(query)
        if search:
            for field in search:
                parameters += '&filter[{}]={}'.format(field, search[field])
        if sort:
            parameters += '&sort={}'.format(sort[0])
            for x in range(1, len(sort)):
                parameters += ',{}'.format(sort[x])

        response = self.__make_api_request('GET', self.__url.audio_recordings_url() + parameters)
        if response:
            for x in range(0, len(response)):
                response[x]['insert_time'] = datetime.strptime(response[x]['insert_time'], SKYETEL_DATESTRING)
                response[x]['start_time'] = datetime.strptime(response[x]['start_time'], SKYETEL_DATESTRING)
                response[x]['org'] = responses.Organization(**response[x]['org'])
                response[x] = responses.AudioRecording(**response[x])
            return response
        else:
            return None

    def get_audio_recording_url(self, recording_id):
        """
            Get the URL for the audio file of a specific call recording
        :param recording_id: integer, ID of a call recording from recording list
        :return: string, URL of call recording audio file
        """
        response = self.__make_api_request('GET', self.__url.audio_recording_download_url(recording_id))
        return response['download_url']

    def get_audio_transcriptions_list(self, items_per_page=10, page_offset=0, query=None, search=None, sort=None):
        """
            Get a list of all phone call transcriptions
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param query: string, wildcard search on all string fields
        :param search: dict, format 'field':'query'
        :param sort: list[string], list of fields to sort, prefix a '-' for descending sort
        :return: list[AudioTranscription], list of AudioTranscription objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if query:
            parameters += '&filter[query]={}'.format(query)
        if search:
            for field in search:
                parameters += '&filter[{}]={}'.format(field, search[field])
        if sort:
            parameters += '&sort={}'.format(sort[0])
            for x in range(1, len(sort)):
                parameters += ',{}'.format(sort[x])

        response = self.__make_api_request('GET', self.__url.audio_transcriptions_url() + parameters)
        if response:
            for x in range(0, len(response)):
                response[x]['insert_time'] = datetime.strptime(response[x]['insert_time'], SKYETEL_DATESTRING)
                response[x]['start_time'] = datetime.strptime(response[x]['start_time'], SKYETEL_DATESTRING)
                response[x]['org'] = responses.Organization(**response[x]['org'])
                response[x] = responses.AudioTranscription(**response[x])
            return response
        else:
            return None

    def get_audio_transcription_url(self, transcription_id):
        """
            Get the URL for the text log of a specific call transcription
        :param transcription_id: integer, ID of a call transcription from transcription list
        :return: string, URL of call transcription text log
        """
        response = self.__make_api_request('GET', self.__url.audio_transcription_download_url(transcription_id))
        return response['download_url']

    def get_audio_transcription_text(self, transcription_id):
        """
            Get the text log for a specific call transcription
        :param transcription_id: integer, ID of a call transcription from transcription list
        :return: dict, dictionary of both parties text and timestamps
        """
        response = self.__make_api_request('GET', self.__url.audio_transcription_download_url(transcription_id))
        url = response['download_url']
        transcript = requests.get(url).json()
        return transcript

    def get_billing_balance(self):
        """
            Get the remaining balance on the account
        :return: float, billing balance remaining on the account
        """
        response = self.__make_api_request('GET', self.__url.balance_url())
        return float(response['BALANCE'])

    def get_organization_statement(self, year=None, month=None):
        """
            Get the monthly statement for the entire organization account. Defaults to current month.
        :param year: integer, four digit year of the statement month
        :param month: integer, single or double digit, with January corresponding to 1
        :return: BillingStatement
        """
        parameters = '?'
        if year:
            parameters += 'year={}'.format(year)
            if month:
                parameters += '&'
        if month:
            parameters += 'month={}'.format(month)
        response = self.__make_api_request('GET', self.__url.organization_statement_url() + parameters)
        if response['transactions']:
            for x in range(0, len(response['transactions'])):
                response['transactions'][x]['transaction_date'] = datetime.strptime(
                    response['transactions'][x]['transaction_date'], SKYETEL_DATESTRING)
                response['transactions'][x] = responses.StatementTransaction(**response['transactions'][x])
        if response['taxes']:
            for x in range(0, len(response['taxes'])):
                response['taxes'][x] = responses.StatementTax(**response['taxes'][x])
        if response['statement']:
            response['statement']['totals']['phone_numbers'] = responses.PhoneNumberTotals(
                **response['statement']['totals']['phone_numbers'])
            response['statement'] = responses.StatementTotals(**response['statement']['totals'])
        response = responses.BillingStatement(**response)
        return response

    def get_endpoints_list(self, items_per_page=10, page_offset=0):
        """
            Get list of SIP Endpoints
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :return: list[Endpoint], list of Endpoint objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        response = self.__make_api_request('GET', self.__url.endpoints_url() + parameters)
        for x in range(0, len(response)):
            response[x]['endpoint_group'] = responses.EndpointGroup(**response[x]['endpoint_group'])
            response[x]['org'] = responses.Organization(org_id=response[x]['org']['id'],
                                                        org_name=response[x]['org']['name'])
            response[x] = responses.Endpoint(**response[x])
        return response

    def create_endpoint(self, ip, priority, description, endpoint_group_id, endpoint_group_name, port=5060,
                        transport="udp"):
        """
            Create a new SIP Endpoint in an Endpoint Group
        :param ip: string, IPv4 Address of the Endpoint
        :param priority: integer, the higher the number, the higher the priority
        :param description: string, short note to describe the Endpoint
        :param endpoint_group_id: integer, Endpoint Group ID
        :param endpoint_group_name: string, Endpoint Group Name
        :param port: integer, SIP Port Number for the Endpoint (default 5060)
        :param transport: string, SIP Transport method, UDP (default) or TCP
        :return: Endpoint, object representation of the created Endpoint
        """
        parameters = {'ip': ip, 'port': port, 'transport': transport, 'priority': priority, 'description': description,
                      'endpoint_group_id': endpoint_group_id, 'endpoint_group_name': endpoint_group_name}
        response = self.__make_api_request('POST', self.__url.endpoints_url(), data=parameters)
        response['endpoint_group'] = responses.EndpointGroup(**response['endpoint_group'])
        response['org'] = responses.Organization(org_id=response['org']['id'],
                                                 org_name=response['org']['name'])
        response = responses.Endpoint(**response)
        return response

    def update_endpoint(self, endpoint_id, ip, priority, description, endpoint_group_id, endpoint_group_name, port=5060,
                        transport="udp"):
        """
            Update an existing Endpoint's details
        :param endpoint_id: integer, assigned ID for the Endpoint
        :param ip: string, IPv4 Address of the Endpoint
        :param priority: integer, the higher the number, the higher the priority
        :param description: string, short note to describe the Endpoint
        :param endpoint_group_id: integer, Endpoint Group ID
        :param endpoint_group_name: string, Endpoint Group Name
        :param port: integer, SIP Port Number for the Endpoint (default 5060)
        :param transport: string, SIP Transport method, UDP (default) or TCP
        :return: Endpoint, object representation of the updated Endpoint
        """
        parameters = {'ip': ip, 'port': port, 'transport': transport, 'priority': priority, 'description': description,
                      'endpoint_group_id': endpoint_group_id, 'endpoint_group_name': endpoint_group_name}
        response = self.__make_api_request('PATCH', self.__url.endpoint_url(endpoint_id), data=parameters)
        response['endpoint_group'] = responses.EndpointGroup(**response['endpoint_group'])
        response['org'] = responses.Organization(org_id=response['org']['id'],
                                                 org_name=response['org']['name'])
        response = responses.Endpoint(**response)
        return response

    def get_phonenumber_e911(self, phonenumber_id):
        """
            Get the E911 address associated with a phone number
        :param phonenumber_id: integer, assigned ID for the Phone Number
        :return: E911Address, object representation of the associated E911 Address
        """
        response = self.__make_api_request('GET', self.__url.phonenumber_e911address_url(phonenumber_id))
        response = responses.E911Address(**response)
        return response

    def create_phonenumber_e911(self, phonenumber_id, caller_name, address1, address2, community, state, postal_code):
        """
            Create an E911 address for a phone number and enable E911 processing
        :param phonenumber_id: integer, assigned ID for the Phone Number
        :param caller_name: string, Name associated with the Phone Number
        :param address1: string, First Address Line for Emergency Response
        :param address2: string, Second Address Line for Emergency Response
        :param community: string, City for Emergency Response
        :param state: string, Two letter State Abbreviation for Emergency Response
        :param postal_code: string, Postal Code for Emergency Response
        :return: E911Address, object representation of the associated E911 Address
        """
        parameters = {'caller_name': caller_name, 'address1': address1, 'address2': address2, 'community': community,
                      'state': state, 'postal_code': postal_code}
        response = self.__make_api_request('POST', self.__url.phonenumber_e911address_url(phonenumber_id),
                                           data=parameters)
        response = responses.E911Address(**response)
        return response

    def update_phonenumber_e911(self, phonenumber_id: int, caller_name, address1, address2, community, state,
                                postal_code):
        """
            Update an E911 address for a phone number
        :param phonenumber_id: integer, assigned ID for the Phone Number
        :param caller_name: string, Name associated with the Phone Number
        :param address1: string, First Address Line for Emergency Response
        :param address2: string, Second Address Line for Emergency Response
        :param community: string, City for Emergency Response
        :param state: string, Two letter State Abbreviation for Emergency Response
        :param postal_code: string, Postal Code for Emergency Response
        :return: E911Address, object representation of the associated E911 Address
        """
        parameters = {'caller_name': caller_name, 'address1': address1, 'address2': address2, 'community': community,
                      'state': state, 'postal_code': postal_code}
        response = self.__make_api_request('PATCH', self.__url.phonenumber_e911address_url(phonenumber_id),
                                           data=parameters)
        response = responses.E911Address(**response)
        return response

    def get_phonenumbers(self, items_per_page=10, page_offset=0, query: str = None, search: Dict = None,
                         sort: List = None):
        """
            Get a list of all Phone Numbers associated with the organization account
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param query: string, wildcard search on all string fields
        :param search: dict, format 'field':'query'
        :param sort: list[string], list of fields to sort, prefix a '-' for descending sort
        :return: list[PhoneNumber], list of PhoneNumber objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if query:
            parameters += '&filter[query]={}'.format(query)
        if search:
            for field in search:
                parameters += '&filter[{}]={}'.format(field, search[field])
        if sort:
            parameters += '&sort={}'.format(sort[0])
            for x in range(1, len(sort)):
                parameters += ',{}'.format(sort[x])
        response = self.__make_api_request('GET', self.__url.phonenumbers_url() + parameters)
        for x in range(0, len(response)):
            response[x]['number'] = int(response[x]['number'])
            if response[x]['forward']:
                response[x]['forward'] = int(response[x]['forward'])
            if response[x]['failover']:
                response[x]['failover'] = int(response[x]['failover'])
            if response[x]['endpoint_group']:
                response[x]['endpoint_group'] = responses.EndpointGroup(**response[x]['endpoint_group'])
            if response[x]['tenant']:
                response[x]['tenant'] = responses.Tenant(**response[x]['tenant'])
            if response[x]['origination']:
                response[x]['origination'] = responses.Origination(**response[x]['origination'])
            if response[x]['e911address']:
                response[x]['e911address'] = responses.E911Address(**response[x]['e911address'])
            response[x]['intl_balance'] = float(response[x]['intl_balance'])
            response[x]['intl_reserve'] = float(response[x]['intl_reserve'])
            response[x]['org']['account_number'] = int(response[x]['org']['account_number'])
            response[x]['org']['support_pin'] = int(response[x]['org']['support_pin'])
            response[x]['org']['balance'] = float(response[x]['org']['balance'])
            response[x]['org']['auto_recharge_reserve'] = float(response[x]['org']['auto_recharge_reserve'])
            response[x]['org'] = responses.ExtendedOrganization(**response[x]['org'])
            response[x] = responses.PhoneNumber(**response[x])
        return response

    def create_off_network_phonenumber(self, number: str):
        """
            Creates an Off-Network Phone Number
        :param number: string, 11 digit phone number to register
        :return: OffNetworkPhoneNumber, object representation of the Off-Network Phone Number
        """
        parameters = {'number': str(number)}
        response = self.__make_api_request('POST', self.__url.phonenumbers_offnetwork_url(), json=parameters)
        response = responses.OffNetworkPhoneNumber(**response)
        return response

    def update_phonenumber(self, phonenumber_id: int, update_data: responses.PhoneNumberUpdate):
        """
            Update features and settings of a Phone Number
        :param phonenumber_id: integer, assigned Id for the Phone Number
        :param update_data: PhoneNumberUpdate, object containing changes to apply to the Phone Number
        :return: PhoneNumberUpdate, object representation of the Phone Number's features and settings
        """
        data = update_data.as_dict()
        response = self.__make_api_request('PATCH', self.__url.phonenumber_url(phonenumber_id), data=data)
        response = responses.PhoneNumberUpdate(**response)
        return response

    def get_available_phonenumbers(self, search_filter: responses.PhoneNumberFilter = None):
        """
            Get a list of Phone Numbers available for purchase, with filtering. Phone Numbers are held server-side
            for 10 minutes
        :param search_filter: PhoneNumberFilter, object containing filters to apply to search
        :return: list[string], List of Phone Numbers available for purchase
        """
        params = ''
        if search_filter:
            params = search_filter.params()
        response = self.__make_api_request('GET', self.__url.phonenumbers_ordersearch_url() + params)
        return response

    def get_rate_centers(self, state: str = None):
        """
            Get a list of Rate Centers in a given State
        :param state: string, Two letter State Abbreviation
        :return: list[RateCenter], list of RateCenter objects
        """
        params = ''
        if state:
            params = '?state={}'.format(state)
        response = self.__make_api_request('GET', self.__url.phonenumbers_ratecenters_url() + params)
        for x in range(0, len(response)):
            response[x] = responses.RateCenter(**response[x])
        return response

    def order_phonenumbers(self, number_list: List[responses.NumberPurchase]):
        """
            Order Phone Numbers
        :param number_list: list[NumberPurchase], List of NumberPurchase objects with associated MOU
        :return: list[PhoneNumberUpdate], List of PhoneNumberUpdate objects
        """
        data = {}
        for num in number_list:
            data['numbers[{}][mou]'.format(num.number)] = num.mou
        response = self.__make_api_request('POST', self.__url.phonenumbers_order_url(), data=data)
        for x in range(0, len(response)):
            response[x] = responses.PhoneNumberUpdate(**response[x])
        return response

    def get_local_phonunumbers_count(self):
        """
            Get a count of local Phone Numbers in the organization
        :return: int, Count of local Phone Numbers
        """
        response = self.__make_api_request('GET', self.__url.phonenumbers_localcount_url())
        return int(response['TOTAL'])

    def get_tollfree_phonenumbers_count(self):
        """
            Get a count of Toll-Free Phone Numbers in the organization
        :return: int, Count of Toll-Free Phone Numbers
        """
        response = self.__make_api_request('GET', self.__url.phonenumbers_tfcount_url())
        return int(response['TOTAL'])

    def get_sms_receipts(self, items_per_page=10, page_offset=0, query: str = None, search: Dict = None,
                         sort: List = None):
        """
            Get a list of received SMS/MMS messages
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param query: string, wildcard search on all string fields
        :param search: dict, format 'field':'query'
        :param sort: list[string], list of fields to sort, prefix a '-' for descending sort
        :return: list[SMSMessage], list of SMSMessage objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if query:
            parameters += '&filter[query]={}'.format(query)
        if search:
            for field in search:
                parameters += '&filter[{}]={}'.format(field, search[field])
        if sort:
            parameters += '&sort={}'.format(sort[0])
            for x in range(1, len(sort)):
                parameters += ',{}'.format(sort[x])
        response = self.__make_api_request('GET', self.__url.smsreceipts_url() + parameters)
        for x in range(0, len(response)):
            response[x]['time'] = datetime.strptime(response[x]['time'], SKYETEL_DATESTRING)
            response[x]['cost'] = float(response[x]['cost'])
            response[x]['org']['account_number'] = int(response[x]['org']['account_number'])
            response[x]['org']['support_pin'] = int(response[x]['org']['support_pin'])
            response[x]['org']['balance'] = float(response[x]['org']['balance'])
            response[x]['org']['auto_recharge_reserve'] = float(response[x]['org']['auto_recharge_reserve'])
            response[x]['org'] = responses.ExtendedOrganization(**response[x]['org'])
            response[x] = responses.SMSMessage(**response[x])
        return response

    def get_endpoint_health(self, items_per_page: int = 10, page_offset: int = 0):
        """
            Get a list of all Endpoints and their associated health status
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :return: list[EndpointHealth], list of EndpointHealth objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        response = self.__make_api_request('GET', self.__url.endpoint_health_url() + parameters)
        for x in range(0, len(response)):
            response[x] = responses.EndpointHealth(**response[x])
        return response

    def get_daily_traffic_counts(self, items_per_page: int = 10, page_offset: int = 0, start_time_min: datetime = None,
                                 start_time_max: datetime = None, tz_string: str = None):
        """
            Get a list of Traffic Counts per-day between two specified dates
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param start_time_min: datetime, filters data after this date
        :param start_time_max: datetime, filters data before this date
        :param tz_string: string, standard Time Zone string (ex. America/New_York)
        :return: list[TrafficCount], list of TrafficCount objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if start_time_min:
            parameters += '&start_time_min={}'.format(start_time_min.strftime(SKYETEL_DATESTRING))
        if start_time_max:
            parameters += '&start_time_max={}'.format(start_time_max.strftime(SKYETEL_DATESTRING))
        if tz_string:
            parameters += '&tz={}'.format(tz_string)
        response = self.__make_api_request('GET', self.__url.traffic_count_url() + parameters)
        for x in range(0, len(response)):
            response[x]['date'] = datetime.strptime(response[x]['date'], SKYETEL_DATESTRING)
            response[x] = responses.TrafficCount(**response[x])
        return response

    def get_daily_traffic_channels(self, items_per_page: int = 10, page_offset: int = 0,
                                   start_time_min: datetime = None,
                                   start_time_max: datetime = None, tz_string: str = None):
        """
            Get a list of Channels used per-day between two specified dates
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param start_time_min: datetime, filters data after this date
        :param start_time_max: datetime, filters data before this date
        :param tz_string: string, standard Time Zone string (ex. America/New_York)
        :return: list[ChannelCount], list of ChannelCount objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if start_time_min:
            parameters += '&start_time_min={}'.format(start_time_min.strftime(SKYETEL_DATESTRING))
        if start_time_max:
            parameters += '&start_time_max={}'.format(start_time_max.strftime(SKYETEL_DATESTRING))
        if tz_string:
            parameters += '&tz={}'.format(tz_string)
        response = self.__make_api_request('GET', self.__url.channel_count_url() + parameters)
        for x in range(0, len(response)):
            response[x]['date'] = datetime.strptime(response[x]['date'], SKYETEL_DATESTRING)
            response[x]['channel_count'] = int(response[x]['channel_count'])
            response[x] = responses.ChannelCount(**response[x])
        return response

    def get_hourly_call_count(self, items_per_page: int = 10, page_offset: int = 0,
                              start_time_min: datetime = None, start_time_max: datetime = None, tz_string: str = None):
        """
            Get a list of Calls placed per-hour between two specified dates
        :param items_per_page: integer, defaults to 10 records returned per request
        :param page_offset: integer, combines with items_per_page
        :param start_time_min: datetime, filters data after this date
        :param start_time_max: datetime, filters data before this date
        :param tz_string: string, standard Time Zone string (ex. America/New_York)
        :return: list[CallCount], list of CallCount objects
        """
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if start_time_min:
            parameters += '&start_time_min={}'.format(start_time_min.strftime(SKYETEL_DATESTRING))
        if start_time_max:
            parameters += '&start_time_max={}'.format(start_time_max.strftime(SKYETEL_DATESTRING))
        if tz_string:
            parameters += '&tz={}'.format(tz_string)
        response = self.__make_api_request('GET', self.__url.traffic_hourly_url() + parameters)
        for x in range(0, len(response)):
            response[x]['date'] = datetime.strptime(response[x]['date'], SKYETEL_TIMESTRING)
            response[x]['call_count'] = int(response[x]['call_count'])
            response[x] = responses.CallCount(**response[x])
        return response

    def get_tenant_statements(self, year=None, month=None):
        """
            Get all Tenant Statements in a given month. Defaults to current month
        :param year: integer, four digit year of the statement month
        :param month: integer, single or double digit, with January corresponding to 1
        :return: list[TenantStatement], list of TenantStatement objects
        """
        parameters = '?'
        if year:
            parameters += 'year={}'.format(year)
            if month:
                parameters += '&'
        if month:
            parameters += 'month={}'.format(month)
        response = self.__make_api_request('GET', self.__url.tenant_statements_url()+parameters)
        for x in range(0, len(response)):
            response[x]['month'] = datetime.strptime(response[x]['month'], SKYETEL_DATESTRING)
            response[x]['org'] = responses.Organization(org_id=response[x]['org']['id'],
                                                        org_name=response[x]['org']['org_name'])
            response[x]['tenant'] = responses.Tenant(**response[x]['tenant'])
            response[x]['fields']['totals']['phone_numbers'] = \
                responses.TenantPhoneNumberTotals(**response[x]['fields']['totals']['phone_numbers'])
            response[x]['fields']['totals'] = responses.TenantStatementTotals(**response[x]['fields']['totals'])
            response[x] = responses.TenantStatement(id=response[x]['id'], month=response[x]['month'],
                                                    org=response[x]['org'], tenant=response[x]['tenant'],
                                                    totals=response[x]['fields']['totals'])
        return response

    def get_tenant_invoices(self):
        """
            Get all Tenant Invoices
        :return: list[TenantInvoice], list of TenantInvoice objects
        """
        response = self.__make_api_request('GET', self.__url.tenant_invoices_url())
        for x in range(0, len(response)):
            response[x]['scheduled_date'] = datetime.strptime(response[x]['scheduled_date'], SKYETEL_TIMESTRING)
            response[x] = responses.TenantInvoice(**response[x])
        return response
