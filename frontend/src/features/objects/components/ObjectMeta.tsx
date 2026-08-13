import type { BackendAstroObject } from '../types';

type ObjectMetaProps = {
  object: BackendAstroObject;
};

export function ObjectMeta({ object }: ObjectMetaProps) {
  return (
    <dl className="grid gap-x-6 gap-y-3 text-sm sm:grid-cols-[140px_1fr]">
      <MetaItem
        label="Also known as"
        value={object.aliases?.slice(0, 3).join(', ') || '-'}
      />
      <MetaItem label="Right Ascension" value={formatCoordinate(object.ra)} />
      <MetaItem label="Declination" value={formatCoordinate(object.dec)} />
      <MetaItem label="Magnitude" value={object.magnitude?.toString() ?? '-'} />
      <MetaItem label="Size" value={object.angular_size_display ?? '-'} />
      <MetaItem label="Distance" value={object.distance_display ?? '-'} />
    </dl>
  );
}

function MetaItem({ label, value }: { label: string; value: string }) {
  return (
    <>
      <dt className="text-xs text-slate-500">{label}</dt>
      <dd className="text-xs font-medium text-slate-200">{value}</dd>
    </>
  );
}

function formatCoordinate(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return '-';
  }

  return value.toFixed(4);
}
