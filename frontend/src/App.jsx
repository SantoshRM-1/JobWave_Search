import React, { useEffect, useMemo, useState } from 'react';
import { AlertTriangle, Bookmark, BriefcaseBusiness, Sparkles, Target } from 'lucide-react';
import { AnimatePresence, motion as Motion } from 'framer-motion';
import JobCard from './components/JobCard';
import SearchBar from './components/SearchBar';

const API_BASE = (import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '')).replace(/\/$/, '');
const PAGE_SIZE = 6;
const thinkingSteps = ['Reading your search', 'Finding current roles', 'Matching your experience', 'Preparing job links'];

function ResumeProfile({ profile }) {
  if (!profile) return null;
  return <section className="mt-7 rounded-2xl border border-cyan-400/15 bg-slate-900/70 p-5"><p className="text-xs font-semibold uppercase tracking-[.18em] text-cyan-300">Resume profile</p><div className="mt-2 flex flex-wrap items-center justify-between gap-3"><h2 className="text-lg font-semibold text-white">{profile.role_preference || 'Career profile'} <span className="text-slate-500">·</span> {profile.experience_level || 'Experience detected'}</h2><span className="rounded-full bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200">{profile.skills?.length || 0} skills found</span></div><div className="mt-4 flex flex-wrap gap-2">{(profile.skills || []).map(skill => <span key={skill} className="rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1 text-xs text-slate-300">{skill}</span>)}</div></section>;
}

export default function App() {
  const [jobs, setJobs] = useState([]), [profile, setProfile] = useState(null), [loading, setLoading] = useState(false), [error, setError] = useState('');
  const [step, setStep] = useState(0), [filters, setFilters] = useState({ remote: false, saved: false, score: 'all' }), [saved, setSaved] = useState(() => new Set(JSON.parse(localStorage.getItem('saved-jobs') || '[]'))), [page, setPage] = useState(1);
  useEffect(() => { if (!loading) return; const id = setInterval(() => setStep(value => (value + 1) % thinkingSteps.length), 900); return () => clearInterval(id); }, [loading]);
  const handleSearch = async ({ query, location, file }) => {
    setLoading(true); setError(''); setJobs([]); setProfile(null); setPage(1); setStep(0);
    const form = new FormData(); form.append('query', query); form.append('location', location); if (file) form.append('resume', file);
    try { const response = await fetch(`${API_BASE}/search`, { method: 'POST', body: form }); const data = await response.json(); if (!response.ok) throw new Error(data.detail || 'Search could not be completed.'); setJobs(data.jobs || []); setProfile(data.resume || null); }
    catch (reason) { setError(reason.message || 'Search could not be completed. Please try again.'); }
    finally { setLoading(false); }
  };
  const toggleSaved = job => setSaved(current => { const next = new Set(current); next.has(job.id) ? next.delete(job.id) : next.add(job.id); localStorage.setItem('saved-jobs', JSON.stringify([...next])); return next; });
  const filtered = useMemo(() => jobs.filter(job => (!filters.remote || /remote/i.test(job.location || '')) && (!filters.saved || saved.has(job.id)) && (filters.score === 'all' || (job.match_score || 0) >= Number(filters.score))), [jobs, filters, saved]);
  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE)); const shown = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
  useEffect(() => setPage(1), [filters]);
  return <main className="min-h-screen overflow-x-hidden bg-[#070b14] text-slate-100 selection:bg-cyan-400/30"><div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_15%_0%,rgba(34,211,238,.12),transparent_26%),radial-gradient(circle_at_92%_20%,rgba(139,92,246,.10),transparent_22%)]" /><div className="relative mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:py-16">
    <header className="mx-auto mb-10 max-w-3xl text-center"><div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-400/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-[.16em] text-cyan-200"><Sparkles className="h-3.5 w-3.5" /> Smart job discovery</div><h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">Find work that fits <span className="text-cyan-300">you.</span></h1><p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-400">Search by role or upload a PDF resume for personalised matches, direct application links, and clear fit reasons.</p></header>
    <SearchBar onSearch={handleSearch} isLoading={loading} />
    <AnimatePresence>{error && <Motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="mx-auto mt-5 flex max-w-4xl gap-3 rounded-xl border border-rose-400/25 bg-rose-400/10 p-4 text-sm text-rose-200"><AlertTriangle className="h-5 w-5 shrink-0" />{error}</Motion.div>}</AnimatePresence>
    {loading && <div className="mx-auto mt-6 max-w-4xl rounded-2xl border border-cyan-400/20 bg-slate-900/80 p-5"><div className="flex items-center gap-3"><span className="h-3 w-3 animate-ping rounded-full bg-cyan-300" /><div><p className="font-semibold text-white">Thinking…</p><p className="text-sm text-cyan-200">{thinkingSteps[step]}</p></div></div><div className="mt-5 grid grid-cols-4 gap-2">{thinkingSteps.map((item, index) => <span key={item} className={`h-1 rounded-full transition-all duration-500 ${index <= step ? 'bg-cyan-300' : 'bg-slate-700'}`} />)}</div></div>}
    <ResumeProfile profile={profile} />
    {jobs.length > 0 && !loading && <section className="mt-12"><div className="mb-6 flex flex-wrap items-end justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-[.16em] text-cyan-300">Search results</p><h2 className="mt-1 text-2xl font-semibold text-white">Roles worth reviewing</h2></div><div className="flex items-center gap-2 rounded-lg border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-slate-400"><BriefcaseBusiness className="h-4 w-4 text-cyan-300" /> {filtered.length} roles</div></div><div className="mb-5 flex flex-wrap gap-3 rounded-xl border border-slate-800 bg-slate-900/70 p-3"><label className="flex items-center gap-2 text-sm text-slate-300"><input type="checkbox" checked={filters.remote} onChange={e => setFilters(f => ({ ...f, remote: e.target.checked }))} /> Remote</label><label className="flex items-center gap-2 text-sm text-slate-300"><input type="checkbox" checked={filters.saved} onChange={e => setFilters(f => ({ ...f, saved: e.target.checked }))} /> <Bookmark className="h-3.5 w-3.5" /> Saved</label><select value={filters.score} onChange={e => setFilters(f => ({ ...f, score: e.target.value }))} className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-white"><option value="all">Any match</option><option value="75">75%+ match</option><option value="55">55%+ match</option></select></div><div className="grid gap-4">{shown.map(job => <JobCard key={job.id} job={job} saved={saved.has(job.id)} onSave={() => toggleSaved(job)} />)}</div>{!shown.length && <p className="rounded-xl border border-dashed border-slate-700 p-8 text-center text-slate-400">No roles match these filters.</p>}{pages > 1 && <nav className="mt-7 flex items-center justify-center gap-3"><button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="rounded-lg border border-slate-700 px-4 py-2 text-sm disabled:opacity-40">Previous</button><span className="text-sm text-slate-400">Page {page} of {pages}</span><button onClick={() => setPage(p => Math.min(pages, p + 1))} disabled={page === pages} className="rounded-lg border border-slate-700 px-4 py-2 text-sm disabled:opacity-40">Next</button></nav>}</section>}
    {!loading && !jobs.length && !error && <div className="mt-12 rounded-2xl border border-dashed border-slate-800 p-10 text-center text-slate-500"><Target className="mx-auto mb-3 h-7 w-7 text-slate-600" />Search a role, upload your resume, or do both.</div>}
  </div></main>;
}
