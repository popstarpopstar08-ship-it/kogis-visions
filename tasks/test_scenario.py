from crewai import Task

def build_test_scenario(ceo, intelligence, product, marketing, sales, finance, operations, tech, rd):
    """
    TEST SCENARIO: First Monthly Cycle — Find & Validate Top 3 Products to Launch

    This simulates the company's first real business cycle.
    Every director plays their role. The CEO makes the final call.
    """

    # ── TASK 1: Intelligence scans the market ─────────────────────────────────
    scan = Task(
        description="""
        You are running the first market scan for Kogis Visions.

        Simulate scanning these marketplaces for the past 30 days:
        - Amazon Best Sellers & Movers/Shakers
        - eBay Trending
        - AliExpress Hot Products
        - TikTok Shop Trending
        - Google Shopping Insights

        Based on your deep knowledge of current e-commerce trends, identify the TOP 5
        product candidates that meet ALL of the following criteria:
        - Strong and rising demand (not declining)
        - No major brand domination (Nike, Apple, etc.)
        - Potential gross margin of at least 35%
        - Available from multiple suppliers
        - No serious legal/trademark risks
        - Not highly seasonal

        For each of the 5 products provide:
        1. Product name and category
        2. Estimated monthly sales volume
        3. Price range (low / average / high)
        4. Number of competing sellers (estimate)
        5. Trend direction (rising / stable)
        6. Seasonality risk (low / medium / high)
        7. Your score out of 100
        8. Why this product passed your risk filters

        Apply ALL risk filters before finalizing your list.
        Rank them from strongest to weakest opportunity.
        """,
        expected_output="""
        A ranked list of exactly 5 product candidates.
        Each entry is detailed with: name, category, estimated monthly sales,
        price range, competitor count, trend direction, seasonality risk, score (1-100),
        and a brief risk filter confirmation.
        """,
        agent=intelligence,
    )

    # ── TASK 2: Product validates and selects top 3 ───────────────────────────
    validate = Task(
        description="""
        You have received the Intelligence Director's ranked list of 5 product candidates.

        Your job is to validate each one and SELECT THE TOP 3 to move forward.

        For each of the 5 products:
        1. Find 2 realistic suppliers (from AliExpress, CJdropshipping, Spocket, Zendrop)
           - Name the supplier platform, estimated product cost, shipping cost, shipping time
        2. Calculate the full margin:
           - Supplier cost + shipping
           - Payment processing (2.9% + $0.30)
           - Refund reserve (3%)
           - = True COGS
           - Set retail price (must achieve minimum 35% gross margin)
           - Calculate gross margin %
        3. Write a product brief:
           - Product name (retail-ready)
           - One-sentence unique value proposition
           - Target customer persona
           - Top 3 benefits
           - Top 2 customer objections + your answers
           - Pricing recommendation

        Apply your risk filters:
        - Reject if margin is below 35%
        - Reject if only 1 supplier found
        - Reject if shipping time exceeds 20 days

        Select the TOP 3 products that pass all filters.
        Explain why you rejected any products.
        """,
        expected_output="""
        Top 3 validated products, each with:
        - Supplier details (2 suppliers per product)
        - Full margin calculation
        - Retail price recommendation
        - Complete product brief
        Any rejected products listed with clear rejection reasons.
        """,
        agent=product,
        context=[scan],
    )

    # ── TASK 3: Tech plans the build ──────────────────────────────────────────
    tech_plan = Task(
        description="""
        You have received the 3 validated product briefs from the Product Director.

        For each of the 3 products, create a detailed technical build plan:

        1. Site structure:
           - Store name / domain suggestion
           - Landing page sections needed (based on Sales Director funnel architecture)
           - Mobile-first layout notes

        2. Pixel & analytics setup:
           - List every tracking pixel needed (Meta, Google, TikTok)
           - Server-side tracking (CAPI) requirements
           - GA4 event configuration

        3. Integration checklist:
           - Supplier integration (which platform: DSers / AutoDS / manual)
           - Email platform (Klaviyo) connection points
           - Customer support widget configuration
           - Payment gateway setup

        4. Performance targets:
           - Target PageSpeed score (mobile)
           - Image optimization approach
           - Any performance risks for this product type

        5. Timeline: confirm all 3 sites can be live within 24 hours of green light.

        Flag any technical risks or blockers for any of the 3 products.
        """,
        expected_output="""
        Technical build plan for each of the 3 products:
        - Site structure and domain suggestion
        - Full pixel and analytics setup plan
        - Integration checklist
        - Performance targets and risks
        - 24-hour launch confirmation or flagged blockers
        """,
        agent=tech,
        context=[validate],
    )

    # ── TASK 4: Marketing designs organic-first campaigns ─────────────────────
    campaigns = Task(
        description="""
        You have the 3 validated products and their briefs.
        We are starting with ZERO ad budget — organic content only.
        Design a complete organic-first marketing launch plan for each product.

        For EACH of the 3 products, create:

        1. Target Audience Profile:
           - Who exactly is this person? (age, lifestyle, pain points, platforms they use)
           - Where do they hang out online? (which TikTok niches, subreddits, Facebook groups)

        2. TikTok Organic Strategy:
           - Write 3 video scripts (hook + structure) using different angles:
             Angle A: Problem/pain hook ("Stop scrolling if you have [problem]...")
             Angle B: Curiosity/reveal hook ("I can't believe this actually works...")
             Angle C: Social proof hook ("After 30 days using this...")
           - Recommended trending sounds category
           - Hashtag set (5 hashtags)
           - Best posting times for this audience

        3. Instagram Reels + Pinterest:
           - How to repurpose TikTok content for Reels
           - Pinterest board name + 3 pin title ideas for this product
           - Carousel post idea (what "5 things" or comparison would work?)

        4. Facebook Groups:
           - Name 3 types of Facebook groups this product belongs in
           - Write a soft-sell post (value-first, not spammy) for each product

        5. Email List Building:
           - Lead magnet idea (what free value can we offer for email signups?)
           - Pop-up offer text for the website
           - Subject lines for: welcome email, abandoned cart (3 emails), post-purchase (2 emails)

        6. 7-Day Content Calendar:
           - Day by day plan: what to post, on which platform, with what angle

        7. Organic → Paid Trigger:
           - At what signal (views, conversions, list size) should we switch on paid ads?

        Remember: zero budget. Every result must come from content quality and consistency.
        """,
        expected_output="""
        Full organic marketing plan for each of the 3 products:
        - Audience profile
        - 3 TikTok video scripts with hooks
        - Instagram and Pinterest strategy
        - Facebook group soft-sell posts
        - Email list building plan with lead magnet idea
        - 7-day content calendar
        - Organic-to-paid transition trigger
        """,
        agent=marketing,
        context=[validate],
    )

    # ── TASK 5: Sales designs the funnels ────────────────────────────────────
    funnels = Task(
        description="""
        For each of the 3 products, design the complete sales funnel.

        1. Landing Page Copy Outline:
           - Hero headline (benefit-driven)
           - Subheadline
           - Top 3 bullet points (benefits, not features)
           - Social proof approach (what type of proof works best for this product?)
           - Guarantee wording
           - CTA button text

        2. Offer Structure:
           - Base product price (confirmed from Product Director)
           - Order bump: what complementary product / add-on? At what price?
           - Upsell 1: what offer immediately post-purchase? At what price?
           - Upsell 2 or Downsell: what's the fallback offer?

        3. Conversion Targets:
           - Expected conversion rate range for this product type
           - Expected AOV with upsells
           - First A/B test to run (what element and what hypothesis?)

        4. Psychological Triggers:
           - Which Cialdini principles apply most to this product?
           - Any scarcity or urgency elements that are REAL and usable?
        """,
        expected_output="""
        Complete funnel design for each of the 3 products:
        - Landing page copy outline
        - Full offer stack (base + bump + upsell 1 + upsell 2/downsell)
        - Conversion rate expectations and AOV projections
        - First A/B test plan
        - Key psychological triggers applied
        """,
        agent=sales,
        context=[validate, campaigns],
    )

    # ── TASK 6: Finance runs the numbers ─────────────────────────────────────
    financials = Task(
        description="""
        Run the financial model for all 3 products before launch approval.
        NOTE: We are starting with ZERO ad budget — organic traffic only.

        For EACH product, using data from Product and Marketing directors:

        1. Unit Economics (zero ad spend model):
           - COGS (from Product Director)
           - Retail price
           - Gross margin %
           - Net margin per order (no ad spend deducted — organic traffic is free)
           - Profit per order

        2. Monthly Projection (organic only — conservative):
           - Assume: 20 orders in month 1 (organic is slow to start)
           - Calculate: revenue, COGS, gross profit, net profit
           - How much profit can be reinvested into ads after month 1?

        3. Monthly Projection (organic only — optimistic):
           - Assume: 100 orders in month 1 (if a video goes viral)
           - Calculate: same metrics
           - At what revenue point should we start paid ads?

        4. Startup Cost Breakdown:
           - Shopify ($1/month trial): $1
           - Domain: $10
           - Anthropic API: $20
           - Total startup capital needed: calculate
           - Break-even point: how many orders to recover startup cost?

        5. Reinvestment Plan:
           - First $100 profit: where does it go?
           - First $500 profit: when do we start paid ads and with how much?
           - First $1,000 profit: scaling plan

        6. Risk Flags:
           - Which product has the tightest margins?
           - Any financial red flags before launch?
           - What is the worst case scenario (zero orders month 1)?
        """,
        expected_output="""
        Financial model for all 3 products (zero ad budget):
        - Unit economics table per product (organic model)
        - Conservative and optimistic monthly projections
        - Total startup cost and break-even calculation
        - Reinvestment plan ($100 / $500 / $1,000 milestones)
        - Risk ranking of the 3 products
        """,
        agent=finance,
        context=[validate, campaigns],
    )

    # ── TASK 7: Operations plans fulfillment ─────────────────────────────────
    fulfillment = Task(
        description="""
        For each of the 3 products, create the fulfillment and operations plan.

        1. Fulfillment Setup:
           - Primary supplier (from Product Director brief): confirm routing plan
           - Backup supplier: confirm and document
           - Expected order-to-ship time
           - Expected delivery time to customer (US / EU / AU)

        2. Customer Support Preparation:
           - Top 5 customer questions for this product (write the Q&A)
           - Refund/return policy recommendation for this product
           - Any known fulfillment risks (fragile? oversized? customs?)

        3. Automation Checklist:
           - Order routing: automated? (yes/no + method)
           - Tracking notification: automated? (yes/no + method)
           - Review request: automated? (yes/no + timing)

        4. Risk Assessment:
           - What is the biggest fulfillment risk for each product?
           - What is the contingency plan if primary supplier fails?

        5. Supplier Performance Targets:
           - Set KPIs for each supplier before launch
        """,
        expected_output="""
        Fulfillment plan for each of the 3 products:
        - Supplier routing confirmed (primary + backup)
        - Delivery time estimates by region
        - Customer support Q&A (5 per product)
        - Automation checklist status
        - Risk assessment and contingency plan
        - Supplier KPIs
        """,
        agent=operations,
        context=[validate],
    )

    # ── TASK 8: R&D adds future intelligence ─────────────────────────────────
    rd_input = Task(
        description="""
        Review the 3 products selected for launch and provide R&D intelligence.

        1. Market Timing Assessment:
           - For each product: are we early, on-time, or late to this trend?
           - What is the estimated runway (months of strong demand remaining)?

        2. Competitive Threat Assessment:
           - For each product: who are the top 3 competitors right now?
           - What are they doing well that we must match?
           - What gap can we exploit that they're missing?

        3. Next Cycle Preview:
           - Based on current trends, suggest 2 adjacent niches to explore next month
           - Brief rationale for each (why now, why this niche)

        4. Internal Improvement Suggestion:
           - Identify 1 process improvement for this launch cycle
           - What could be faster, cheaper, or more automated?
        """,
        expected_output="""
        R&D intelligence report:
        - Market timing assessment per product (early/on-time/late + runway estimate)
        - Competitive threat summary per product (top 3 competitors + gap analysis)
        - 2 niche recommendations for next cycle with rationale
        - 1 internal process improvement suggestion
        """,
        agent=rd,
        context=[scan, validate],
    )

    # ── TASK 9: CEO makes the final call ─────────────────────────────────────
    ceo_decision = Task(
        description="""
        You have received full reports from all 7 directors on the 3 product candidates.

        Review everything and produce the COMPANY LAUNCH DECISION MEMO.

        1. Launch Decision:
           - For each of the 3 products: APPROVED / CONDITIONAL / REJECTED
           - If conditional: what must be resolved before launch?
           - If rejected: clear reason why

        2. Priority Ranking:
           - Which product launches first? Why?
           - What is the launch sequence and timeline?

        3. Budget Authorization:
           - Total ad spend approved for month 1
           - Per-product budget allocation
           - Any spending limits or conditions

        4. Risk Summary:
           - Top 3 risks across all 3 products
           - Mitigation plan for each

        5. Success Metrics:
           - What does a successful month 1 look like? (specific numbers)
           - At what point do you personally review performance?

        6. Instructions to Directors:
           - Specific instruction to each director for the launch week

        This memo is the final word. All directors execute based on this decision.
        """,
        expected_output="""
        CEO Launch Decision Memo:
        - Launch decision per product (Approved / Conditional / Rejected) with reasoning
        - Launch priority and sequence
        - Budget authorization with per-product allocation
        - Top 3 risk mitigation plans
        - Month 1 success metrics
        - Specific instructions to each of the 7 directors
        """,
        agent=ceo,
        context=[scan, validate, tech_plan, campaigns, funnels, financials, fulfillment, rd_input],
    )

    return [scan, validate, tech_plan, campaigns, funnels, financials, fulfillment, rd_input, ceo_decision]
