import type {
  BackendAstroObject,
  BackendFile,
  BackendSession,
  ObjectSummary,
} from '../types';

export function getObjectName(object: BackendAstroObject) {
  return object.display_name ?? object.primary_name;
}

export function getCatalogLabel(object: BackendAstroObject) {
  const catalogValues = Object.values(object.catalog_ids ?? {});

  return catalogValues[0] ?? object.primary_name;
}

export function formatIntegration(seconds: number | null | undefined) {
  if (!seconds) {
    return '0 h';
  }

  const hours = seconds / 3600;

  return `${hours.toLocaleString(undefined, {
    maximumFractionDigits: hours >= 10 ? 0 : 1,
    minimumFractionDigits: hours > 0 && hours < 10 ? 1 : 0,
  })} h`;
}

export function formatDate(date: string | null | undefined) {
  if (!date) {
    return '-';
  }

  return new Intl.DateTimeFormat(undefined, {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${date}T00:00:00`));
}

export function formatLongDate(date: string | null | undefined) {
  if (!date) {
    return 'No sessions';
  }

  return new Intl.DateTimeFormat(undefined, {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(`${date}T00:00:00`));
}

export function formatBytes(bytes: number | null | undefined) {
  if (!bytes) {
    return '-';
  }

  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex += 1;
  }

  return `${size.toFixed(size >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

export function getSessionFiles(session: BackendSession, files: BackendFile[]) {
  return files.filter((file) => file.session_id === session.id);
}

export function getHeroSeed(summary: ObjectSummary) {
  return `${summary.object.slug}-${summary.heroFile?.filename ?? summary.object.id}`;
}
