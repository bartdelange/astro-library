import type {
  BackendAstroObject,
  BackendFile,
  BackendProject,
  BackendSession,
  ObjectSummary,
} from '../types';

export function buildObjectSummary(
  object: BackendAstroObject,
  allProjects: BackendProject[],
  allSessions: BackendSession[],
  allFiles: BackendFile[],
): ObjectSummary {
  const projects = allProjects.filter(
    (project) => project.object_id === object.id,
  );
  const projectIds = new Set(projects.map((project) => project.id));
  const sessions = allSessions.filter((session) =>
    projectIds.has(session.project_id),
  );
  const files = allFiles.filter((file) => projectIds.has(file.project_id));
  const heroFile = findHeroFile(object, projects, files);
  const latestSessionDate =
    sessions.length > 0
      ? sessions
          .map((session) => session.date)
          .sort((a, b) => b.localeCompare(a))[0]
      : null;

  return {
    object,
    projects,
    sessions,
    files,
    heroFile,
    sessionCount: sessions.length,
    totalIntegrationSeconds: sessions.reduce(
      (total, session) => total + (session.integration_seconds ?? 0),
      0,
    ),
    latestSessionDate,
  };
}

export function sortObjectSummaries(objects: ObjectSummary[]) {
  return [...objects].sort((a, b) =>
    displayName(a.object).localeCompare(displayName(b.object)),
  );
}

function findHeroFile(
  object: BackendAstroObject,
  projects: BackendProject[],
  files: BackendFile[],
): BackendFile | null {
  const heroFileIds = [
    object.hero_file_id,
    ...projects.map((project) => project.hero_file_id),
  ].filter(
    (fileId): fileId is number => fileId !== null && fileId !== undefined,
  );

  return (
    files.find((file) => heroFileIds.includes(file.id)) ??
    files.find((file) => file.file_role === 'EXPORT') ??
    files.find((file) => file.file_role === 'EDIT') ??
    files.find((file) => file.file_role === 'LIGHT') ??
    null
  );
}

function displayName(object: BackendAstroObject) {
  return object.display_name ?? object.primary_name;
}
