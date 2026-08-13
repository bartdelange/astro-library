import { ChevronRight, MoreHorizontal, Star } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { Button, Card, EmptyState } from '../../../shared/components';
import { ObjectMeta } from '../components/ObjectMeta';
import { ObjectThumbnail } from '../components/ObjectThumbnail';
import { useObject } from '../hooks/useObjects';
import type { BackendSession, ObjectDetail } from '../types';
import {
  formatDate,
  formatIntegration,
  formatLongDate,
  getCatalogLabel,
  getHeroSeed,
  getObjectName,
  getSessionFiles,
} from '../utils/objectFormat';

export function ObjectDetailView() {
  const { objectId } = useParams();
  const { data: detail, isError, isLoading } = useObject(objectId);

  if (isLoading) {
    return (
      <Card className="p-6 text-sm text-slate-400">Loading object...</Card>
    );
  }

  if (isError || !detail) {
    return (
      <EmptyState
        action={
          <Link
            className="inline-flex h-9 items-center justify-center rounded-md border border-slate-700 bg-slate-900 px-3 text-sm font-medium text-slate-100 transition hover:bg-slate-800"
            to="/objects"
          >
            Back to objects
          </Link>
        }
        description="The requested object could not be loaded from the backend API."
        title={isError ? 'Unable to load object' : 'Object not found'}
      />
    );
  }

  const { object, sessions } = detail;
  const catalog = getCatalogLabel(object);
  const name = getObjectName(object);
  const latestSessions = sessions.slice(0, 4);

  return (
    <div className="space-y-5">
      <div className="flex items-center gap-2 text-xs text-slate-500">
        <Link className="transition hover:text-slate-300" to="/objects">
          Objects
        </Link>
        <ChevronRight className="size-3" />
        <span className="text-slate-300">{catalog}</span>
      </div>

      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-sm font-medium text-sky-300">{catalog}</p>
          <h1 className="mt-1 text-3xl font-semibold text-white">{name}</h1>
          <div className="mt-3 flex flex-wrap gap-2">
            <Pill>{object.object_type ?? 'Unknown type'}</Pill>
            <Pill>{object.constellation ?? 'Unknown constellation'}</Pill>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="secondary">
            <Star className="size-4 text-amber-300" />
            Set as Favorite
          </Button>
          <Button
            aria-label="More actions"
            className="w-10 px-0"
            variant="secondary"
          >
            <MoreHorizontal className="size-4" />
          </Button>
        </div>
      </div>

      <div className="grid gap-4 xl:grid-cols-[minmax(0,1fr)_380px]">
        <ObjectThumbnail
          alt={name}
          className="aspect-[1.85] rounded-lg border border-slate-800"
          file={detail.heroFile}
          seed={getHeroSeed(detail)}
        />

        <Card className="p-5">
          <ObjectMeta object={object} />
          <div className="mt-5 border-t border-slate-800 pt-4">
            <p className="text-xs text-slate-500">Description</p>
            <p className="mt-2 text-xs leading-5 text-slate-300">
              {object.description ??
                'No description has been added for this object yet.'}
            </p>
          </div>
        </Card>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <Metric label="Total Sessions" value={detail.sessionCount.toString()} />
        <Metric
          label="Total Integration"
          value={formatIntegration(detail.totalIntegrationSeconds)}
        />
        <Metric
          label="Best Image"
          value={
            detail.heroFile?.modified_at
              ? formatDate(detail.heroFile.modified_at.slice(0, 10))
              : '-'
          }
        />
        <Metric
          label="First Imaged"
          value={formatDate(getFirstSessionDate(sessions))}
        />
        <Metric
          label="Last Imaged"
          value={formatDate(detail.latestSessionDate)}
        />
      </div>

      <Card className="overflow-hidden">
        <div className="border-b border-slate-800 px-5 py-4">
          <h2 className="text-sm font-semibold text-white">My Sessions</h2>
        </div>
        {latestSessions.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[760px] text-left text-sm">
              <thead className="text-xs text-slate-500">
                <tr>
                  <th className="px-5 py-3 font-medium">Date</th>
                  <th className="px-5 py-3 font-medium">Integration</th>
                  <th className="px-5 py-3 font-medium">Files</th>
                  <th className="px-5 py-3 font-medium">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {latestSessions.map((session) => (
                  <SessionRow
                    detail={detail}
                    key={session.id}
                    session={session}
                  />
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="px-5 py-8 text-sm text-slate-500">
            No sessions recorded.
          </div>
        )}
      </Card>
    </div>
  );
}

function SessionRow({
  detail,
  session,
}: {
  detail: ObjectDetail;
  session: BackendSession;
}) {
  const files = getSessionFiles(session, detail.files);

  return (
    <tr className="text-slate-300">
      <td className="px-5 py-3">
        <div className="flex items-center gap-3">
          <ObjectThumbnail
            alt={formatLongDate(session.date)}
            className="h-11 w-16 rounded border border-slate-800"
            file={files[0] ?? detail.heroFile}
            seed={`${detail.object.slug}-${session.id}`}
          />
          <span className="text-xs font-medium text-slate-200">
            {session.date}
          </span>
        </div>
      </td>
      <td className="px-5 py-3 text-xs">
        {formatIntegration(session.integration_seconds)}
      </td>
      <td className="px-5 py-3 text-xs">{files.length}</td>
      <td className="px-5 py-3 text-xs text-slate-400">
        {session.notes ?? 'No notes'}
      </td>
    </tr>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <Card className="px-4 py-3 text-center">
      <p className="text-[11px] text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-semibold text-slate-100">{value}</p>
    </Card>
  );
}

function Pill({ children }: { children: string }) {
  return (
    <span className="rounded bg-slate-800 px-2 py-1 text-[11px] font-medium text-slate-300">
      {children}
    </span>
  );
}

function getFirstSessionDate(sessions: BackendSession[]) {
  if (sessions.length === 0) {
    return null;
  }

  return sessions
    .map((session) => session.date)
    .sort((a, b) => a.localeCompare(b))[0];
}
