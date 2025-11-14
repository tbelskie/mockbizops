"""Marketing domain schemas."""
from app.domains.marketing.schemas.common import PaginatedResponse
from app.domains.marketing.schemas.influencer import (
    InfluencerBase,
    InfluencerResponse,
    InfluencerListResponse
)
from app.domains.marketing.schemas.campaign import (
    CampaignResponse,
    CampaignListResponse
)
from app.domains.marketing.schemas.promo_code import (
    PromoCodeResponse,
    PromoCodeListResponse,
    PromoCodeUsageResponse
)
from app.domains.marketing.schemas.ad_insight import (
    AdInsightResponse,
    AdInsightListResponse
)
from app.domains.marketing.schemas.influencer_payout import (
    InfluencerPayoutResponse,
    InfluencerPayoutListResponse
)

__all__ = [
    "PaginatedResponse",
    "InfluencerBase",
    "InfluencerResponse",
    "InfluencerListResponse",
    "CampaignResponse",
    "CampaignListResponse",
    "PromoCodeResponse",
    "PromoCodeListResponse",
    "PromoCodeUsageResponse",
    "AdInsightResponse",
    "AdInsightListResponse",
    "InfluencerPayoutResponse",
    "InfluencerPayoutListResponse",
]
