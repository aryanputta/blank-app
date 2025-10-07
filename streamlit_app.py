import math
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KIND Token | Carbon-Negative Blockchain",
    page_icon="🌱",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    :root {
        --solana-purple: #9945ff;
        --solana-cyan: #14f195;
        --solana-deep: #0b1624;
        --solana-ink: #0a0b1e;
    }

    * {
        font-family: 'Inter', sans-serif !important;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, rgba(153, 69, 255, 0.18), transparent 35%),
                    radial-gradient(circle at 20% 80%, rgba(20, 241, 149, 0.15), transparent 45%),
                    linear-gradient(135deg, #050716 0%, #090c1f 40%, #030512 100%);
        color: #d9e2ff;
    }

    [data-testid="stHeader"] {background: transparent;}

    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: 700 !important;
    }

    .hero {
        padding: 4rem 0 3rem 0;
    }

    .hero h1 {
        font-size: clamp(2.8rem, 4vw, 4rem);
        margin-bottom: 1rem;
        line-height: 1.1;
        letter-spacing: -0.03em;
    }

    .hero p {
        font-size: 1.1rem;
        max-width: 650px;
        color: rgba(255, 255, 255, 0.85);
    }

    .cta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2rem;
    }

    .cta-btn {
        padding: 0.75rem 1.6rem;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 600;
    }

    .cta-primary {
        background: linear-gradient(120deg, var(--solana-purple), var(--solana-cyan));
        color: #051016 !important;
        box-shadow: 0 8px 25px rgba(20, 241, 149, 0.35);
    }

    .cta-secondary {
        border: 1px solid rgba(153, 69, 255, 0.45);
        color: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(6px);
    }

    .metric-card {
        background: rgba(12, 15, 40, 0.65);
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid rgba(153, 69, 255, 0.25);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
        height: 100%;
    }

    .metric-card h3 {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .metric-card p {
        font-size: 1.75rem;
        margin: 0.35rem 0 0;
        font-weight: 700;
        color: white;
    }

    .metric-card span {
        font-size: 0.95rem;
        color: rgba(20, 241, 149, 0.85);
    }

    .section-title {
        font-size: 1.9rem;
        margin-top: 3rem;
    }

    .section-description {
        color: rgba(233, 243, 255, 0.7);
        max-width: 720px;
    }

    .solana-grid {
        display: grid;
        gap: 1.5rem;
        margin-top: 1.5rem;
    }

    .solana-grid.two {
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }

    .solana-grid.three {
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }

    .gradient-card {
        background: linear-gradient(145deg, rgba(153, 69, 255, 0.2), rgba(20, 241, 149, 0.08));
        padding: 1.6rem;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(6px);
        color: rgba(255, 255, 255, 0.92);
        min-height: 180px;
    }

    .gradient-card h4 {
        margin-bottom: 0.6rem;
    }

    .solana-table thead th {
        background: rgba(255, 255, 255, 0.04);
    }

    .stTabs [data-baseweb="tab-list"] button {
        background: rgba(12, 15, 40, 0.6);
        border-radius: 999px !important;
        margin-right: 0.75rem;
        border: 1px solid transparent;
        color: rgba(255, 255, 255, 0.7);
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(120deg, rgba(153, 69, 255, 0.25), rgba(20, 241, 149, 0.25));
        border-color: rgba(153, 69, 255, 0.35);
        color: white;
    }

    .stTabs [data-baseweb="tab-content"] {
        padding-top: 2rem;
    }

    .roadmap-item {
        border-left: 2px solid rgba(153, 69, 255, 0.35);
        padding-left: 1.2rem;
        margin-bottom: 1.8rem;
        position: relative;
    }

    .roadmap-item::before {
        content: '';
        position: absolute;
        left: -10px;
        top: 4px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(120deg, var(--solana-purple), var(--solana-cyan));
        box-shadow: 0 0 12px rgba(20, 241, 149, 0.5);
    }

    .footer {
        margin-top: 4rem;
        padding: 2.5rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        color: rgba(233, 243, 255, 0.6);
    }

    .footer a {
        color: rgba(20, 241, 149, 0.85) !important;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

hero_left, hero_right = st.columns([2.2, 1])

with hero_left:
    st.markdown(
        """
        <div class="hero">
            <h1>KIND Token</h1>
            <h3 style="color: rgba(255,255,255,0.65); font-weight: 500;">The carbon-negative Layer 1 inspired by Solana's lightning architecture.</h3>
            <p>
                KIND proves that blockchains can regenerate the planet. Harness high-throughput
                Proof-of-History consensus, 100% renewable validators, and an impact-first treasury
                that removes 10× more CO₂ than the network emits.
            </p>
            <div class="cta-row">
                <a class="cta-btn cta-primary" href="https://docs.kind.earth" target="_blank">Explore Docs</a>
                <a class="cta-btn cta-secondary" href="https://impact.kind.earth" target="_blank">View Impact Dashboard</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div class="gradient-card" style="height:100%; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <h4>Total Supply</h4>
                <p style="font-size:2rem; margin:0;">10,000,000,000 KIND</p>
                <span style="color:rgba(20,241,149,0.8);">Genesis allocation</span>
            </div>
            <div style="margin-top:1.5rem;">
                <h4>Fee Structure</h4>
                <p style="margin:0; color:rgba(233,243,255,0.75);">50% of every network fee is burned.<br/>Remaining 50% rewards validators.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

metrics_cols = st.columns(3)
metrics = [
    ("Carbon Removal", "5,000 tons / yr", "Growing with adoption"),
    ("Energy Draw", "3.5 GWh", "100% renewable"),
    ("Validators", "1,000+", "Global, eco-verified"),
]

for col, (label, value, delta) in zip(metrics_cols, metrics):
    col.markdown(
        f"""
        <div class="metric-card">
            <h3>{label}</h3>
            <p>{value}</p>
            <span>{delta}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

solana_tabs = st.tabs(
    [
        "Architecture",
        "Tokenomics",
        "Impact",
        "Roadmap",
        "Governance",
        "Investors",
    ]
)

with solana_tabs[0]:
    st.markdown("<h2 class='section-title'>Designed for speed, built for the climate</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-description">
        KIND mirrors Solana's Proof-of-History core to deliver 65,000+ TPS and < 600 ms finality while
        staking validators replace miners with renewable-powered infrastructure. The result is a
        next-generation chain that accelerates global climate action.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='solana-grid two'>", unsafe_allow_html=True)
    architecture_cards = [
        (
            "Tower BFT + PoH",
            "Deterministic cryptographic timestamps unlock parallel execution without sacrificing decentralization.",
        ),
        (
            "Proof-of-Stake Security",
            "Stake-weighted validators replace mining rigs, slashing energy usage by 99.9% versus Proof-of-Work.",
        ),
        (
            "Sustainable Hardware",
            "12-core CPUs, NVMe storage, and 1 Gbps links powered exclusively by verified renewable sources.",
        ),
        (
            "Developer Ready",
            "Solana-compatible tooling, SDKs, and RPC architecture make building climate-positive dApps effortless.",
        ),
    ]
    for title, body in architecture_cards:
        st.markdown(
            f"""
            <div class="gradient-card">
                <h4>{title}</h4>
                <p>{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:2.5rem;'>Impact-native use cases</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="solana-grid three">
            <div class="gradient-card">
                <h4>Green Payments</h4>
                <p>Instant cross-border transfers and remittances with negligible fees and verified CO₂ removal.</p>
            </div>
            <div class="gradient-card">
                <h4>Climate DeFi</h4>
                <p>Liquidity pools for carbon forwards, renewable energy credits, and sustainability-linked loans.</p>
            </div>
            <div class="gradient-card">
                <h4>Impact NFTs</h4>
                <p>On-chain proof of carbon removal, biodiversity milestones, and regenerative impact achievements.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with solana_tabs[1]:
    st.markdown("<h2 class='section-title'>Tokenomics engineered for regeneration</h2>", unsafe_allow_html=True)

    distribution_data = [
        ("Environmental Impact Fund", 35, "Carbon removal, renewable energy, restoration"),
        ("Community Rewards & Staking", 25, "Validator rewards, staking incentives"),
        ("Ecosystem Development", 15, "Developer grants and partnerships"),
        ("Foundation Operations", 10, "Nonprofit operations (4-year vesting)"),
        ("Early Supporters & Partners", 10, "Strategic environmental organizations"),
        ("Public Launch", 5, "Fair distribution event with no pre-mine"),
    ]
    dist_df = pd.DataFrame(distribution_data, columns=["Allocation", "Percent", "Use"])

    st.dataframe(
        dist_df,
        hide_index=True,
        width="stretch",
    )

    st.bar_chart(dist_df.set_index("Allocation")["Percent"], color="#14f195")

    col1, col2 = st.columns(2)
    total_supply = 10_000_000_000
    minted = col1.number_input(
        "Tokens minted", min_value=0, max_value=total_supply, value=500_000_000, step=1_000_000
    )
    burn_rate = col2.slider("Fee burn percentage", 0, 100, value=50, step=5)

    if minted:
        dist_df["Tokens"] = (dist_df["Percent"] / 100 * minted).round().astype(int)
    else:
        dist_df["Tokens"] = 0

    st.markdown("### Allocation Breakdown")
    st.dataframe(dist_df, hide_index=True, width="stretch")

    burned_tokens = math.floor(minted * burn_rate / 100)
    circulating = minted - burned_tokens
    st.metric(
        "Projected circulating supply",
        f"{circulating:,} KIND",
        delta=f"{burned_tokens:,} KIND burned",
    )

    st.markdown(
        """
        <div class="solana-grid two" style="margin-top:2rem;">
            <div class="gradient-card">
                <h4>Dynamic staking incentives</h4>
                <p>Validators earn 5–8% APR with slashing guarantees while delegators can participate with as little as 10 KIND.</p>
            </div>
            <div class="gradient-card">
                <h4>Impact-aligned burns</h4>
                <p>Half of every network fee is destroyed and milestone burns unlock when carbon removal goals are exceeded.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with solana_tabs[2]:
    st.markdown("<h2 class='section-title'>Live climate impact modeling</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        KIND partners with Gold Standard, SBTi, and independent auditors to validate every carbon claim.
        Use the sliders below to simulate the regenerative impact of on-chain activity.
        """,
        unsafe_allow_html=True,
    )

    transactions = st.number_input(
        "Simulate monthly transactions",
        min_value=0,
        max_value=50_000_000,
        value=5_000_000,
        step=100_000,
    )
    removal_per_tx = 0.00001
    monthly_removal = transactions * removal_per_tx
    annual_removal = monthly_removal * 12

    impact_cols = st.columns(2)
    impact_cols[0].markdown(
        f"""
        <div class="metric-card">
            <h3>Monthly CO₂ Removed</h3>
            <p>{monthly_removal:,.0f} tons</p>
            <span>Beyond validator footprint</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    impact_cols[1].markdown(
        f"""
        <div class="metric-card">
            <h3>Annualized Removal</h3>
            <p>{annual_removal:,.0f} tons</p>
            <span>Scaled with usage</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="solana-grid three" style="margin-top:2rem;">
            <div class="gradient-card">
                <h4>Direct Air Capture</h4>
                <p>Investments into DAC facilities remove hard-to-abate emissions with verifiable credits.</p>
            </div>
            <div class="gradient-card">
                <h4>Blue Carbon</h4>
                <p>Mangrove and kelp restoration amplifies carbon sequestration and protects coastlines.</p>
            </div>
            <div class="gradient-card">
                <h4>Community Renewables</h4>
                <p>Microgrids and solar cooperatives bring clean energy access to underserved communities.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with solana_tabs[3]:
    st.markdown("<h2 class='section-title'>Roadmap to planetary scale</h2>", unsafe_allow_html=True)
    roadmap = [
        ("Q4 2025", "Genesis", "Testnet launch, validator onboarding, foundation established"),
        ("Q1 2026", "Mainnet Launch", "Public distribution, staking live, first impact projects funded"),
        ("Q2 2026", "Ecosystem Growth", "Developer SDK, first dApps, mobile wallet"),
        ("Q3 2026", "Scale Impact", "10 environmental projects, 500+ validators, first impact report"),
        ("Q4 2026", "Global Expansion", "International partnerships, 1M+ tons CO₂ removed"),
        ("2027+", "Planetary Scale", "10M+ users across 100 countries"),
    ]

    for quarter, title, description in roadmap:
        st.markdown(
            f"""
            <div class="roadmap-item">
                <h4>{quarter} — {title}</h4>
                <p style='color: rgba(233,243,255,0.75);'>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="gradient-card" style="margin-top:2rem;">
            <h4>Performance Specs</h4>
            <ul>
                <li>65,000+ TPS throughput with 400–600 ms finality</li>
                <li>400 ms block times with Solana-compatible runtime</li>
                <li>0.00006 kWh per transaction on 100% renewable grids</li>
                <li>Validator requirements: 12-core/24-thread CPU, 128 GB RAM, 1 TB NVMe, 1 Gbps network</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with solana_tabs[4]:
    st.markdown("<h2 class='section-title'>Transparent, community-led governance</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="solana-grid two">
            <div class="gradient-card">
                <h4>Nonprofit Foundation</h4>
                <p>Registered 501(c)(3)-equivalent stewarding treasury allocations with open financials and annual impact reports.</p>
            </div>
            <div class="gradient-card">
                <h4>Community Voting</h4>
                <p>1 KIND equals 1 vote, boosted 1.5× for staked tokens with quadratic voting for equitable outcomes.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with solana_tabs[5]:
    st.markdown("<h2 class='section-title'>Investor-ready growth engine</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <p class="section-description">
        KIND couples premium Solana-inspired performance with investor-grade incentives, referral mechanics,
        and mobile-first dashboards so capital can accelerate both yield and planetary regeneration.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="solana-grid three">
            <div class="gradient-card">
                <h4>High-yield incentives</h4>
                <ul>
                    <li>Up to 20% APY staking rewards with dynamic lockups.</li>
                    <li>Gasless ERC-2612 permits for effortless compounding.</li>
                    <li>Governance voting power grows with staked balances.</li>
                </ul>
            </div>
            <div class="gradient-card">
                <h4>Social impact integration</h4>
                <ul>
                    <li>Transparent fee routing into humanitarian treasuries.</li>
                    <li>Impact NFTs and dashboards track every contribution.</li>
                    <li>Community votes direct capital to frontline causes.</li>
                </ul>
            </div>
            <div class="gradient-card">
                <h4>Advanced DeFi toolkit</h4>
                <ul>
                    <li>Yield farming and liquidity mining with deflationary burns.</li>
                    <li>Cross-chain ready smart contracts and analytics APIs.</li>
                    <li>Responsive mobile dashboard for on-the-go investors.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h3 style='margin-top:2.5rem;'>Launch in five guided steps</h3>", unsafe_allow_html=True)
    st.code(
        """bash
cd kind
python -m venv venv
source venv/bin/activate  # On Windows use venv\\Scripts\\activate
pip install -r requirements.txt
cp env.template .env
python scripts/fetch_oz.py
python scripts/deploy_enhanced.py
python scripts/add_liquidity_v2.py --pair ETH --amount-kind 10000 --amount-eth 0.2
python scripts/indexer.py
uvicorn dashboards.investor_dashboard:app --reload
        """
    )

    st.markdown(
        """
        <div class="solana-grid two" style="margin-top:2rem;">
            <div class="gradient-card">
                <h4>Feature spotlight</h4>
                <ul>
                    <li>Transfer fees ≤3% with 0.5% auto-burn to boost scarcity.</li>
                    <li>Referral rewards distribute 1% of onboarding volume.</li>
                    <li>Emergency pause and fee caps protect investor capital.</li>
                </ul>
            </div>
            <div class="gradient-card">
                <h4>Operations toolkit</h4>
                <ul>
                    <li>Deploy ERC-20 + ERC-2612 token and humanitarian treasury.</li>
                    <li>Run FastAPI analytics with real-time price and volume feeds.</li>
                    <li>Scripts manage staking, governance, marketing, and LP flows.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h3 style='margin-top:2.5rem;'>Command cheat sheet</h3>", unsafe_allow_html=True)
    operations_cols = st.columns(2)

    operations_cols[0].markdown(
        """
        <div class="gradient-card">
            <h4>Trading & liquidity</h4>
            <ul>
                <li><code>python scripts/dex_buy_sell.py buy-eth --eth 0.02</code></li>
                <li><code>python scripts/dex_buy_sell.py sell-eth --kind 50</code></li>
                <li><code>python scripts/add_liquidity_v2.py --pair ETH --amount-kind 10000 --amount-eth 0.2</code></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    operations_cols[1].markdown(
        """
        <div class="gradient-card">
            <h4>Staking & governance</h4>
            <ul>
                <li><code>python scripts/staking_manager.py stake 1000 --days 90</code></li>
                <li><code>python scripts/staking_manager.py claim-rewards</code></li>
                <li><code>python scripts/governance_manager.py create \"Increase staking rewards to 25%\"</code></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="solana-grid two" style="margin-top:2rem;">
            <div class="gradient-card">
                <h4>Partnership Network</h4>
                <p>Alliances with Conservation International, Rainforest Alliance, Ocean Conservancy, and climate tech accelerators.</p>
            </div>
            <div class="gradient-card">
                <h4>Audit-Ready Transparency</h4>
                <p>Quarterly environmental accounting, real-time treasury dashboards, and NFT-backed impact certificates.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='footer'>", unsafe_allow_html=True)
footer_cols = st.columns(3)
footer_cols[0].markdown("**Website:** [kind.earth](https://kind.earth)")
footer_cols[0].markdown("**Docs:** [docs.kind.earth](https://docs.kind.earth)")
footer_cols[1].markdown("**Email:** foundation@kind.earth")
footer_cols[1].markdown("**GitHub:** [github.com/kind-token](https://github.com/kind-token)")
footer_cols[2].markdown("**Twitter:** [@KINDToken](https://twitter.com/KINDToken)")
footer_cols[2].markdown("**Discord:** [discord.gg/kindtoken](https://discord.gg/kindtoken)")

st.markdown(
    f"<p style='margin-top:1.5rem; color: rgba(233,243,255,0.5);'>© {datetime.now().year} KIND Foundation — Building a blockchain that heals the planet.</p>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
