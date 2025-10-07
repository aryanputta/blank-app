'use client';

import { Disclosure } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/24/outline';
import { learnTopics } from '@/lib/data';

export default function LearnPage() {
  return (
    <div className="section-shell space-y-12">
      <header className="space-y-4 max-w-3xl">
        <span className="badge">Learn KIND</span>
        <h1 className="text-4xl font-semibold text-dusk">Discover the strategy behind the world’s kindest blockchain.</h1>
        <p className="text-lg text-dusk/70">
          Dive into curated modules that make the KIND whitepaper approachable for new explorers and seasoned investors alike.
        </p>
        <a
          href="/KIND-Token-Whitepaper.pdf"
          className="btn-primary inline-flex w-fit"
        >
          Download Full Whitepaper
        </a>
      </header>

      <section className="grid lg:grid-cols-[1.1fr,0.9fr] gap-12 items-start">
        <div className="space-y-4">
          {learnTopics.map((topic) => (
            <Disclosure key={topic.title}>
              {({ open }) => (
                <div className="card">
                  <Disclosure.Button className="w-full flex items-center justify-between text-left">
                    <div className="flex items-center gap-4">
                      <span className="text-2xl">{topic.icon}</span>
                      <div>
                        <p className="text-lg font-semibold text-dusk">{topic.title}</p>
                        <p className="text-sm text-dusk/60">{topic.description}</p>
                      </div>
                    </div>
                    <ChevronDownIcon className={`h-5 w-5 text-brand-500 transition-transform ${open ? 'rotate-180' : ''}`} />
                  </Disclosure.Button>
                  <Disclosure.Panel className="mt-4 text-sm text-dusk/70">
                    Access case studies, governance playbooks, and implementation tutorials tailored to your preferred depth.
                  </Disclosure.Panel>
                </div>
              )}
            </Disclosure>
          ))}
        </div>
        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-dusk">Interactive Curriculum</h2>
          <ul className="space-y-3 text-sm text-dusk/70">
            <li>
              <span className="font-semibold text-dusk">Video Library:</span> Guided walkthroughs of mission, tokenomics, and
              governance mechanics.
            </li>
            <li>
              <span className="font-semibold text-dusk">Office Hours:</span> Weekly AMAs with engineers, climate scientists, and
              policy advisors.
            </li>
            <li>
              <span className="font-semibold text-dusk">Impact Labs:</span> Build prototypes using KIND APIs and receive micro-grants
              for promising pilots.
            </li>
          </ul>
          <div className="rounded-3xl bg-brand-50/60 border border-brand-100/70 p-6 space-y-3">
            <p className="text-sm font-semibold text-brand-600 uppercase tracking-[0.3em]">Certification</p>
            <p className="text-lg font-semibold text-dusk">Earn the "Certified Kindness Architect" badge.</p>
            <p className="text-xs text-dusk/60">Complete the coursework to unlock governance boosts and mentorship circles.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
