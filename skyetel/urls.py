class URLs:
    def __init__(self):
        self.base_url = "https://api.skyetel.com/v1"

        self.audio_recordings = "/audio_recordings"
        self.audio_recordings_download = "/audio_recordings/{id}/download"
        self.audio_transcriptions = "/audio_transcriptions"
        self.audio_transcriptions_download = "/audio_transcriptions/{id}/download"

        self.balance = "/billing/balance"

        self.endpoints = "/endpoints"
        self.endpoint = self.endpoints+"/{id}"

        self.phonenumbers = "/phonenumbers"
        self.phonenumbers_e911address = "/phonenumbers/{id}/e911address"
        self.phonenumbers_offnetwork = "/phonenumbers/off-network"
        self.phonenumber = "/phonenumbers/{id}"
        self.phonenumbers_search = "/phonenumbers/order/search"
        self.phonenumbers_ratecenters = "/phonenumbers/order/rate_centers"
        self.phonenumbers_order = "/phonenumbers/order"

        self.phonenumbers_count_local = "/stats/phonenumbers/local"
        self.phonenumbers_count_tollfree = "/stats/phonenumbers/toll-free"

        self.sms_receipts = "/smsreceipts"

        self.stats_iphealth = "/stats/iphealth"
        self.stats_orgstatement = "/stats/org/statement"
        self.stats_traffic = "/stats/org/traffic/total-counts"
        self.stats_channels = "/stats/org/traffic/channels"
        self.stats_traffic_hourly = "/stats/org/traffic/most-active-hour"

        self.tenant_statements = "/stats/org/tenant-statements"
        self.tenant_invoices = "/tenants/billing"
        self.tenant_invoice = "/tenants/{id}/billing"
        self.tenant_products = "/tenants/billing-products"
        self.tenants = "/tenants"
        self.tenant = "/tenants/{id}"
        self.tenant_allendpoints = "/tenants/endpoints"
        self.tenant_endpoints = "/tenants/{id}/endpoints"
        self.tenant_endpoint = "/tenants/{id}/endpoints/{endpoint_id}"
        self.tenant_features = "/tenants/{id}/features"
        self.tenant_monthlystats = "/tenants/{id}/monthly-stats"
        self.tenant_currentstats = "/tenants/{id}/current-stats"
        self.org_users = "/tenants/users"
        self.tenant_users = "/tenants/{id}/users"
        self.tenant_user = "/tenants/{id}/users/{userID}"

        self.faxes = "/vfaxes"
        self.fax_download = "/vfaxes/{id}/download"

    def audio_recordings_url(self):
        return self.base_url+self.audio_recordings

    def audio_recording_download_url(self, recording_id):
        return self.base_url+self.audio_recordings_download.format(id=recording_id)

    def audio_transcriptions_url(self):
        return self.base_url+self.audio_transcriptions

    def audio_transcription_download_url(self, transcription_id):
        return self.base_url+self.audio_transcriptions_download.format(id=transcription_id)

    def balance_url(self):
        return self.base_url+self.balance

    def endpoints_url(self):
        return self.base_url+self.endpoints

    def endpoint_url(self, endpoint_id):
        return self.base_url+self.endpoint.format(id=endpoint_id)

    def phonenumber_e911address_url(self, phonenumber_id):
        return self.base_url+self.phonenumbers_e911address.format(id=phonenumber_id)

    def phonenumbers_url(self):
        return self.base_url+self.phonenumbers

    def phonenumbers_offnetwork_url(self):
        return self.base_url+self.phonenumbers_offnetwork

    def phonenumber_url(self, phonenumber_id):
        return self.base_url+self.phonenumber.format(id=phonenumber_id)

    def phonenumbers_ordersearch_url(self):
        return self.base_url+self.phonenumbers_search

    def phonenumbers_ratecenters_url(self):
        return self.base_url+self.phonenumbers_ratecenters

    def phonenumbers_order_url(self):
        return self.base_url+self.phonenumbers_order

    def phonenumbers_localcount_url(self):
        return self.base_url+self.phonenumbers_count_local

    def phonenumbers_tfcount_url(self):
        return self.base_url+self.phonenumbers_count_tollfree

    def smsreceipts_url(self):
        return self.base_url+self.sms_receipts

    def endpoint_health_url(self):
        return self.base_url+self.stats_iphealth

    def organization_statement_url(self):
        return self.base_url+self.stats_orgstatement

    def traffic_count_url(self):
        return self.base_url+self.stats_traffic

    def channel_count_url(self):
        return self.base_url+self.stats_channels

    def traffic_hourly_url(self):
        return self.base_url+self.stats_traffic_hourly

    def tenant_statements_url(self):
        return self.base_url+self.tenant_statements

    def tenant_invoices_url(self):
        return self.base_url+self.tenant_invoices

    def tenant_invoice_url(self, tenant_id):
        return self.base_url+self.tenant_invoice.format(id=tenant_id)

    def tenant_products_url(self):
        return self.base_url+self.tenant_products

    def tenants_url(self):
        return self.base_url+self.tenants

    def tenant_url(self, tenant_id):
        return self.base_url+self.tenant.format(id=tenant_id)

    def tenant_allendpoints_url(self):
        return self.base_url+self.tenant_allendpoints

    def tenant_endpoints_url(self, tenant_id):
        return self.base_url+self.tenant_endpoints.format(id=tenant_id)

    def tenant_endpoint_url(self, tenant_id, endpoint_id):
        return self.base_url+self.tenant_endpoint.format(id=tenant_id, endpoint_id=endpoint_id)

    def tenant_features_url(self, tenant_id):
        return self.base_url+self.tenant_features.format(id=tenant_id)

    def tenant_monthlystats_url(self, tenant_id):
        return self.base_url+self.tenant_monthlystats.format(id=tenant_id)

    def tenant_currentstats_url(self, tenant_id):
        return self.base_url+self.tenant_currentstats.format(id=tenant_id)

    def org_users_url(self):
        return self.base_url+self.org_users

    def tenant_users_url(self, tenant_id):
        return self.base_url+self.tenant_users.format(id=tenant_id)

    def tenant_user_url(self, tenant_id, user_id):
        return self.base_url+self.tenant_user.format(id=tenant_id, userID=user_id)

    def faxes_url(self):
        return self.base_url+self.faxes

    def fax_download_url(self, fax_id):
        return self.base_url+self.fax_download.format(id=fax_id)
