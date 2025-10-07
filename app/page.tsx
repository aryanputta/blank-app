'use client';

import { useEffect, useMemo, useState } from 'react';
import { roadmap, teamMembers, impactStories, kindnessStories } from '@/lib/data';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { PlayCircleIcon } from '@heroicons/react/24/solid';

const counters = [
  { label: 'Investors', target: 18432 },
  { label: 'Projects Funded', target: 54 },
  { label: 'People Impacted', target: 1624000 }
];

function useAnimatedCounter(target: number) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    let frame = 0;
    const totalFrames = 60;
    const animation = () => {
      frame += 1;
      const progress = Math.min(frame / totalFrames, 1);
      setValue(Math.floor(progress * target));
      if (progress < 1) {
        requestAnimationFrame(animation);
      }
    };

    animation();
  }, [target]);

  return value.toLocaleString();
}

const impactCategories = [
  { label: 'Meals Funded', icon: '🍲', multiplier: 1 },
  { label: 'Hours of Clean Power', icon: '🔋', multiplier: 0.4 },
  { label: 'Climate Research Grants', icon: '🔬', multiplier: 0.02 }
];

export default function HomePage() {
  const heroCounters = counters.map((counter) => ({
    ...counter,
    value: useAnimatedCounter(counter.target)
  }));
  const [investment, setInvestment] = useState(5000);
  const [selectedStory, setSelectedStory] = useState(impactStories[0]);

  const impactResult = useMemo(() => {
    return impactCategories.map((category) => ({
      ...category,
      amount: Math.round(investment * category.multiplier)
    }));
  }, [investment]);

  return (
    <div>
      <section className="section-shell pt-12 lg:pt-16">
        <div className="grid lg:grid-cols-2 gap-14 items-center">
          <div className="space-y-8">
            <span className="badge">Carbon-Negative. Community Positive.</span>
            <h1 className="text-4xl md:text-5xl xl:text-6xl font-bold text-dusk leading-tight">
              Invest in Compassion. <span className="text-ocean">Grow with Kindness.</span>
            </h1>
            <p className="text-lg text-dusk/70 max-w-xl">
              KIND Token fuses high-performance blockchain infrastructure with a nonprofit ethos, ensuring every transaction
              regenerates the planet and uplifts communities.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link href="/token" className="btn-primary">
                Buy KIND
              </Link>
              <Link href="/dashboard" className="btn-secondary">
                View Dashboard
              </Link>
            </div>
            <div className="grid sm:grid-cols-3 gap-6 pt-6">
              {heroCounters.map((counter) => (
                <div key={counter.label} className="card text-center">
                  <p className="text-3xl font-semibold text-ocean">{counter.value}</p>
                  <p className="text-sm text-dusk/60">{counter.label}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="relative">
            <div className="gradient-border">
              <div className="card relative overflow-hidden">
                <p className="text-sm font-semibold text-brand-600 uppercase tracking-[0.3em]">Impact Flywheel</p>
                <div className="mt-6 space-y-6">
                  {['Invest', 'Deploy', 'Measure', 'Reinvest'].map((step, index) => (
                    <motion.div
                      key={step}
                      initial={{ opacity: 0, x: 40 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 * index }}
                      className="flex items-start gap-4"
                    >
                      <div className="mt-1 h-12 w-12 rounded-full bg-brand-100 flex items-center justify-center text-brand-600 font-semibold shadow-soft">
                        {index + 1}
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-dusk">{step}</h3>
                        <p className="text-sm text-dusk/70">
                          {[
                            'Capital flows from investors into the KIND treasury with transparent on-chain routing.',
                            'Funds activate vetted climate and humanitarian partners delivering measurable change.',
                            'AI-driven oracles verify outcomes and publish impact NFTs for every supporter.',
                            'Returns and rewards cycle back into new projects, compounding global good.'
                          ][index]}
                        </p>
                      </div>
                    </motion.div>
                  ))}
                </div>
                <motion.div
                  className="absolute -right-10 top-1/2 hidden xl:block"
                  animate={{ y: [0, -12, 0] }}
                  transition={{ repeat: Infinity, duration: 6, ease: 'easeInOut' }}
                >
                  <Image
                    src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=420&q=80"
                    alt="Impact visualization"
                    width={240}
                    height={240}
                    className="rounded-full border-8 border-white shadow-soft"
                  />
                </motion.div>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-12 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-8 bg-white/80 backdrop-blur rounded-3xl border border-brand-100/60 p-8">
          <div>
            <p className="text-sm font-semibold text-brand-600 uppercase tracking-[0.3em]">Stay Connected</p>
            <h2 className="text-2xl font-semibold text-dusk mt-2">Join a movement where kindness compounds.</h2>
            <p className="text-sm text-dusk/70">Connect your wallet or subscribe to receive impact updates and launch alerts.</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <Link href="/dashboard" className="btn-primary">
              Connect Wallet
            </Link>
            <Link href="/join#newsletter" className="btn-secondary">
              Subscribe to Updates
            </Link>
          </div>
        </div>
      </section>

      <section className="section-shell bg-brand-50/40">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <span className="badge">About KIND</span>
            <h2 className="text-3xl font-semibold text-dusk">Mission & Vision</h2>
            <p className="text-lg text-dusk/70">
              We believe finance can nourish people and the planet. KIND Token mobilizes capital to frontline projects, tracks
              verified outcomes in real time, and rewards every contributor with transparent returns.
            </p>
            <div className="grid sm:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-xl font-semibold text-dusk">Mission</h3>
                <p className="text-sm text-dusk/70 mt-3">
                  Deploy regenerative finance that reverses climate change and funds compassionate initiatives globally.
                </p>
              </div>
              <div className="card">
                <h3 className="text-xl font-semibold text-dusk">Vision</h3>
                <p className="text-sm text-dusk/70 mt-3">
                  Build the world’s most trusted carbon-negative blockchain and inspire a new era of empathetic economies.
                </p>
              </div>
            </div>
            <div className="card flex items-center gap-4">
              <PlayCircleIcon className="h-12 w-12 text-brand-500" />
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-brand-500 font-semibold">Watch</p>
                <p className="text-lg text-dusk font-semibold">Stories of kindness in motion (2:04)</p>
                <p className="text-sm text-dusk/60">Hear from beneficiaries, builders, and backers of the KIND movement.</p>
              </div>
            </div>
          </div>
          <div className="space-y-8">
            <div className="gradient-border">
              <div className="card">
                <h3 className="text-lg font-semibold text-dusk">Roadmap</h3>
                <div className="mt-6 space-y-6">
                  {roadmap.map((item) => (
                    <div key={item.quarter} className="flex gap-4">
                      <div className="flex-shrink-0 w-24 text-sm font-semibold text-ocean">{item.quarter}</div>
                      <div>
                        <p className="text-base font-semibold text-dusk">{item.title}</p>
                        <p className="text-sm text-dusk/70">{item.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="card">
              <h3 className="text-lg font-semibold text-dusk mb-4">Our Team</h3>
              <div className="grid gap-6 sm:grid-cols-3">
                {teamMembers.map((member) => (
                  <div key={member.name} className="text-center">
                    <Image
                      src={member.image}
                      alt={member.name}
                      width={96}
                      height={96}
                      className="mx-auto rounded-full object-cover"
                    />
                    <p className="mt-3 text-sm font-semibold text-dusk">{member.name}</p>
                    <p className="text-xs text-brand-600">{member.role}</p>
                    <p className="text-xs text-dusk/60 mt-2">{member.bio}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-shell">
        <div className="grid lg:grid-cols-[1.1fr,0.9fr] gap-12 items-start">
          <div className="space-y-6">
            <span className="badge">AI Impact Calculator</span>
            <h2 className="text-3xl font-semibold text-dusk">See what your kindness can change today.</h2>
            <p className="text-sm text-dusk/70 max-w-2xl">
              Our AI inference engine blends on-chain data with third-party verification to forecast the humanitarian ripple
              effects of every contribution.
            </p>
            <div className="card space-y-6">
              <label className="flex flex-col gap-2">
                <span className="text-sm font-semibold text-dusk">Investment Amount (USD)</span>
                <input
                  type="range"
                  min={100}
                  max={25000}
                  step={100}
                  value={investment}
                  onChange={(event) => setInvestment(Number(event.target.value))}
                  className="w-full"
                />
                <span className="text-2xl font-semibold text-ocean">${investment.toLocaleString()}</span>
              </label>
              <div className="grid md:grid-cols-3 gap-4">
                {impactResult.map((item) => (
                  <div key={item.label} className="card bg-brand-50/60">
                    <p className="text-2xl font-semibold text-brand-600 flex items-center gap-2">
                      <span>{item.icon}</span>
                      {item.amount.toLocaleString()}
                    </p>
                    <p className="text-xs text-dusk/60">{item.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="space-y-6">
            <span className="badge">Stories of Kindness</span>
            <div className="card">
              <Image
                src={selectedStory.image}
                alt={selectedStory.title}
                width={960}
                height={640}
                className="rounded-2xl object-cover"
              />
              <div className="mt-4 space-y-2">
                <p className="text-sm font-semibold text-brand-500 uppercase tracking-[0.25em]">{selectedStory.location}</p>
                <h3 className="text-2xl font-semibold text-dusk">{selectedStory.title}</h3>
                <p className="text-sm text-dusk/70">{selectedStory.description}</p>
                <p className="text-xs text-dusk/50">{selectedStory.peopleHelped.toLocaleString()} people empowered</p>
              </div>
            </div>
            <div className="flex gap-4 overflow-x-auto pb-2">
              {impactStories.map((story) => (
                <button
                  key={story.id}
                  onClick={() => setSelectedStory(story)}
                  className={`min-w-[200px] card text-left transition hover:border-brand-300 ${
                    selectedStory.id === story.id ? 'border-brand-400 shadow-soft' : 'opacity-70'
                  }`}
                >
                  <p className="text-sm font-semibold text-dusk">{story.title}</p>
                  <p className="text-xs text-dusk/60">{story.location}</p>
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="section-shell bg-brand-50/40">
        <div className="space-y-6 text-center max-w-4xl mx-auto">
          <span className="badge">Voices from the movement</span>
          <h2 className="text-3xl font-semibold text-dusk">Kindness is a network effect.</h2>
          <p className="text-sm text-dusk/70">
            Supporters around the world share how KIND Token transforms capital into hope.
          </p>
        </div>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {kindnessStories.map((story) => (
            <div key={story.id} className="card h-full flex flex-col gap-4">
              <Image
                src={story.image}
                alt={story.name}
                width={160}
                height={160}
                className="rounded-full object-cover mx-auto"
              />
              <p className="text-sm text-dusk/70">“{story.quote}”</p>
              <p className="text-sm font-semibold text-dusk text-center">— {story.name}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
