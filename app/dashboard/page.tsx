'use client';

import { useMemo, useState } from 'react';
import { useAccount, useConnect, useDisconnect } from 'wagmi';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, BarChart, Bar, Legend } from 'recharts';
import { priceHistory } from '@/lib/data';

const dashboardMetrics = [
  { label: 'Portfolio Value', value: '$48,920', detail: '+12.4% this month' },
  { label: 'Staking Rewards', value: '1,482 KIND', detail: '≈ 1,482 meals donated' },
  { label: 'Impact Score', value: 'Gold Ally', detail: 'Top 5% of contributors' }
];

const connectorsDescription: Record<string, string> = {
  MetaMask: 'Connect with MetaMask',
  WalletConnect: 'Connect with WalletConnect'
};

export default function DashboardPage() {
  const { address, isConnected } = useAccount();
  const { connectors, connect } = useConnect();
  const { disconnect } = useDisconnect();
  const [kindHoldings] = useState(18234.78);

  const holdingsUSD = useMemo(() => (kindHoldings * 0.78).toFixed(2), [kindHoldings]);

  const metrics = useMemo(
    () => [
      { title: 'KIND Balance', value: `${kindHoldings.toLocaleString()} KIND` },
      { title: 'USD Value', value: `$${Number(holdingsUSD).toLocaleString()}` },
      { title: 'Lifetime Impact', value: `${Math.round(kindHoldings)} meals donated` }
    ],
    [kindHoldings, holdingsUSD]
  );

  return (
    <div className="section-shell space-y-12">
      <header className="space-y-4">
        <span className="badge">Investor Dashboard</span>
        <h1 className="text-4xl font-semibold text-dusk">Your kindness-powered fintech cockpit.</h1>
        <p className="text-lg text-dusk/70 max-w-2xl">
          Track holdings, staking yields, and social dividends with responsive analytics designed to make doing good feel as
          intuitive as managing a modern portfolio.
        </p>
      </header>

      <section className="card space-y-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-2">
            <p className="text-sm font-semibold text-dusk/60">Wallet</p>
            <p className="text-lg font-semibold text-dusk">{isConnected ? address : 'No wallet connected'}</p>
            <p className="text-xs text-dusk/50">1 KIND = 1 meal donated</p>
          </div>
          <div className="flex flex-wrap gap-3">
            {isConnected ? (
              <button className="btn-secondary" onClick={() => disconnect()}>
                Disconnect
              </button>
            ) : (
              connectors.map((connector) => (
                <button
                  key={connector.uid}
                  className="btn-primary"
                  onClick={() => connect({ connector })}
                  disabled={!connector.ready}
                >
                  {connector.name in connectorsDescription ? connectorsDescription[connector.name] : connector.name}
                </button>
              ))
            )}
          </div>
        </div>
        {isConnected ? (
          <div className="grid md:grid-cols-3 gap-4">
            {metrics.map((metric) => (
              <div key={metric.title} className="card bg-brand-50/60">
                <p className="text-xs text-dusk/60 uppercase tracking-[0.3em]">{metric.title}</p>
                <p className="text-2xl font-semibold text-brand-600 mt-3">{metric.value}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-dusk/60">
            Connect your wallet to unlock personalized analytics, staking actions, and verified impact reporting.
          </p>
        )}
      </section>

      <section className="grid xl:grid-cols-[1.2fr,0.8fr] gap-12 items-start">
        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-dusk">Portfolio Performance</h2>
          <div className="h-72">
            <ResponsiveContainer>
              <AreaChart data={priceHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#bbf7d0" />
                <XAxis dataKey="day" stroke="#0f766e" tickLine={false} axisLine={false} />
                <YAxis stroke="#16a34a" tickLine={false} axisLine={false} />
                <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
                <Area type="monotone" dataKey="price" stroke="#16a34a" fill="rgba(34,197,94,0.2)" name="Portfolio" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-dusk">Community Growth</h2>
          <div className="h-72">
            <ResponsiveContainer>
              <BarChart data={priceHistory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#bbf7d0" />
                <XAxis dataKey="day" stroke="#0f766e" tickLine={false} axisLine={false} />
                <YAxis stroke="#16a34a" tickLine={false} axisLine={false} />
                <Tooltip formatter={(value: number) => `${value.toLocaleString()} holders`} />
                <Legend />
                <Bar dataKey="holders" fill="#0f766e" name="Holders" radius={[12, 12, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="card space-y-6">
        <h2 className="text-lg font-semibold text-dusk">Reward Streams</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {dashboardMetrics.map((metric) => (
            <div key={metric.label} className="card bg-white border-brand-100/80">
              <p className="text-xs font-semibold text-dusk/60 uppercase tracking-[0.3em]">{metric.label}</p>
              <p className="text-2xl font-semibold text-brand-600 mt-2">{metric.value}</p>
              <p className="text-xs text-dusk/50 mt-1">{metric.detail}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
