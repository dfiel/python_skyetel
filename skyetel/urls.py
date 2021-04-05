class URLs:
    def __init__(self):
        self.__base_url = "https://api.skyetel.com/v1"

        self.__audio_recordings = "/audio_recordings"
        self.__audio_recordings_download = "/audio_recordings/{id}/download"
        self.__audio_transcriptions = "/audio_transcriptions"
        self.__audio_transcriptions_download = "/audio_transcriptions/{id}/download"

        self.__balance = "/billing/balance"

        self.__endpoints = "/endpoints"
        self.__endpoint = self.__endpoints + "/{id}"

        self.__phonenumbers = "/phonenumbers"
        self.__phonenumbers_e911address = "/phonenumbers/{id}/e911address"
        self.__phonenumbers_offnetwork = "/phonenumbers/off-network"
        self.__phonenumber = "/phonenumbers/{id}"
        self.__phonenumbers_search = "/phonenumbers/order/search"
        self.__phonenumbers_ratecenters = "/phonenumbers/order/rate_centers"
        self.__phonenumbers_order = "/phonenumbers/order"

        self.__phonenumbers_count_local = "/stats/phonenumbers/local"
        self.__phonenumbers_count_tollfree = "/stats/phonenumbers/toll-free"

        self.__sms_receipts = "/smsreceipts"

        self.__stats_iphealth = "/stats/iphealth"
        self.__stats_orgstatement = "/stats/org/statement"
        self.__stats_traffic = "/stats/org/traffic/total-counts"
        self.__stats_channels = "/stats/org/traffic/channels"
        self.__stats_traffic_hourly = "/stats/org/traffic/most-active-hour"

        self.__tenant_statements = "/stats/org/tenant-statements"
        self.__tenant_invoices = "/tenants/billing"
        self.__tenant_invoice = "/tenants/{id}/billing"
        self.__tenant_products = "/tenants/billing-products"
        self.__tenants = "/tenants"
        self.__tenant = "/tenants/{id}"
        self.__tenant_allendpoints = "/tenants/endpoints"
        self.__tenant_endpoints = "/tenants/{id}/endpoints"
        self.__tenant_endpoint = "/tenants/{id}/endpoints/{endpoint_id}"
        self.__tenant_features = "/tenants/{id}/features"
        self.__tenant_monthlystats = "/tenants/{id}/monthly-stats"
        self.__tenant_currentstats = "/tenants/{id}/current-stats"
        self.__org_users = "/tenants/users"
        self.__tenant_users = "/tenants/{id}/users"
        self.__tenant_user = "/tenants/{id}/users/{userID}"

        self.__faxes = "/vfaxes"
        self.__fax_download = "/vfaxes/{id}/download"

    def audio_recordings_url(self):
        return self.__base_url + self.__audio_recordings

    def audio_recording_download_url(self, recording_id):
        return self.__base_url + self.__audio_recordings_download.format(id=recording_id)

    def audio_transcriptions_url(self):
        return self.__base_url + self.__audio_transcriptions

    def audio_transcription_download_url(self, transcription_id):
        return self.__base_url + self.__audio_transcriptions_download.format(id=transcription_id)

    def balance_url(self):
        return self.__base_url + self.__balance

    def endpoints_url(self):
        return self.__base_url + self.__endpoints

    def endpoint_url(self, endpoint_id):
        return self.__base_url + self.__endpoint.format(id=endpoint_id)

    def phonenumber_e911address_url(self, phonenumber_id):
        return self.__base_url + self.__phonenumbers_e911address.format(id=phonenumber_id)

    def phonenumbers_url(self):
        return self.__base_url + self.__phonenumbers

    def phonenumbers_offnetwork_url(self):
        return self.__base_url + self.__phonenumbers_offnetwork

    def phonenumber_url(self, phonenumber_id):
        return self.__base_url + self.__phonenumber.format(id=phonenumber_id)

    def phonenumbers_ordersearch_url(self):
        return self.__base_url + self.__phonenumbers_search

    def phonenumbers_ratecenters_url(self):
        return self.__base_url + self.__phonenumbers_ratecenters

    def phonenumbers_order_url(self):
        return self.__base_url + self.__phonenumbers_order

    def phonenumbers_localcount_url(self):
        return self.__base_url + self.__phonenumbers_count_local

    def phonenumbers_tfcount_url(self):
        return self.__base_url + self.__phonenumbers_count_tollfree

    def smsreceipts_url(self):
        return self.__base_url + self.__sms_receipts

    def endpoint_health_url(self):
        return self.__base_url + self.__stats_iphealth

    def organization_statement_url(self):
        return self.__base_url + self.__stats_orgstatement

    def traffic_count_url(self):
        return self.__base_url + self.__stats_traffic

    def channel_count_url(self):
        return self.__base_url + self.__stats_channels

    def traffic_hourly_url(self):
        return self.__base_url + self.__stats_traffic_hourly

    def tenant_statements_url(self):
        return self.__base_url + self.__tenant_statements

    def tenant_invoices_url(self):
        return self.__base_url + self.__tenant_invoices

    def tenant_invoice_url(self, tenant_id):
        return self.__base_url + self.__tenant_invoice.format(id=tenant_id)

    def tenant_products_url(self):
        return self.__base_url + self.__tenant_products

    def tenants_url(self):
        return self.__base_url + self.__tenants

    def tenant_url(self, tenant_id):
        return self.__base_url + self.__tenant.format(id=tenant_id)

    def tenant_allendpoints_url(self):
        return self.__base_url + self.__tenant_allendpoints

    def tenant_endpoints_url(self, tenant_id):
        return self.__base_url + self.__tenant_endpoints.format(id=tenant_id)

    def tenant_endpoint_url(self, tenant_id, endpoint_id):
        return self.__base_url + self.__tenant_endpoint.format(id=tenant_id, endpoint_id=endpoint_id)

    def tenant_features_url(self, tenant_id):
        return self.__base_url + self.__tenant_features.format(id=tenant_id)

    def tenant_monthlystats_url(self, tenant_id):
        return self.__base_url + self.__tenant_monthlystats.format(id=tenant_id)

    def tenant_currentstats_url(self, tenant_id):
        return self.__base_url + self.__tenant_currentstats.format(id=tenant_id)

    def org_users_url(self):
        return self.__base_url + self.__org_users

    def tenant_users_url(self, tenant_id):
        return self.__base_url + self.__tenant_users.format(id=tenant_id)

    def tenant_user_url(self, tenant_id, user_id):
        return self.__base_url + self.__tenant_user.format(id=tenant_id, userID=user_id)

    def faxes_url(self):
        return self.__base_url + self.__faxes

    def fax_download_url(self, fax_id):
        return self.__base_url + self.__fax_download.format(id=fax_id)
