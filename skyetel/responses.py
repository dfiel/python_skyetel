from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from . import errors


@dataclass(frozen=True)
class Organization:
    org_id: int
    org_name: str


@dataclass(frozen=True)
class AudioRecording:
    id: int
    insert_time: datetime
    start_time: datetime
    cost: float
    callid: str
    audio_file: str
    tenant_id: int
    org: Organization
    src_route: str
    dst_route: str
    size: int
    duration: float


@dataclass(frozen=True)
class AudioTranscription:
    id: int
    start_time: datetime
    insert_time: datetime
    cost: float
    callid: str
    transcription_file: str
    tenant_id: int
    org: Organization
    src_route: str
    dst_route: str
    duration: float


@dataclass(frozen=True)
class StatementTransaction:
    amount: float
    note: str
    transaction_date: datetime
    transaction_type: str
    subtotal: float
    tax: float


@dataclass(frozen=True)
class StatementTax:
    tax_auth: str
    description: str
    tax_amount: float
    is_exempt: bool


@dataclass(frozen=True)
class PhoneNumberTotals:
    local: int
    tollfree: int
    vanity: int
    message_enabled: int
    e911_enabled: int
    cnam_enabled: int


@dataclass(frozen=True)
class StatementTotals:
    outbound_conversational_minutes: float
    outbound_highcost_minutes: float
    outbound_highcost_cost: float
    outbound_conversational_cost: float
    dialer_traffic_minutes: float
    dialer_traffic_cost: float
    outbound_local_presence_traffic_minutes: float
    outbound_local_presence_traffic_cost: float
    outbound_pre_tax: float
    outbound_subtotal: float
    outbound_total: float
    outbound_minutes: float
    outbound_calls_count: int
    inbound_conversational_minutes: float
    inbound_conversational_cost: float
    cnam_count: int
    spamblock_count: int
    cnam_cost: float
    spamblock_cost: float
    inbound_local_presence_traffic_minutes: float
    inbound_local_presence_traffic_cost: float
    inbound_toll_free_traffic_minutes: float
    inbound_toll_free_traffic_cost: float
    inbound_pre_tax: float
    inbound_subtotal: float
    inbound_total: float
    inbound_minutes: float
    inbound_calls_count: int
    transcription_cost: float
    transcription_count: int
    audio_recording_cost: float
    audio_recording_count: int
    audio_transcription_cost: float
    audio_transcription_count: int
    vfax_cost: float
    vfax_count: int
    received_sms_cost: float
    received_sms_count: int
    sent_sms_cost: float
    sent_sms_count: int
    received_mms_cost: float
    received_mms_count: int
    sent_mms_cost: float
    sent_mms_count: int
    transactions_cost: float
    transactions_non_tax_cost: float
    transactions_total_cost: float
    phone_numbers: PhoneNumberTotals
    total_sms_mms_cost: float
    total_features_cost: float
    subtotal: float
    total_taxes: float
    total_cost: float


@dataclass(frozen=True)
class BillingStatement:
    statement: StatementTotals
    taxes: List[StatementTax]
    transactions: List[StatementTransaction]


@dataclass(frozen=True)
class EndpointGroup:
    id: int
    name: str


@dataclass(frozen=True)
class Endpoint:
    id: int
    ip: str
    endpoint_id: str
    port: int
    transport: str
    flags: int
    priority: int
    description: str
    endpoint_group: EndpointGroup
    org: Organization


@dataclass(frozen=True)
class E911Address:
    id: int
    caller_name: str
    address1: str
    address2: str
    community: str
    state: str
    postal_code: int


@dataclass(frozen=True)
class Tenant:
    id: int
    tenant_code: str
    name: str


@dataclass(frozen=True)
class Origination:
    id: int
    t38: None


@dataclass(frozen=True)
class ExtendedOrganization:
    id: int
    active: bool
    authorized_tier: int
    account_number: int
    support_pin: int
    org_name: str
    website: str
    transcription_password: str
    phone_number: str
    billing_postal_code: str
    billing_alert_email: str
    billing_alert_sms: str
    uptime_alert_email: str
    uptime_alert_sms: str
    address: str
    balance: float
    auto_recharge_reserve: float
    tags: List


@dataclass(frozen=True)
class PhoneNumber:
    id: int
    number: int
    forward: int
    failover: int
    category: str
    note: str
    endpoint_group: EndpointGroup
    tenant: Tenant
    origination: Origination
    localpresence: None
    localpresence_principle: None
    e911address: E911Address
    alg: int
    vanity: bool
    exotic: bool
    tn_format: int
    failure_strategy: int
    e911_enabled: bool
    off_network: bool
    cnam_enabled: bool
    spamblock_enabled: bool
    spamblock_passthru: bool
    spamblock_cnam_prepend: bool
    spamblock_risk_score: int
    spamblock_allow_unknown: bool
    record_calls: int
    spamblock_bot: int
    spamblock_bot_contact_email: str
    vfax_enabled: bool
    vfax_external_enabled: bool
    vfax_routing_enabled: bool
    conference_bridge_enabled: bool
    block_nocid: bool
    message_enabled: bool
    tier_enabled: int
    intl_balance: float
    intl_reserve: float
    lifecycle_state: str
    portin_id: int
    sip_credential: None
    org: ExtendedOrganization


@dataclass(frozen=True)
class OffNetworkPhoneNumber:
    id: int
    number: int


@dataclass
class PhoneNumberUpdate:
    block_nocid: bool = None
    vfax_external_enabled: bool = None
    vfax_enabled: bool = None
    conference_bridge_enabled: bool = None
    record_calls: bool = None
    spamblock_bot_contact_email: str = None
    spamblock_bot: int = None
    spamblock_risk_score: int = None
    spamblock_passthru: bool = None
    number: str = None
    forward: str = None
    failover: str = None
    note: str = None
    alg: int = None
    e911_enabled: bool = None
    off_network: bool = None
    cnam_enabled: bool = None
    spamblock_enabled: bool = None
    message_enabled: bool = None
    tn_format: int = None
    failure_strategy: int = None
    tier_enabled: int = None
    intl_balance: float = None
    intl_reserve: float = None
    endpoint_group_id: int = None
    tenant_id: int = None
    localpresence_id: int = None


@dataclass
class PhoneNumberFilter:
    states: List[str] = field(default_factory=list)
    npas: List[int] = field(default_factory=list)
    nxxs: List[int] = field(default_factory=list)
    category: int = 1
    consecutive: int = None
    quantity: int = 1
    vanity: int = None
    tnMask: str = None
    tnWildcard: str = None
    lata: int = None
    rateCenter: str = None
    sequential: bool = None
    province: str = None
    city: str = None
    postalCode: int = None
    radius: int = None
    localCallingArea: bool = None

    def validate(self):
        if (self.rateCenter and self.city) or (self.rateCenter and self.postalCode) or (self.city and self.postalCode):
            raise errors.DataValidityError("Rate center, city, and postal code are mutually exclusive")

        if self.city and not self.states:
            raise errors.DataValidityError("If city is specified, the state must be specified")

        if self.radius and not((self.city and self.province) or self.postalCode):
            raise errors.DataValidityError("Radius is only valid if city and province or zip are specified")

        if (self.radius and self.localCallingArea) or (self.radius and self.sequential) or (self.localCallingArea
                                                                                            and self.sequential):
            raise errors.DataValidityError("Radius, local, and sequential are mutually exclusive")

        if self.localCallingArea and not (self.tnMask or self.tnWildcard or self.rateCenter
                                          or (self.city and self.province) or self.postalCode):
            err = "If local is specified, one of the following must be true:\n tnMask or tnWildcard specify the " \
                  "NPANXX (first six digits)\n rateCenter is specified\n city and province are specified (without a " \
                  "radius)\n postal Code is specified (without a radius) "
            raise errors.DataValidityError(err)

    def params(self):
        self.validate()
        params = '?'
        if self.states:
            for state in self.states:
                params += 'filter[states][]={}&'.format(str(state))
        if self.npas:
            for npa in self.npas:
                params += 'filter[npas][]={}&'.format(str(npa))
        if self.nxxs:
            for nxx in self.nxxs:
                params += 'filter[nxxs][]={}&'.format(str(nxx))
        if self.category:
            params += 'filter[category]={}&'.format(str(self.category))
        if self.quantity:
            params += 'filter[quantity]={}&'.format(str(self.quantity))
        if self.tnMask:
            params += 'filter[tnMask]={}&'.format(str(self.tnMask))
        if self.tnWildcard:
            params += 'filter[tnWildcard]={}&'.format(str(self.tnWildcard))
        if self.lata:
            params += 'filter[lata]={}&'.format(str(self.lata))
        if self.rateCenter:
            params += 'filter[rateCenter]={}&'.format(str(self.rateCenter))
        if self.sequential:
            params += 'filter[sequential]={}&'.format(str(self.sequential).lower())
        if self.province:
            params += 'filter[province]={}&'.format(str(self.province))
        if self.city:
            params += 'filter[city]={}&'.format(str(self.city))
        if self.postalCode:
            params += 'filter[postalCode]={}&'.format(str(self.postalCode))
        if self.radius:
            params += 'filter[radius]={}&'.format(str(self.radius))
        if self.localCallingArea:
            params += 'filter[localCallingArea]={}'.format(str(self.localCallingArea).lower())
        return params


@dataclass(frozen=True)
class RateCenter:
    rateCenter: str
    market: str
    lata: int


@dataclass(frozen=True)
class NumberPurchase:
    number: str
    mou: int


@dataclass(frozen=True)
class SMSMessage:
    id: int
    org: ExtendedOrganization
    time: datetime
    flag_attachment: bool
    flag_delivered: bool
    from_phonenumber: str
    to_phonenumber: str
    fwd_to_phonenumber: str
    fwd_to_email: str
    src_tenant_id: int
    dst_tenant_id: int
    cost: float
    delivery_state: str


@dataclass(frozen=True)
class EndpointHealth:
    ip: str
    transport: str
    description: str
    alert: bool
    monitor: bool
    enhanced_monitor: bool
    channel_threshold: int
    org_name: str
    region1: int
    region2: int
    region3: int
    region4: int


@dataclass(frozen=True)
class TrafficCount:
    date: datetime
    inbound_minutes: int
    outbound_minutes: int
    inbound_count: int
    outbound_count: int
    total_billing_cost: float


@dataclass(frozen=True)
class ChannelCount:
    date: datetime
    channel_count: int


@dataclass(frozen=True)
class CallCount:
    date: datetime
    call_count: int
