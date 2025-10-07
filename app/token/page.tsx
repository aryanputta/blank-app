'use client';

import { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, AreaChart, Area, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import { tokenDistribution, sampleTransactions, priceHistory } from '@/lib/data';

const COLORS = ['#16a34a', '#0f766e', '#22c55e', '#4ade80', '#0ea5e9', '#f97316'];

export default function TokenPage() {
  const [copied, setCopied] = useState(false);
  const contractAddress = '0xK1ND0000F0UNDAT10N00000000000000000123';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(contractAddress);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      setCopied(false);
    }
  };

  return (
    <div className="section-shell space-y-16">
      <header className="space-y-6 text-center max-w-3xl mx-auto">
        <span className="badge">Token Transparency</span>
        <h1 className="text-4xl font-semibold text-dusk">The currency of compassion, engineered for trust.</h1>
        <p className="text-lg text-dusk/70">
          KIND Token aligns long-term sustainability with investor incentives through transparent tokenomics, deflationary
          mechanics, and carbon-negative operations.
        </p>
      </header>

      <section className="grid lg:grid-cols-2 gap-12 items-start">
        <div className="card">
          <h2 className="text-xl font-semibold text-dusk mb-4">Tokenomics Overview</h2>
          <div className="h-72">
            <ResponsiveContainer>
              <PieChart>
                <Pie
                  data={tokenDistribution}
                  innerRadius={70}
                  outerRadius={120}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {tokenDistribution.map((entry, index) => (
                    <Cell key={`cell-${entry.name}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => `${value}%`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <ul className="grid md:grid-cols-2 gap-4 mt-6 text-sm text-dusk/70">
            {tokenDistribution.map((slice) => (
              <li key={slice.name} className="rounded-2xl bg-brand-50/60 p-4">
                <p className="font-semibold text-dusk">{slice.name}</p>
                <p>{slice.value}% allocation</p>
              </li>
            ))}
          </ul>
        </div>
        <div className="space-y-6">
          <div className="card space-y-4">
            <h3 className="text-lg font-semibold text-dusk">Smart Contract Credentials</h3>
            <dl className="grid grid-cols-1 gap-4 text-sm text-dusk/70">
              <div>
                <dt className="font-semibold text-dusk">Token Address</dt>
                <dd className="flex items-center justify-between gap-3 bg-brand-50/80 border border-brand-100/70 rounded-2xl px-4 py-2">
                  <span className="truncate">{contractAddress}</span>
                  <button onClick={handleCopy} className="btn-secondary text-xs">
                    {copied ? 'Copied!' : 'Copy Contract'}
                  </button>
                </dd>
              </div>
              <div>
                <dt className="font-semibold text-dusk">Network</dt>
                <dd>Solana &amp; Ethereum L2 bridge</dd>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <dt className="font-semibold text-dusk">Total Supply</dt>
                  <dd>10,000,000,000 KIND</dd>
                </div>
                <div>
                  <dt className="font-semibold text-dusk">Decimals</dt>
                  <dd>9</dd>
                </div>
              </div>
              <div>
                <dt className="font-semibold text-dusk">Audits &amp; Verification</dt>
                <dd>Halborn | CertiK | Science-Based Targets Initiative</dd>
              </div>
            </dl>
          </div>
          <div className="card space-y-3">
            <h3 className="text-lg font-semibold text-dusk">How to Buy KIND</h3>
            <ol className="space-y-3 text-sm text-dusk/70">
              <li>
                <span className="font-semibold text-dusk">1. Connect Wallet:</span> Use MetaMask or WalletConnect to link your
                wallet securely.
              </li>
              <li>
                <span className="font-semibold text-dusk">2. Swap for KIND:</span> Acquire USDC, then trade for KIND on our preferred
                DEX partners.
              </li>
              <li>
                <span className="font-semibold text-dusk">3. Track Progress:</span> Monitor your holdings and real-time impact in the
                investor dashboard.
              </li>
            </ol>
          </div>
        </div>
      </section>

      <section className="grid xl:grid-cols-[1.2fr,0.8fr] gap-12 items-start">
        <div className="card space-y-6">
          <h3 className="text-lg font-semibold text-dusk">Live Token Analytics</h3>
          <div className="h-80">
            <ResponsiveContainer>
              <AreaChart data={priceHistory} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#16a34a" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorVolume" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0f766e" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#0f766e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" stroke="#0f766e" tickLine={false} axisLine={false} />
                <YAxis yAxisId="left" stroke="#16a34a" tickLine={false} axisLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="#0f766e" tickLine={false} axisLine={false} />
                <CartesianGrid strokeDasharray="3 3" stroke="#bbf7d0" />
                <Tooltip formatter={(value: number, name) => [`${value.toFixed(2)} ${name === 'price' ? 'USD' : 'M'}`, name]} />
                <Legend />
                <Area
                  yAxisId="left"
                  type="monotone"
                  dataKey="price"
                  stroke="#16a34a"
                  fillOpacity={1}
                  fill="url(#colorPrice)"
                  name="price"
                />
                <Area
                  yAxisId="right"
                  type="monotone"
                  dataKey="volume"
                  stroke="#0f766e"
                  fillOpacity={1}
                  fill="url(#colorVolume)"
                  name="volume"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="card space-y-4">
          <h3 className="text-lg font-semibold text-dusk">Real-Time Activity</h3>
          <p className="text-sm text-dusk/60">Latest on-chain events highlight the pulse of the KIND ecosystem.</p>
          <div className="space-y-3">
            {sampleTransactions.map((tx) => (
              <div key={tx.hash} className="rounded-2xl border border-brand-100/70 bg-brand-50/60 px-4 py-3 text-sm text-dusk/80">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-dusk">{tx.action}</span>
                  <span className="text-xs text-dusk/50">{tx.hash}</span>
                </div>
                <div className="flex justify-between text-xs text-dusk/60 mt-1">
                  <span>{tx.amount}</span>
                  <span>{tx.impact}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="card bg-brand-50/60">
        <h3 className="text-lg font-semibold text-dusk">Ecosystem Fundamentals</h3>
        <div className="mt-6 grid md:grid-cols-3 gap-6 text-sm text-dusk/70">
          <div>
            <h4 className="font-semibold text-dusk mb-2">Deflationary Mechanics</h4>
            <p>50% of transaction fees burn automatically while impact milestones trigger additional supply reductions.</p>
          </div>
          <div>
            <h4 className="font-semibold text-dusk mb-2">Impact Vault</h4>
            <p>Every fee routes to audited humanitarian vaults funding carbon removal, health access, and climate resilience.</p>
          </div>
          <div>
            <h4 className="font-semibold text-dusk mb-2">Investor Confidence</h4>
            <p>Audited smart contracts, transparent reserves, and nonprofit governance align incentives with long-term growth.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
