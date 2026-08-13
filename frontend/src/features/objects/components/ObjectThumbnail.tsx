import type { BackendFile } from '../types';

type ObjectThumbnailProps = {
  alt: string;
  className?: string;
  file?: BackendFile | null;
  seed: string;
};

export function ObjectThumbnail({
  alt,
  className = '',
  file,
  seed,
}: ObjectThumbnailProps) {
  const variant = getVariant(seed);

  return (
    <div
      aria-label={alt}
      className={`relative overflow-hidden bg-slate-950 ${className}`}
      role="img"
    >
      <div className={`absolute inset-0 ${variant.background}`} />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_18%,rgba(255,255,255,0.9)_0_1px,transparent_2px),radial-gradient(circle_at_70%_28%,rgba(255,255,255,0.8)_0_1px,transparent_2px),radial-gradient(circle_at_84%_75%,rgba(255,255,255,0.7)_0_1px,transparent_2px),radial-gradient(circle_at_42%_62%,rgba(255,255,255,0.65)_0_1px,transparent_2px)] opacity-80" />
      <div className={`absolute ${variant.object}`} />
      <div className="absolute inset-0 bg-gradient-to-b from-white/0 via-white/0 to-black/35" />
      {file ? (
        <div className="absolute right-2 bottom-2 rounded bg-black/45 px-1.5 py-0.5 text-[10px] font-medium text-slate-200 uppercase">
          {file.file_role}
        </div>
      ) : null}
    </div>
  );
}

function getVariant(seed: string) {
  const variants = [
    {
      background:
        'bg-[radial-gradient(circle_at_42%_45%,rgba(45,212,191,0.28),transparent_22%),radial-gradient(circle_at_58%_48%,rgba(248,113,113,0.32),transparent_18%),linear-gradient(135deg,#030712,#111827_58%,#020617)]',
      object:
        'left-[24%] top-[18%] h-[64%] w-[52%] rounded-full bg-cyan-300/40 blur-[1px] ring-8 ring-rose-400/25',
    },
    {
      background:
        'bg-[radial-gradient(ellipse_at_center,rgba(226,232,240,0.55),transparent_22%),radial-gradient(ellipse_at_42%_48%,rgba(251,146,60,0.24),transparent_30%),linear-gradient(135deg,#020617,#111827)]',
      object:
        'left-[13%] top-[39%] h-[18%] w-[76%] rotate-[-14deg] rounded-full bg-slate-200/60 shadow-[0_0_28px_rgba(255,255,255,0.25)]',
    },
    {
      background:
        'bg-[radial-gradient(circle_at_52%_48%,rgba(56,189,248,0.18),transparent_16%),radial-gradient(circle_at_50%_50%,rgba(248,113,113,0.38),transparent_34%),linear-gradient(135deg,#030712,#1f2937)]',
      object:
        'left-[32%] top-[19%] h-[62%] w-[38%] rounded-[45%] bg-rose-400/35 blur-[2px] ring-8 ring-cyan-300/15',
    },
    {
      background:
        'bg-[conic-gradient(from_210deg_at_52%_50%,#020617,#1e3a8a,#7f1d1d,#0f172a,#020617)]',
      object:
        'left-[22%] top-[22%] h-[56%] w-[56%] rounded-full border-[14px] border-sky-300/20 bg-transparent shadow-[inset_0_0_32px_rgba(255,255,255,0.16),0_0_22px_rgba(96,165,250,0.22)]',
    },
  ];

  return variants[hash(seed) % variants.length];
}

function hash(value: string) {
  return value
    .split('')
    .reduce((total, character) => total + character.charCodeAt(0), 0);
}
