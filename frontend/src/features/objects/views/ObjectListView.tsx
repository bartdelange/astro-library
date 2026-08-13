import { Grid2X2, ListFilter, Search } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Button, Card, EmptyState } from '../../../shared/components';
import { ObjectThumbnail } from '../components/ObjectThumbnail';
import { useObjects } from '../hooks/useObjects';
import {
  formatIntegration,
  getCatalogLabel,
  getHeroSeed,
  getObjectName,
} from '../utils/objectFormat';

export function ObjectListView() {
  const { data, isError, isLoading } = useObjects();
  const objects = data?.objects ?? [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-white">Objects</h1>
          <p className="mt-1 text-sm text-slate-400">
            {isLoading ? 'Loading catalog...' : `${objects.length} objects`}
          </p>
        </div>

        <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
          <label className="relative block w-full sm:w-72">
            <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-slate-500" />
            <input
              className="h-10 w-full rounded-md border border-slate-700 bg-[#0b1119] pr-3 pl-9 text-sm text-slate-100 transition outline-none placeholder:text-slate-500 focus:border-sky-500"
              placeholder="Search objects..."
              type="search"
            />
          </label>
          <Button className="justify-between" variant="secondary">
            <ListFilter className="size-4" />
            Filter
          </Button>
          <Button className="justify-between" variant="secondary">
            Sort: Last Imaged
          </Button>
          <Button
            aria-label="Grid view"
            className="w-10 px-0"
            variant="secondary"
          >
            <Grid2X2 className="size-4" />
          </Button>
        </div>
      </div>

      {isError ? (
        <EmptyState
          description="The catalog could not be loaded from the backend API."
          title="Unable to load objects"
        />
      ) : isLoading ? (
        <ObjectGridSkeleton />
      ) : objects.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {objects.map((summary) => {
            const name = getObjectName(summary.object);
            const catalog = getCatalogLabel(summary.object);

            return (
              <Link
                className="group overflow-hidden rounded-lg border border-slate-800 bg-slate-900/70 transition hover:-translate-y-0.5 hover:border-slate-600 hover:bg-slate-900"
                key={summary.object.id}
                to={`/objects/${summary.object.id}`}
              >
                <ObjectThumbnail
                  alt={name}
                  className="aspect-[1.55] border-b border-slate-800"
                  file={summary.heroFile}
                  seed={getHeroSeed(summary)}
                />
                <div className="space-y-3 p-3">
                  <div>
                    <h2 className="text-sm font-semibold text-white">
                      {catalog}
                    </h2>
                    <p className="mt-1 truncate text-xs text-slate-400">
                      {name}
                    </p>
                  </div>
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>
                      {summary.sessionCount}{' '}
                      {summary.sessionCount === 1 ? 'session' : 'sessions'}
                    </span>
                    <span>
                      {formatIntegration(summary.totalIntegrationSeconds)}
                    </span>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      ) : (
        <EmptyState
          description="Objects will appear here once records exist in the backend catalog."
          title="No objects found"
        />
      )}

      {!isLoading && objects.length > 0 ? (
        <p className="text-xs text-slate-500">
          Showing 1-{objects.length} of {objects.length} objects
        </p>
      ) : null}
    </div>
  );
}

function ObjectGridSkeleton() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {Array.from({ length: 8 }).map((_, index) => (
        <Card className="overflow-hidden" key={index}>
          <div className="aspect-[1.55] animate-pulse bg-slate-800" />
          <div className="space-y-3 p-3">
            <div className="h-4 w-20 rounded bg-slate-800" />
            <div className="h-3 w-32 rounded bg-slate-800" />
            <div className="flex justify-between">
              <div className="h-3 w-16 rounded bg-slate-800" />
              <div className="h-3 w-12 rounded bg-slate-800" />
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
