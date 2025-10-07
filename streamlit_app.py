import math
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KIND Token | Carbon-Negative Blockchain",
    page_icon="🌱",
    layout="wide",
)

st.title("🌍 KIND Token: The Carbon-Negative Blockchain for Global Impact")

st.markdown(
    """
    KIND Token is a nonprofit blockchain foundation inspired by Solana's Proof-of-History
    architecture. Every KIND transaction removes more carbon than it emits, proving that
    cryptocurrency can be a force for planetary healing.
    """
)

with st.container():
    st.subheader("Key Highlights")
    cols = st.columns(5)
    highlights = [
        ("Carbon-Negative", "10× CO₂ removal"),
        ("Performance", "65,000+ TPS"),
        ("Finality", "< 0.001 sec"),
        ("Fees", "$0.0001 avg"),
        ("Energy", "100% renewable"),
    ]
    for col, (title, value) in zip(cols, highlights):
        col.metric(title, value)

st.divider()

impact_cols = st.columns(3)
impact_cols[0].metric("Annual CO₂ Removed", "5,000 tons", delta="Growing with adoption")
impact_cols[1].metric("Network Energy Use", "3.5 GWh", delta="100% offset")
impact_cols[2].metric("Validators Target", "1,000+", delta="Global distribution")

st.divider()

overview_tab, tokenomics_tab, impact_tab, roadmap_tab, governance_tab = st.tabs(
    [
        "Vision & Architecture",
        "Tokenomics",
        "Impact Dashboard",
        "Roadmap",
        "Governance & Partnerships",
    ]
)

with overview_tab:
    st.header("Vision & Mission")
    st.write(
        """
        * **Vision:** Create the world's most environmentally responsible blockchain.
        * **Mission:** Deploy high-performance financial infrastructure that actively reverses climate change.
        """
    )

    st.header("Why KIND?")
    st.write(
        """
        Traditional blockchains consume massive energy (Bitcoin: ~150 TWh/year). KIND leverages
        Proof-of-History with Proof-of-Stake validation, eliminating mining hardware while
        timestamping transactions for parallel processing and sub-second finality.
        """
    )

    st.subheader("Technical Architecture")
    st.write(
        """
        * **Consensus:** Tower BFT (PoH + PoS)
        * **Throughput:** 65,000+ TPS with 400 ms block times
        * **Validation:** Stake-weighted selection, 99.9% lower energy than Proof-of-Work
        * **Infrastructure:** Renewable-powered validators with 12-core CPU, 128 GB RAM, NVMe storage, 1 Gbps network
        """
    )

    st.subheader("Use Cases")
    st.write(
        """
        * Payments & transfers with instant settlement
        * Green finance rails for carbon credits and renewable investments
        * Impact NFTs and verifiable carbon removal certificates
        * DeFi protocols for sustainable yield and lending
        """
    )

with tokenomics_tab:
    st.header("Token Distribution")

    distribution_data = [
        ("Environmental Impact Fund", 35, "Carbon removal, renewable energy, restoration"),
        ("Community Rewards & Staking", 25, "Validator rewards, staking incentives"),
        ("Ecosystem Development", 15, "Developer grants and partnerships"),
        ("Foundation Operations", 10, "Nonprofit operations (4-year vesting)"),
        ("Early Supporters & Partners", 10, "Strategic environmental organizations"),
        ("Public Launch", 5, "Fair distribution event with no pre-mine"),
    ]
    dist_df = pd.DataFrame(distribution_data, columns=["Allocation", "Percent", "Use"])
    st.dataframe(dist_df, hide_index=True, use_container_width=True)

    chart_data = dist_df[["Allocation", "Percent"]].set_index("Allocation")
    st.bar_chart(chart_data)

    st.subheader("Deflationary Mechanics")
    st.write(
        """
        * 50% of transaction fees are permanently burned, creating deflationary pressure.
        * Additional community-governed burns unlock when impact milestones are reached.
        """
    )

    st.subheader("Staking & Rewards")
    st.write(
        """
        * **Validator staking:** Minimum 10,000 KIND, with dynamic 5-8% annual yield.
        * **Delegated staking:** Join with as little as 10 KIND and share validator rewards.
        * **Slashing:** Misbehavior results in stake reductions to maintain network integrity.
        """
    )

    st.markdown("---")

    st.subheader("Minting & Allocation Simulator")
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

    st.write("### Allocation Breakdown")
    st.dataframe(dist_df, hide_index=True, use_container_width=True)

    burned_tokens = math.floor(minted * burn_rate / 100)
    circulating = minted - burned_tokens
    st.metric("Projected circulating supply", f"{circulating:,} KIND", delta=f"{burned_tokens:,} burned")

with impact_tab:
    st.header("Real-Time Impact Snapshot")
    st.write(
        """
        KIND pairs radical efficiency with verifiable climate action. The network partners with
        Gold Standard, SBTi, and independent auditors to confirm every claim.
        """
    )

    st.subheader("Carbon Removal Tracker")
    transactions = st.number_input("Simulate monthly transactions", 0, 50_000_000, 5_000_000, step=100_000)
    removal_per_tx = 0.00001  # tons removed per transaction beyond energy usage
    monthly_removal = transactions * removal_per_tx
    annual_removal = monthly_removal * 12
    st.metric("Estimated CO₂ removed per month", f"{monthly_removal:,.0f} tons")
    st.metric("Estimated CO₂ removed per year", f"{annual_removal:,.0f} tons")

    st.subheader("Impact Focus Areas")
    focus_cols = st.columns(3)
    focus_cols[0].write("• Direct air capture investments\n• Mangrove & kelp restoration")
    focus_cols[1].write("• Solar farms in emerging nations\n• Ocean plastic removal")
    focus_cols[2].write("• Wildlife corridor preservation\n• Community-led renewable microgrids")

with roadmap_tab:
    st.header("Roadmap")
    roadmap = [
        ("Q4 2025", "Genesis", "Testnet launch, validator onboarding, foundation established"),
        ("Q1 2026", "Mainnet Launch", "Public distribution, staking live, first impact projects funded"),
        ("Q2 2026", "Ecosystem Growth", "Developer SDK, first dApps, mobile wallet"),
        ("Q3 2026", "Scale Impact", "10 environmental projects, 500+ validators, first impact report"),
        ("Q4 2026", "Global Expansion", "International partnerships, 1M+ tons CO₂ removed"),
        ("2027+", "Planetary Scale", "10M+ users across 100 countries"),
    ]
    for quarter, title, description in roadmap:
        st.markdown(f"**{quarter} — {title}**\n:green[ {description} ]")

    st.subheader("Technical Specifications")
    st.write(
        """
        * **Throughput:** 65,000+ TPS with 400-600 ms finality
        * **Block Time:** 400 ms
        * **Energy Use:** 0.00006 kWh per transaction on renewable grids
        * **Validator Hardware:** 12-core CPU, 128 GB RAM, 1 TB NVMe SSD, 1 Gbps connection
        """
    )

with governance_tab:
    st.header("Nonprofit Foundation Governance")
    st.write(
        """
        * Registered as a 501(c)(3)-equivalent entity with transparent finances.
        * Board of environmental scientists, blockchain engineers, and policy experts.
        * Annual impact reports and quarterly environmental audits published publicly.
        """
    )

    st.subheader("Community Governance")
    st.write(
        """
        * 1 KIND = 1 vote on proposals, with 1.5× power for staked tokens.
        * Quadratic voting ensures equitable representation.
        * Community controls environmental project funding, protocol upgrades, and burn events.
        """
    )

    st.subheader("Partnership Network")
    st.write(
        """
        * Environmental partners: Conservation International, Rainforest Alliance, Ocean Conservancy.
        * Technical allies: Renewable energy providers, carbon verification bodies, climate tech accelerators.
        * Financial transparency: Real-time treasury, quarterly independent audits, public impact API.
        """
    )

st.divider()

st.header("Connect with KIND")
col_a, col_b, col_c = st.columns(3)
col_a.markdown("**Website:** [kind.earth](https://kind.earth)")
col_a.markdown("**Docs:** [docs.kind.earth](https://docs.kind.earth)")
col_b.markdown("**Email:** foundation@kind.earth")
col_b.markdown("**GitHub:** [github.com/kind-token](https://github.com/kind-token)")
col_c.markdown("**Twitter:** [@KINDToken](https://twitter.com/KINDToken)")
col_c.markdown("**Discord:** [discord.gg/kindtoken](https://discord.gg/kindtoken)")

st.caption("© {year} KIND Foundation — Building a blockchain that heals the planet.".format(year=datetime.now().year))
