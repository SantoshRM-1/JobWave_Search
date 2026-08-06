import React, { useEffect, useState } from 'react';
import { CheckCircle2, LoaderCircle } from 'lucide-react';

const API_BASE = (import.meta.env.VITE_API_BASE || (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '')).replace(/\/$/, '');

export default function AgentThoughtPanel({ sessionId, onComplete }) {
  const [status, setStatus] = useState(''); const [done, setDone] = useState(false);
  useEffect(() => {
    if (!sessionId) return undefined;
    const source = new EventSource(`${API_BASE}/agent-stream/${sessionId}`);
    const finish = () => { source.close(); setDone(true); onComplete?.(); };
    source.onmessage = event => { try { const message = JSON.parse(event.data); if (message.type === 'END') finish(); else if (message.message) setStatus(message.message); } catch { /* Ignore malformed stream updates. */ } };
    source.onerror = finish;
    return () => source.close();
  }, [sessionId, onComplete]);
  if (!sessionId) return null;
  return <div className="mx-auto mt-5 flex max-w-4xl items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/70 px-4 py-3 text-sm"><div className="rounded-full bg-cyan-300/10 p-1.5">{done ? <CheckCircle2 className="h-4 w-4 text-emerald-300"/> : <LoaderCircle className="h-4 w-4 animate-spin text-cyan-300"/>}</div><span className="min-w-0 truncate text-slate-300">{done ? 'Search complete — loading results.' : status}</span></div>;
}
