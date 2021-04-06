import requests

from . import errors, urls


class Skyetel:
    def __init__(self, x_auth_sid, x_auth_secret):
        self.__x_auth_sid = x_auth_sid
        self.__x_auth_secret = x_auth_secret
        self.__url = urls.URLs()

        self.__session = requests.Session()
        self.__session.headers = {'X-AUTH-SID': x_auth_sid, 'X-AUTH-SECRET': x_auth_secret}

    def __make_api_request(self, request_type, endpoint, data=None):
        try:
            if request_type == 'GET':
                response = self.__session.get(endpoint)

            elif request_type == 'POST':
                response = self.__session.post(endpoint, data=data)

            elif request_type == 'PATCH':
                response = self.__session.patch(endpoint, data=data)

            else:
                raise AttributeError('Invalid Request Type')

            response.raise_for_status()

        except (requests.ConnectionError, requests.Timeout) as e:
            raise errors.Unavailable() from e

        except requests.exceptions.HTTPError:
            content = response.json()
            raise errors.APIError(content['ERROR'])

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
        return response

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
        return response

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
        return response

    def get_endpoints_list(self, items_per_page=10, page_offset=0):
        parameters = '?page[limit]={}&page[offset]={}'.format(items_per_page, page_offset)
        response = self.__make_api_request('GET', self.__url.endpoints_url()+parameters)
        return response

    def create_endpoint(self, ip, priority, description, endpoint_group_id, endpoint_group_name, endpoint_id=None,
                        port=5060, transport="UDP"):
        parameters = {'ip': ip, 'port': port, 'transport': transport, 'priority': priority, 'description': description,
                      'endpoint_group_id': endpoint_group_id, 'endpoint_group_name': endpoint_group_name}
        if endpoint_id:
            parameters['endpoint_id'] = endpoint_id
        response = self.__make_api_request('POST', self.__url.endpoints_url(), data=parameters)
        return response
