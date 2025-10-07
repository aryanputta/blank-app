'use client';

import { useState } from 'react';

export default function ContactPage() {
  const [formState, setFormState] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="section-shell space-y-12">
      <header className="space-y-4 max-w-2xl">
        <span className="badge">Contact</span>
        <h1 className="text-4xl font-semibold text-dusk">We’d love to hear from you.</h1>
        <p className="text-lg text-dusk/70">
          Reach the KIND Foundation team for partnerships, media requests, or community questions. We respond within two
          business days.
        </p>
      </header>

      <section className="grid lg:grid-cols-[1fr,0.9fr] gap-12 items-start">
        <div className="card space-y-6">
          <h2 className="text-lg font-semibold text-dusk">Send a Message</h2>
          {submitted ? (
            <p className="text-sm text-brand-600">Thanks for reaching out! Our team will be in touch soon.</p>
          ) : (
            <form
              className="space-y-4"
              onSubmit={(event) => {
                event.preventDefault();
                setSubmitted(true);
              }}
            >
              <label className="text-sm text-dusk/70 space-y-1">
                Full Name
                <input
                  required
                  value={formState.name}
                  onChange={(event) => setFormState({ ...formState, name: event.target.value })}
                  className="w-full rounded-2xl border border-brand-100/70 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-300"
                />
              </label>
              <label className="text-sm text-dusk/70 space-y-1">
                Email
                <input
                  type="email"
                  required
                  value={formState.email}
                  onChange={(event) => setFormState({ ...formState, email: event.target.value })}
                  className="w-full rounded-2xl border border-brand-100/70 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-300"
                />
              </label>
              <label className="text-sm text-dusk/70 space-y-1">
                Message
                <textarea
                  required
                  value={formState.message}
                  rows={4}
                  onChange={(event) => setFormState({ ...formState, message: event.target.value })}
                  className="w-full rounded-2xl border border-brand-100/70 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-300"
                />
              </label>
              <button type="submit" className="btn-primary">
                Send Message
              </button>
            </form>
          )}
        </div>
        <div className="space-y-6">
          <div className="card space-y-3">
            <h3 className="text-lg font-semibold text-dusk">Foundation Headquarters</h3>
            <p className="text-sm text-dusk/70">144 Kindness Avenue, Suite 12 · San Francisco, CA 94105</p>
            <p className="text-sm text-dusk/70">Email: foundation@kind.earth</p>
            <p className="text-sm text-dusk/70">Media: press@kind.earth</p>
          </div>
          <div className="card space-y-3">
            <h3 className="text-lg font-semibold text-dusk">Compliance & Security</h3>
            <p className="text-sm text-dusk/70">HTTPS enforced • Smart contract audits • SOC2-aligned data practices</p>
            <div className="grid sm:grid-cols-3 gap-3 text-xs text-dusk/60">
              <a href="/terms" className="rounded-2xl border border-brand-100/70 px-4 py-3 text-center">
                Terms of Use
              </a>
              <a href="/privacy" className="rounded-2xl border border-brand-100/70 px-4 py-3 text-center">
                Privacy Policy
              </a>
              <a href="/risk" className="rounded-2xl border border-brand-100/70 px-4 py-3 text-center">
                Risk Disclosure
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
