'use client';

import { useState } from 'react';
import { events, kindnessLeaders } from '@/lib/data';

export default function JoinPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="section-shell space-y-12">
      <header className="space-y-4 max-w-3xl">
        <span className="badge">Join KIND</span>
        <h1 className="text-4xl font-semibold text-dusk">Step into a community where generosity compounds.</h1>
        <p className="text-lg text-dusk/70">
          Subscribe, connect, and celebrate impact with peers leading the humanitarian finance movement.
        </p>
      </header>

      <section id="newsletter" className="grid lg:grid-cols-2 gap-12 items-start">
        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-dusk">Stay in the Loop</h2>
          <p className="text-sm text-dusk/60">
            Receive launch alerts, governance invitations, and impact reporting directly to your inbox.
          </p>
          {submitted ? (
            <p className="text-sm text-brand-600">Thank you for joining our newsletter! Check your inbox for a welcome note.</p>
          ) : (
            <form
              className="flex flex-col gap-4"
              onSubmit={(event) => {
                event.preventDefault();
                setSubmitted(true);
              }}
            >
              <input
                required
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.org"
                className="rounded-2xl border border-brand-100/70 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-300"
              />
              <button type="submit" className="btn-primary">
                Subscribe
              </button>
            </form>
          )}
        </div>
        <div className="card space-y-6">
          <h2 className="text-lg font-semibold text-dusk">Connect With Us</h2>
          <div className="grid sm:grid-cols-2 gap-4 text-sm text-dusk/70">
            {[
              { label: 'Twitter', handle: '@KINDToken', href: 'https://twitter.com/KINDToken' },
              { label: 'Discord', handle: 'discord.gg/kindtoken', href: 'https://discord.gg/kindtoken' },
              { label: 'Telegram', handle: 't.me/kindtoken', href: 'https://t.me/kindtoken' },
              { label: 'LinkedIn', handle: 'KIND Foundation', href: 'https://linkedin.com/company/kind-token' }
            ].map((item) => (
              <a
                key={item.label}
                href={item.href}
                className="rounded-2xl border border-brand-100/70 p-4 hover:border-brand-300 hover:bg-brand-50/60 transition"
              >
                <p className="text-sm font-semibold text-dusk">{item.label}</p>
                <p className="text-xs text-dusk/60">{item.handle}</p>
              </a>
            ))}
          </div>
        </div>
      </section>

      <section className="grid xl:grid-cols-[0.8fr,1.2fr] gap-12 items-start">
        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-dusk">Live Events Calendar</h2>
          <ul className="space-y-3 text-sm text-dusk/70">
            {events.map((event) => (
              <li key={event.title} className="rounded-2xl border border-brand-100/70 px-4 py-3">
                <p className="text-xs font-semibold text-brand-600 uppercase tracking-[0.3em]">
                  {new Date(event.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                </p>
                <p className="text-sm font-semibold text-dusk">{event.title}</p>
                <p className="text-xs text-dusk/50">{event.type}</p>
              </li>
            ))}
          </ul>
        </div>
        <div className="card space-y-6">
          <h2 className="text-lg font-semibold text-dusk">Kindness Leaderboard</h2>
          <p className="text-sm text-dusk/60">Celebrate top contributors and inspire friendly collaboration.</p>
          <div className="space-y-4">
            {kindnessLeaders.map((leader, index) => (
              <div
                key={leader.name}
                className="flex items-center justify-between rounded-2xl border border-brand-100/70 px-4 py-3 bg-brand-50/60"
              >
                <div>
                  <p className="text-sm font-semibold text-dusk">
                    #{index + 1} {leader.name}
                  </p>
                  <p className="text-xs text-dusk/60">{leader.impact}</p>
                </div>
                <span className="text-lg">{leader.badge}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
