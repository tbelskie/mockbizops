"""Marketing domain models."""
from app.domains.marketing.models.ad_account import AdAccount, AdAccountStatus
from app.domains.marketing.models.campaign import Campaign, CampaignObjective, CampaignStatus
from app.domains.marketing.models.ad_set import AdSet, OptimizationGoal, BillingEvent, AdSetStatus
from app.domains.marketing.models.creative import Creative
from app.domains.marketing.models.ad import Ad, AdStatus
from app.domains.marketing.models.ad_insight import AdInsight
from app.domains.marketing.models.influencer import Influencer, InfluencerStatus, PaymentTerms
from app.domains.marketing.models.promo_code import PromoCode, DiscountType, PromoCodeStatus
from app.domains.marketing.models.promo_code_usage import PromoCodeUsage
from app.domains.marketing.models.campaign_influencer import CampaignInfluencer, InfluencerRole
from app.domains.marketing.models.influencer_payout import InfluencerPayout, PayoutStatus, PaymentMethod
from app.domains.marketing.models.influencer_content import InfluencerContent, ContentPlatform, ContentType

__all__ = [
    "AdAccount",
    "AdAccountStatus",
    "Campaign",
    "CampaignObjective",
    "CampaignStatus",
    "AdSet",
    "OptimizationGoal",
    "BillingEvent",
    "AdSetStatus",
    "Creative",
    "Ad",
    "AdStatus",
    "AdInsight",
    "Influencer",
    "InfluencerStatus",
    "PaymentTerms",
    "PromoCode",
    "DiscountType",
    "PromoCodeStatus",
    "PromoCodeUsage",
    "CampaignInfluencer",
    "InfluencerRole",
    "InfluencerPayout",
    "PayoutStatus",
    "PaymentMethod",
    "InfluencerContent",
    "ContentPlatform",
    "ContentType",
]
