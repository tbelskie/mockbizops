"""Seed data for Good Bogey marketing domain."""
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from faker import Faker
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.domains.marketing.models import (
    AdAccount, AdAccountStatus,
    Campaign, CampaignObjective, CampaignStatus,
    AdSet, OptimizationGoal, BillingEvent, AdSetStatus,
    Creative,
    Ad, AdStatus,
    AdInsight,
    Influencer, InfluencerStatus, PaymentTerms,
    PromoCode, DiscountType, PromoCodeStatus,
    PromoCodeUsage,
    CampaignInfluencer, InfluencerRole,
    InfluencerPayout, PayoutStatus, PaymentMethod,
    InfluencerContent, ContentPlatform, ContentType
)

fake = Faker()


def create_ad_account(db: Session) -> AdAccount:
    """Create Good Bogey ad account."""
    account = AdAccount(
        account_id="act_goodbogey_2024",
        name="Good Bogey Golf Apparel",
        currency="USD",
        timezone="America/Los_Angeles",
        status=AdAccountStatus.ACTIVE
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def create_influencers(db: Session, count: int = 25) -> list[Influencer]:
    """Create golf influencers."""
    influencers = []

    # Golf-themed first names and last names
    golf_names = [
        ("Tiger", "Woods"), ("Phil", "Mickelson"), ("Rory", "McIlroy"),
        ("Brooks", "Koepka"), ("Dustin", "Johnson"), ("Jordan", "Spieth"),
        ("Justin", "Thomas"), ("Bryson", "DeChambeau"), ("Rickie", "Fowler"),
        ("Patrick", "Reed"), ("Tony", "Finau"), ("Xander", "Schauffele"),
    ]

    for i in range(count):
        if i < len(golf_names):
            first_name, last_name = golf_names[i]
        else:
            first_name = fake.first_name()
            last_name = fake.last_name()

        instagram_handle = f"{first_name.lower()}{last_name.lower()}golf"
        tiktok_handle = f"{first_name.lower()}.golf" if random.random() > 0.3 else None
        youtube_channel = f"{first_name} {last_name} Golf" if random.random() > 0.5 else None

        # Follower distribution: micro (1k-10k), mid (10k-100k), macro (100k-1M)
        tier = random.choices(
            ["micro", "mid", "macro"],
            weights=[0.5, 0.35, 0.15]
        )[0]

        if tier == "micro":
            follower_count = random.randint(1000, 10000)
            engagement_rate = Decimal(str(random.uniform(3.5, 8.0)))
            commission_rate = Decimal("0.15")
            flat_rate = Decimal(str(random.randint(100, 500)))
        elif tier == "mid":
            follower_count = random.randint(10000, 100000)
            engagement_rate = Decimal(str(random.uniform(2.0, 5.0)))
            commission_rate = Decimal("0.12")
            flat_rate = Decimal(str(random.randint(500, 2000)))
        else:  # macro
            follower_count = random.randint(100000, 1000000)
            engagement_rate = Decimal(str(random.uniform(1.0, 3.5)))
            commission_rate = Decimal("0.10")
            flat_rate = Decimal(str(random.randint(2000, 10000)))

        contract_start = date.today() - timedelta(days=random.randint(30, 365))
        contract_end = contract_start + timedelta(days=365)

        influencer = Influencer(
            first_name=first_name,
            last_name=last_name,
            email=f"{instagram_handle}@example.com",
            phone=fake.phone_number()[:20],
            instagram_handle=instagram_handle,
            tiktok_handle=tiktok_handle,
            youtube_channel=youtube_channel,
            follower_count=follower_count,
            engagement_rate=engagement_rate,
            contract_start_date=contract_start,
            contract_end_date=contract_end,
            commission_rate=commission_rate,
            flat_rate_per_post=flat_rate,
            payment_terms=random.choice(list(PaymentTerms)),
            tax_id=f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
            status=InfluencerStatus.ACTIVE if random.random() > 0.1 else InfluencerStatus.INACTIVE
        )
        influencers.append(influencer)

    db.add_all(influencers)
    db.commit()
    for inf in influencers:
        db.refresh(inf)

    return influencers


def create_campaigns(db: Session, ad_account: AdAccount, count: int = 8) -> list[Campaign]:
    """Create Good Bogey marketing campaigns."""
    campaign_names = [
        "Spring Collection Launch 2024",
        "Summer Golf Apparel Sale",
        "Fall/Winter Performance Wear",
        "Holiday Gift Guide - Golf Gear",
        "New Product Launch - ProDry Polo",
        "Brand Awareness - Golf Lifestyle",
        "Retargeting - Cart Abandoners",
        "Influencer Partnership Campaign"
    ]

    campaigns = []
    for i in range(min(count, len(campaign_names))):
        start_time = datetime.now() - timedelta(days=random.randint(30, 180))
        stop_time = start_time + timedelta(days=random.randint(30, 90)) if random.random() > 0.3 else None

        campaign = Campaign(
            campaign_id=f"cmp_{random.randint(100000000, 999999999)}",
            ad_account_id=ad_account.id,
            name=campaign_names[i],
            objective=random.choice([
                CampaignObjective.CONVERSIONS,
                CampaignObjective.TRAFFIC,
                CampaignObjective.BRAND_AWARENESS,
                CampaignObjective.CATALOG_SALES
            ]),
            status=random.choices(
                [CampaignStatus.ACTIVE, CampaignStatus.PAUSED],
                weights=[0.7, 0.3]
            )[0],
            daily_budget=Decimal(str(random.randint(100, 1000))),
            lifetime_budget=None,
            start_time=start_time,
            stop_time=stop_time
        )
        campaigns.append(campaign)

    db.add_all(campaigns)
    db.commit()
    for camp in campaigns:
        db.refresh(camp)

    return campaigns


def create_creatives(db: Session, count: int = 30) -> list[Creative]:
    """Create ad creatives for Good Bogey."""
    creative_titles = [
        "Swing in Style",
        "Performance Meets Fashion",
        "Elevate Your Game",
        "Golf Like a Pro",
        "The Perfect Fit",
        "Moisture-Wicking Technology",
        "UV Protection Golf Wear",
        "Stretch Fabric Innovation",
        "Classic Golf Style",
        "Modern Golf Apparel"
    ]

    creative_bodies = [
        "Discover our new ProDry collection. Stay cool and comfortable on the course.",
        "Premium golf apparel designed for performance. Shop now!",
        "Limited time offer: 20% off all polos and pants.",
        "Join the Good Bogey family. Gear that performs when it matters.",
        "Trusted by pros. Worn by champions. Good Bogey Golf.",
    ]

    ctas = ["shop_now", "learn_more", "sign_up", "get_offer"]

    creatives = []
    for i in range(count):
        creative = Creative(
            creative_id=f"cre_{random.randint(100000000, 999999999)}",
            name=f"Creative {i+1} - {random.choice(creative_titles)}",
            title=random.choice(creative_titles),
            body=random.choice(creative_bodies),
            image_url=f"https://cdn.goodbogey.com/ads/image_{i+1}.jpg",
            video_url=f"https://cdn.goodbogey.com/ads/video_{i+1}.mp4" if random.random() > 0.6 else None,
            call_to_action=random.choice(ctas),
            link_url="https://www.goodbogey.com/shop",
            instagram_permalink_url=f"https://www.instagram.com/p/{fake.lexify('??????????')}/"
        )
        creatives.append(creative)

    db.add_all(creatives)
    db.commit()
    for cre in creatives:
        db.refresh(cre)

    return creatives


def create_ad_sets_and_ads(
    db: Session,
    campaigns: list[Campaign],
    creatives: list[Creative]
) -> tuple[list[AdSet], list[Ad]]:
    """Create ad sets and ads."""
    ad_sets = []
    ads = []

    for campaign in campaigns:
        # 2-4 ad sets per campaign
        num_ad_sets = random.randint(2, 4)

        for j in range(num_ad_sets):
            targeting = {
                "age_min": 25,
                "age_max": 65,
                "genders": ["male", "female"],
                "interests": ["Golf", "Sports", "Outdoor Activities"],
                "locations": ["United States"]
            }

            ad_set = AdSet(
                ad_set_id=f"ads_{random.randint(100000000, 999999999)}",
                campaign_id=campaign.id,
                name=f"{campaign.name} - Ad Set {j+1}",
                optimization_goal=OptimizationGoal.CONVERSIONS,
                billing_event=BillingEvent.IMPRESSIONS,
                bid_amount=Decimal(str(random.uniform(5, 25))),
                daily_budget=Decimal(str(random.randint(50, 300))),
                targeting=targeting,
                status=campaign.status,
                start_time=campaign.start_time,
                stop_time=campaign.stop_time
            )
            ad_sets.append(ad_set)
            db.add(ad_set)
            db.flush()

            # 2-5 ads per ad set
            num_ads = random.randint(2, 5)
            for k in range(num_ads):
                creative = random.choice(creatives)

                ad = Ad(
                    ad_id=f"ad_{random.randint(100000000, 999999999)}",
                    ad_set_id=ad_set.id,
                    creative_id=creative.id,
                    name=f"{ad_set.name} - Ad {k+1}",
                    status=ad_set.status,
                    tracking_specs={"event": "purchase", "pixel_id": "12345"}
                )
                ads.append(ad)

    db.add_all(ads)
    db.commit()

    for ad_set in ad_sets:
        db.refresh(ad_set)
    for ad in ads:
        db.refresh(ad)

    return ad_sets, ads


def create_ad_insights(db: Session, ads: list[Ad]) -> list[AdInsight]:
    """Create performance metrics for ads."""
    insights = []

    for ad in ads:
        # Create daily insights for the past 30 days
        for days_ago in range(30):
            day = date.today() - timedelta(days=days_ago)

            impressions = random.randint(1000, 50000)
            clicks = int(impressions * random.uniform(0.01, 0.05))  # 1-5% CTR
            spend = Decimal(str(random.uniform(50, 500)))
            reach = int(impressions * random.uniform(0.6, 0.9))
            frequency = Decimal(str(impressions / reach)) if reach > 0 else Decimal("1.0")
            cpc = spend / clicks if clicks > 0 else Decimal("0")
            cpm = (spend / impressions) * 1000 if impressions > 0 else Decimal("0")
            ctr = Decimal(str((clicks / impressions) * 100)) if impressions > 0 else Decimal("0")
            conversions = int(clicks * random.uniform(0.02, 0.10))  # 2-10% conversion
            conversion_value = Decimal(str(conversions * random.uniform(50, 150)))

            insight = AdInsight(
                ad_id=ad.id,
                date_start=day,
                date_stop=day,
                impressions=impressions,
                clicks=clicks,
                spend=round(spend, 2),
                reach=reach,
                frequency=round(frequency, 2),
                cpc=round(cpc, 2),
                cpm=round(cpm, 2),
                ctr=round(ctr, 2),
                conversions=conversions,
                conversion_value=round(conversion_value, 2)
            )
            insights.append(insight)

    db.add_all(insights)
    db.commit()

    return insights


def create_promo_codes(db: Session, influencers: list[Influencer]) -> list[PromoCode]:
    """Create promo codes for influencers."""
    promo_codes = []

    for influencer in influencers:
        if influencer.status != InfluencerStatus.ACTIVE:
            continue

        # Each active influencer gets 1-2 promo codes
        num_codes = random.randint(1, 2)

        for i in range(num_codes):
            code_suffix = "10" if i == 0 else "15"
            code = f"{influencer.instagram_handle.upper()[:8]}{code_suffix}"

            promo_code = PromoCode(
                code=code,
                influencer_id=influencer.id,
                discount_type=DiscountType.PERCENTAGE,
                discount_value=Decimal(code_suffix),
                start_date=influencer.contract_start_date,
                end_date=influencer.contract_end_date,
                usage_limit=None,  # Unlimited
                usage_count=0,
                status=PromoCodeStatus.ACTIVE
            )
            promo_codes.append(promo_code)

    db.add_all(promo_codes)
    db.commit()
    for code in promo_codes:
        db.refresh(code)

    return promo_codes


def create_promo_code_usage(db: Session, promo_codes: list[PromoCode]) -> list[PromoCodeUsage]:
    """Create promo code usage records."""
    usage_records = []

    for promo_code in promo_codes:
        # Each promo code has been used 5-50 times
        num_uses = random.randint(5, 50)

        for _ in range(num_uses):
            used_at = datetime.now() - timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )

            order_value = Decimal(str(random.uniform(75, 350)))
            discount_amount = (order_value * promo_code.discount_value) / 100

            usage = PromoCodeUsage(
                promo_code_id=promo_code.id,
                used_at=used_at,
                order_id=f"ORD-{random.randint(100000, 999999)}",
                order_value=round(order_value, 2),
                discount_amount=round(discount_amount, 2),
                customer_id=f"CUST-{random.randint(1000, 9999)}" if random.random() > 0.3 else None
            )
            usage_records.append(usage)

        # Update usage count
        promo_code.usage_count = num_uses

    db.add_all(usage_records)
    db.commit()

    return usage_records


def create_campaign_influencers(
    db: Session,
    campaigns: list[Campaign],
    influencers: list[Influencer]
) -> list[CampaignInfluencer]:
    """Associate influencers with campaigns."""
    associations = []

    # Find the influencer partnership campaign
    influencer_campaign = next((c for c in campaigns if "Influencer" in c.name), campaigns[0])

    # Assign 5-10 influencers to the campaign
    selected_influencers = random.sample(
        [i for i in influencers if i.status == InfluencerStatus.ACTIVE],
        min(10, len([i for i in influencers if i.status == InfluencerStatus.ACTIVE]))
    )

    for i, influencer in enumerate(selected_influencers):
        role = InfluencerRole.PRIMARY if i < 2 else InfluencerRole.SECONDARY

        assoc = CampaignInfluencer(
            campaign_id=influencer_campaign.id,
            influencer_id=influencer.id,
            role=role
        )
        associations.append(assoc)

    db.add_all(associations)
    db.commit()

    return associations


def create_influencer_content(
    db: Session,
    influencers: list[Influencer],
    campaigns: list[Campaign],
    ads: list[Ad]
) -> list[InfluencerContent]:
    """Create influencer content posts."""
    content_posts = []

    for influencer in influencers:
        if influencer.status != InfluencerStatus.ACTIVE:
            continue

        # Each influencer has created 3-10 pieces of content
        num_posts = random.randint(3, 10)

        for _ in range(num_posts):
            platform = random.choice([ContentPlatform.INSTAGRAM, ContentPlatform.TIKTOK])
            post_type = random.choice([ContentType.POST, ContentType.REEL, ContentType.STORY])

            post_date = datetime.now() - timedelta(
                days=random.randint(1, 90),
                hours=random.randint(0, 23)
            )

            # Engagement metrics based on follower count
            base_reach = int(influencer.follower_count * random.uniform(0.3, 0.7))
            impressions = int(base_reach * random.uniform(1.2, 2.5))
            likes = int(impressions * float(influencer.engagement_rate) / 100)
            comments = int(likes * random.uniform(0.02, 0.08))
            shares = int(likes * random.uniform(0.01, 0.05))
            saves = int(likes * random.uniform(0.05, 0.15))

            engagement_rate = Decimal(str(
                ((likes + comments + shares + saves) / impressions) * 100
            )) if impressions > 0 else Decimal("0")

            content = InfluencerContent(
                influencer_id=influencer.id,
                campaign_id=random.choice(campaigns).id if random.random() > 0.5 else None,
                ad_id=random.choice(ads).id if random.random() > 0.7 else None,
                platform=platform,
                post_url=f"https://{'instagram.com' if platform == ContentPlatform.INSTAGRAM else 'tiktok.com'}/@{influencer.instagram_handle}/p/{fake.lexify('??????????')}/",
                post_type=post_type,
                post_date=post_date,
                impressions=impressions,
                likes=likes,
                comments=comments,
                shares=shares,
                saves=saves,
                engagement_rate=round(engagement_rate, 2)
            )
            content_posts.append(content)

    db.add_all(content_posts)
    db.commit()

    return content_posts


def create_influencer_payouts(db: Session, influencers: list[Influencer]) -> list[InfluencerPayout]:
    """Create influencer payout records."""
    payouts = []

    for influencer in influencers:
        if influencer.status != InfluencerStatus.ACTIVE:
            continue

        # Create 1-3 payout records for each influencer
        num_payouts = random.randint(1, 3)

        for i in range(num_payouts):
            period_end = date.today() - timedelta(days=i * 30)
            period_start = period_end - timedelta(days=30)

            # Calculate sales from their promo codes
            total_sales = Decimal(str(random.uniform(5000, 50000)))
            commission_amount = total_sales * influencer.commission_rate
            flat_fee = influencer.flat_rate_per_post * Decimal(str(random.randint(2, 6)))
            total_payout = commission_amount + flat_fee

            payout_status = random.choices(
                [PayoutStatus.PAID, PayoutStatus.APPROVED, PayoutStatus.PENDING],
                weights=[0.6, 0.2, 0.2]
            )[0]

            paid_at = period_end + timedelta(days=random.randint(5, 15)) if payout_status == PayoutStatus.PAID else None

            # Choose payment method using string values
            payment_methods = ["ach", "check", "paypal"]

            payout = InfluencerPayout(
                influencer_id=influencer.id,
                period_start=period_start,
                period_end=period_end,
                total_sales=round(total_sales, 2),
                commission_amount=round(commission_amount, 2),
                flat_fee=round(flat_fee, 2),
                total_payout=round(total_payout, 2),
                status=payout_status,
                paid_at=paid_at,
                payment_method=random.choice(payment_methods) if payout_status == PayoutStatus.PAID else None,
                notes=f"Payment for {period_start} to {period_end}"
            )
            payouts.append(payout)

    db.add_all(payouts)
    db.commit()

    return payouts


def clear_marketing_data(db: Session):
    """Clear all marketing data from database."""
    print("  Clearing existing marketing data...")

    # Delete in reverse order of dependencies
    db.query(InfluencerContent).delete()
    db.query(InfluencerPayout).delete()
    db.query(CampaignInfluencer).delete()
    db.query(PromoCodeUsage).delete()
    db.query(PromoCode).delete()
    db.query(AdInsight).delete()
    db.query(Ad).delete()
    db.query(AdSet).delete()
    db.query(Campaign).delete()
    db.query(Creative).delete()
    db.query(Influencer).delete()
    db.query(AdAccount).delete()

    db.commit()
    print("  ✓ Marketing data cleared")


def seed_marketing_database():
    """Seed the marketing database with Good Bogey data."""
    db = SessionLocal()

    try:
        print("🏌️ Seeding Good Bogey Marketing Database...")

        # Clear existing data
        clear_marketing_data(db)

        # Create ad account
        print("  Creating ad account...")
        ad_account = create_ad_account(db)

        # Create influencers
        print("  Creating influencers...")
        influencers = create_influencers(db, count=25)

        # Create campaigns
        print("  Creating campaigns...")
        campaigns = create_campaigns(db, ad_account, count=8)

        # Create creatives
        print("  Creating creatives...")
        creatives = create_creatives(db, count=30)

        # Create ad sets and ads
        print("  Creating ad sets and ads...")
        ad_sets, ads = create_ad_sets_and_ads(db, campaigns, creatives)

        # Create ad insights
        print("  Creating ad insights...")
        insights = create_ad_insights(db, ads[:20])  # Only for first 20 ads to save time

        # Create promo codes
        print("  Creating promo codes...")
        promo_codes = create_promo_codes(db, influencers)

        # Create promo code usage
        print("  Creating promo code usage...")
        usage = create_promo_code_usage(db, promo_codes)

        # Create campaign-influencer associations
        print("  Creating campaign-influencer associations...")
        associations = create_campaign_influencers(db, campaigns, influencers)

        # Create influencer content
        print("  Creating influencer content...")
        content = create_influencer_content(db, influencers, campaigns, ads)

        # Create influencer payouts
        print("  Creating influencer payouts...")
        payouts = create_influencer_payouts(db, influencers)

        print("\n✅ Marketing database seeded successfully!")
        print(f"   - 1 ad account")
        print(f"   - {len(influencers)} influencers")
        print(f"   - {len(campaigns)} campaigns")
        print(f"   - {len(ad_sets)} ad sets")
        print(f"   - {len(ads)} ads")
        print(f"   - {len(creatives)} creatives")
        print(f"   - {len(insights)} ad insights")
        print(f"   - {len(promo_codes)} promo codes")
        print(f"   - {len(usage)} promo code uses")
        print(f"   - {len(associations)} campaign-influencer associations")
        print(f"   - {len(content)} influencer content posts")
        print(f"   - {len(payouts)} influencer payouts")

    except Exception as e:
        print(f"❌ Error seeding marketing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_marketing_database()
