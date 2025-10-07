'use client';

import { useState } from 'react';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import Image from 'next/image';
import { impactMarkers, impactStories } from '@/lib/data';

const geoUrl = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

export default function ImpactPage() {
  const [selectedProject, setSelectedProject] = useState(impactStories[0]);
  const [formState, setFormState] = useState({
    name: '',
    organization: '',
    email: '',
    summary: ''
  });
  const [submitted, setSubmitted] = useState(false);

  return (
    <div className="section-shell space-y-12">
      <header className="space-y-4 max-w-3xl">
        <span className="badge">Impact Atlas</span>
        <h1 className="text-4xl font-semibold text-dusk">Explore the communities KIND Token powers.</h1>
        <p className="text-lg text-dusk/70">
          Navigate live projects across continents, discover the people behind each initiative, and submit new proposals that
          deserve global attention.
        </p>
      </header>

      <section className="grid xl:grid-cols-[1.2fr,0.8fr] gap-12 items-start">
        <div className="card space-y-6">
          <h2 className="text-lg font-semibold text-dusk">Interactive Map</h2>
          <div className="bg-brand-50/60 rounded-3xl p-4">
            <ComposableMap projectionConfig={{ scale: 150 }} className="w-full h-[420px]">
              <Geographies geography={geoUrl}>
                {({ geographies }) =>
                  geographies.map((geo) => (
                    <Geography
                      key={geo.rsmKey}
                      geography={geo}
                      fill="#e0f2f1"
                      stroke="#a7f3d0"
                      style={{
                        default: { outline: 'none' },
                        hover: { fill: '#bbf7d0', outline: 'none' },
                        pressed: { outline: 'none' }
                      }}
                    />
                  ))
                }
              </Geographies>
              {impactMarkers.map((marker) => (
                <Marker
                  key={marker.projectId}
                  coordinates={marker.coordinates as [number, number]}
                  onClick={() => {
                    const project = impactStories.find((story) => story.id === marker.projectId);
                    if (project) {
                      setSelectedProject(project);
                    }
                  }}
                >
                  <circle r={8} fill={selectedProject.id === marker.projectId ? '#0f766e' : '#22c55e'} stroke="#fff" strokeWidth={2} />
                  <text textAnchor="middle" y={-14} className="fill-brand-600 text-xs font-semibold">
                    {marker.name}
                  </text>
                </Marker>
              ))}
            </ComposableMap>
          </div>
        </div>
        <div className="space-y-6">
          <div className="card">
            <Image
              src={selectedProject.image}
              alt={selectedProject.title}
              width={960}
              height={640}
              className="rounded-2xl object-cover"
            />
            <div className="mt-4 space-y-2">
              <p className="text-sm font-semibold text-brand-500 uppercase tracking-[0.25em]">{selectedProject.location}</p>
              <h3 className="text-2xl font-semibold text-dusk">{selectedProject.title}</h3>
              <p className="text-sm text-dusk/70">{selectedProject.description}</p>
              <p className="text-xs text-dusk/50">{selectedProject.peopleHelped.toLocaleString()} people supported</p>
            </div>
          </div>
          <div className="card space-y-4">
            <h3 className="text-lg font-semibold text-dusk">Submit a Project</h3>
            {submitted ? (
              <p className="text-sm text-brand-600">Thank you! Our impact team will review your proposal within 5 business days.</p>
            ) : (
              <form
                className="space-y-4"
                onSubmit={(event) => {
                  event.preventDefault();
                  setSubmitted(true);
                }}
              >
                <div className="grid md:grid-cols-2 gap-4">
                  <label className="text-sm text-dusk/70 space-y-1">
                    Full Name
                    <input
                      required
                      value={formState.name}
                      onChange={(event) => setFormState({ ...formState, name: event.target.value })}
                      className="w-full rounded-2xl border border-brand-100/70 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-brand-300"
                    />
                  </label>
                  <label className="text-sm text-dusk/70 space-y-1">
                    Organization
                    <input
                      required
                      value={formState.organization}
                      onChange={(event) => setFormState({ ...formState, organization: event.target.value })}
                      className="w-full rounded-2xl border border-brand-100/70 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-brand-300"
                    />
                  </label>
                </div>
                <label className="text-sm text-dusk/70 space-y-1">
                  Email
                  <input
                    type="email"
                    required
                    value={formState.email}
                    onChange={(event) => setFormState({ ...formState, email: event.target.value })}
                    className="w-full rounded-2xl border border-brand-100/70 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-brand-300"
                  />
                </label>
                <label className="text-sm text-dusk/70 space-y-1">
                  Project Summary
                  <textarea
                    required
                    value={formState.summary}
                    rows={4}
                    onChange={(event) => setFormState({ ...formState, summary: event.target.value })}
                    className="w-full rounded-2xl border border-brand-100/70 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-300"
                  />
                </label>
                <button type="submit" className="btn-primary">
                  Submit for Review
                </button>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
