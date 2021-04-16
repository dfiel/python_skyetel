import requests
from ratelimit import limits
from datetime import datetime
from typing import List, Dict
from dataclasses import asdict

from . import errors, urls, responses

SKYETEL_DATESTRING = '%Y-%m-%dT%H:%M:%S+00:00'


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
        response = self.__make_api_request('GET', self.__url.audio_recording_download_url(recording_id))
        return response['download_url']

    def get_audio_transcriptions_list(self, items_per_page=10, page_offset=0, query=None, search=None, sort=None):
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
        response = self.__make_api_request('GET', self.__url.audio_transcription_download_url(transcription_id))
        return response['download_url']

    def get_audio_transcription_text(self, transcription_id):
        response = self.__make_api_request('GET', self.__url.audio_transcription_download_url(transcription_id))
        url = response['download_url']
        transcript = requests.get(url).json()
        return transcript

    def get_billing_balance(self):
        response = self.__make_api_request('GET', self.__url.balance_url())
        return float(response['BALANCE'])

    def get_organization_statement(self, year=None, month=None):
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
        parameters = {'ip': ip, 'port': port, 'transport': transport, 'priority': priority, 'description': description,
                      'endpoint_group_id': endpoint_group_id, 'endpoint_group_name': endpoint_group_name}
        response = self.__make_api_request('PATCH', self.__url.endpoint_url(endpoint_id), data=parameters)
        response['endpoint_group'] = responses.EndpointGroup(**response['endpoint_group'])
        response['org'] = responses.Organization(org_id=response['org']['id'],
                                                 org_name=response['org']['name'])
        response = responses.Endpoint(**response)
        return response

    def get_phonenumber_e911(self, phonenumber_id):
        response = self.__make_api_request('GET', self.__url.phonenumber_e911address_url(phonenumber_id))
        response = responses.E911Address(**response)
        return response

    def create_phonenumber_e911(self, phonenumber_id, caller_name, address1, address2, community, state, postal_code):
        parameters = {'caller_name': caller_name, 'address1': address1, 'address2': address2, 'community': community,
                      'state': state, 'postal_code': postal_code}
        response = self.__make_api_request('POST', self.__url.phonenumber_e911address_url(phonenumber_id),
                                           data=parameters)
        response = responses.E911Address(**response)
        return response

    def update_phonenumber_e911(self, phonenumber_id: int, caller_name, address1, address2, community, state,
                                postal_code):
        parameters = {'caller_name': caller_name, 'address1': address1, 'address2': address2, 'community': community,
                      'state': state, 'postal_code': postal_code}
        response = self.__make_api_request('PATCH', self.__url.phonenumber_e911address_url(phonenumber_id),
                                           data=parameters)
        response = responses.E911Address(**response)
        return response

    def get_phonenumbers(self, items_per_page=10, page_offset=0, query: str = None, search: Dict = None,
                         sort: List = None):
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
            response[x]['endpoint_group'] = responses.EndpointGroup(**response[x]['endpoint_group'])
            response[x]['tenant'] = responses.Tenant(**response[x]['tenant'])
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
        parameters = {'number': str(number)}
        response = self.__make_api_request('POST', self.__url.phonenumbers_offnetwork_url(), json=parameters)
        response = responses.OffNetworkPhoneNumber(**response)
        return response

    def update_phonenumber(self, phonenumber_id: int, update_data: responses.PhoneNumberUpdate):
        data = asdict(update_data)
        response = self.__make_api_request('PATCH', self.__url.phonenumber_url(phonenumber_id), data=data)
        response = responses.PhoneNumberUpdate(**response)
        return response

    def get_available_phonenumbers(self, search_filter: responses.PhoneNumberFilter = None):
        params = ''
        if search_filter:
            params = search_filter.params()
        response = self.__make_api_request('GET', self.__url.phonenumbers_ordersearch_url() + params)
        return response

    def get_rate_centers(self, state: str = None):
        params = ''
        if state:
            params = '?state={}'.format(state)
        response = self.__make_api_request('GET', self.__url.phonenumbers_ratecenters_url() + params)
        for x in range(0, len(response)):
            response[x] = responses.RateCenter(**response[x])
        return response

    def order_phonenumbers(self, number_list: List[responses.NumberPurchase]):
        data = {}
        for num in number_list:
            data['numbers[{}][mou]'.format(num.number)] = num.mou
        response = self.__make_api_request('POST', self.__url.phonenumbers_order_url(), data=data)
        for x in range(0, len(response)):
            response[x] = responses.PhoneNumberUpdate(**response[x])
        return response

    def get_local_phonunumbers_count(self):
        response = self.__make_api_request('GET', self.__url.phonenumbers_localcount_url())
        return int(response['TOTAL'])

    def get_tollfree_phonenumbers_count(self):
        response = self.__make_api_request('GET', self.__url.phonenumbers_tfcount_url())
        return int(response['TOTAL'])

    def get_sms_receipts(self, items_per_page=10, page_offset=0, query: str = None, search: Dict = None,
                         sort: List = None):
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
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        response = self.__make_api_request('GET', self.__url.endpoint_health_url() + parameters)
        for x in range(0, len(response)):
            response[x] = responses.EndpointHealth(**response[x])
        return response

    def get_daily_traffic_counts(self, items_per_page: int = 10, page_offset: int = 0, start_time_min: datetime = None,
                                 start_time_max: datetime = None, tz_string: str = None):
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
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        if start_time_min:
            parameters += '&start_time_min={}'.format(start_time_min.strftime(SKYETEL_DATESTRING))
        if start_time_max:
            parameters += '&start_time_max={}'.format(start_time_max.strftime(SKYETEL_DATESTRING))
        if tz_string:
            parameters += '&tz={}'.format(tz_string)
        response = self.__make_api_request('GET', self.__url.traffic_hourly_url() + parameters)
        for x in range(0, len(response)):
            response[x]['date'] = datetime.strptime(response[x]['date'], SKYETEL_DATESTRING)
            response[x]['call_count'] = int(response[x]['call_count'])
            response[x] = responses.CallCount(**response[x])
        return response
