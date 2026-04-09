from crewai import Task

def build_monthly_tasks(ceo, intelligence, product, marketing, sales, finance, operations, tech, rd):

    scan_market = Task(
        description=(
            "Scan Amazon Best Sellers, eBay Trending, AliExpress Hot Products, TikTok Shop, "
            "and Google Shopping for the past 30 days. Identify the top 20 product candidates. "
            "For each product provide: estimated monthly sales volume, price range, competitor count, "
            "trend direction, seasonality risk, and a score from 1-100. "
            "Apply all risk filters before passing the list forward."
        ),
        expected_output=(
            "A ranked list of top 20 products with full data profiles and scores. "
            "Each entry includes: product name, category, price range, score, risk flags."
        ),
        agent=intelligence,
    )

    validate_products = Task(
        description=(
            "Take the Intelligence Director's ranked product list. "
            "For each product: find minimum 2 suppliers, verify shipping times, calculate gross margin, "
            "set pricing strategy, write a product brief (title, benefits, target persona, unique angle). "
            "Apply all risk filters. Greenlight maximum 10 products to move forward."
        ),
        expected_output=(
            "A validated list of up to 10 greenlighted products. "
            "Each entry includes: supplier details, margin calculation, retail price, product brief."
        ),
        agent=product,
        context=[scan_market],
    )

    build_sites = Task(
        description=(
            "For each greenlighted product, generate a fully functional Shopify product page and "
            "landing page. Configure analytics pixels (Meta, Google, TikTok). "
            "Set up payment gateway, order confirmation emails, and all integrations. "
            "Ensure each site scores ≥ 85 on Google PageSpeed mobile. "
            "Target: all sites live within 24 hours."
        ),
        expected_output=(
            "A list of live product URLs with: PageSpeed score, pixel confirmation, "
            "integration checklist, and any issues encountered."
        ),
        agent=tech,
        context=[validate_products],
    )

    launch_campaigns = Task(
        description=(
            "For each live product, create marketing campaigns across Meta, Google, and TikTok. "
            "Define audience, write 3 ad angle concepts, set campaign structure with testing budgets ($20-30/day). "
            "Set up email sequences: welcome, abandoned cart, post-purchase. "
            "Brief organic TikTok content (3 posts per product)."
        ),
        expected_output=(
            "Campaign launch report per product: platforms activated, audiences defined, "
            "creatives briefed, email sequences configured, spend caps set."
        ),
        agent=marketing,
        context=[build_sites],
    )

    optimize_funnels = Task(
        description=(
            "Review landing pages for all live products. "
            "Ensure each has: benefit-driven headline, social proof, order bump, post-purchase upsell funnel. "
            "Set up A/B test for each product (1 test per product minimum). "
            "Report conversion rate baseline and AOV target per product."
        ),
        expected_output=(
            "Funnel audit per product: conversion rate baseline, AOV, upsell configuration, "
            "A/B test hypothesis and setup confirmation."
        ),
        agent=sales,
        context=[build_sites, launch_campaigns],
    )

    setup_fulfillment = Task(
        description=(
            "For each live product, confirm fulfillment automation is active: "
            "order routing to primary supplier, backup supplier configured, "
            "tracking automation live, customer support chatbot configured with product FAQs. "
            "Confirm refund and dispute handling procedures are in place."
        ),
        expected_output=(
            "Fulfillment checklist per product: supplier routing confirmed, backup active, "
            "tracking automation status, support bot status, SLA configuration."
        ),
        agent=operations,
        context=[validate_products, build_sites],
    )

    financial_review = Task(
        description=(
            "Set up P&L tracking for all new products. "
            "Define budget caps per product (max 20% of total budget each). "
            "Establish kill criteria thresholds. "
            "Produce the company-wide financial baseline report for this cycle."
        ),
        expected_output=(
            "Financial setup report: budget allocation per product, kill thresholds set, "
            "company cash position, operating reserve status."
        ),
        agent=finance,
        context=[validate_products, launch_campaigns],
    )

    rd_research = Task(
        description=(
            "Research 5 emerging niches for the next cycle. "
            "Monitor top 10 competitors and report any significant moves. "
            "Propose 2 internal improvement experiments (tools, automations, or processes). "
            "Deliver findings to Intelligence Director for next month's scan."
        ),
        expected_output=(
            "R&D report: 5 niche recommendations with rationale, competitor intelligence summary, "
            "2 experiment proposals with hypotheses and budget estimates."
        ),
        agent=rd,
        context=[scan_market],
    )

    ceo_review = Task(
        description=(
            "Review all director reports from this cycle. "
            "Confirm product launches, verify budget allocations, assess risk exposure. "
            "Make final decisions on any flagged items. "
            "Produce the company weekly strategy memo: what we launched, what we're watching, "
            "what the priorities are for the next 7 days."
        ),
        expected_output=(
            "CEO strategy memo: products launched, key metrics baseline, risk flags addressed, "
            "decisions made, top 3 priorities for next 7 days."
        ),
        agent=ceo,
        context=[scan_market, validate_products, build_sites, launch_campaigns,
                 optimize_funnels, setup_fulfillment, financial_review, rd_research],
    )

    return [
        scan_market,
        validate_products,
        build_sites,
        launch_campaigns,
        optimize_funnels,
        setup_fulfillment,
        financial_review,
        rd_research,
        ceo_review,
    ]
