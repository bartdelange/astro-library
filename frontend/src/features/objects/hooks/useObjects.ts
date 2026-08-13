import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import type { ObjectDetail, ObjectsResponse } from '../types';
import {
  getAstroObject,
  getAstroObjects,
  getFiles,
  getProjects,
  getSessions,
} from '../api/objectApi';
import {
  buildObjectSummary,
  sortObjectSummaries,
} from '../utils/objectSummary';

const objectKeys = {
  all: ['objects'] as const,
  lists: () => [...objectKeys.all, 'list'] as const,
  detail: (objectId: number) =>
    [...objectKeys.all, 'detail', objectId] as const,
  projects: (objectId?: number) =>
    objectId
      ? ([...objectKeys.all, 'projects', objectId] as const)
      : (['projects'] as const),
  sessions: (projectIds?: number[]) =>
    projectIds
      ? ([...objectKeys.all, 'sessions', projectIds] as const)
      : (['sessions'] as const),
  files: (projectIds?: number[]) =>
    projectIds
      ? ([...objectKeys.all, 'files', projectIds] as const)
      : (['files'] as const),
};

export function useObjects() {
  const objectsQuery = useQuery({
    queryKey: objectKeys.lists(),
    queryFn: getAstroObjects,
  });
  const projectsQuery = useQuery({
    queryKey: objectKeys.projects(),
    queryFn: () => getProjects(),
  });
  const sessionsQuery = useQuery({
    queryKey: objectKeys.sessions(),
    queryFn: () => getSessions(),
  });
  const filesQuery = useQuery({
    queryKey: objectKeys.files(),
    queryFn: () => getFiles(),
  });

  const data = useMemo<ObjectsResponse | undefined>(() => {
    if (
      !objectsQuery.data ||
      !projectsQuery.data ||
      !sessionsQuery.data ||
      !filesQuery.data
    ) {
      return undefined;
    }

    return {
      objects: sortObjectSummaries(
        objectsQuery.data.map((object) =>
          buildObjectSummary(
            object,
            projectsQuery.data,
            sessionsQuery.data,
            filesQuery.data,
          ),
        ),
      ),
    };
  }, [
    filesQuery.data,
    objectsQuery.data,
    projectsQuery.data,
    sessionsQuery.data,
  ]);

  return {
    data,
    isError:
      objectsQuery.isError ||
      projectsQuery.isError ||
      sessionsQuery.isError ||
      filesQuery.isError,
    isLoading:
      objectsQuery.isLoading ||
      projectsQuery.isLoading ||
      sessionsQuery.isLoading ||
      filesQuery.isLoading,
  };
}

export function useObject(objectId: string | undefined) {
  const parsedObjectId = Number(objectId);
  const enabled = Boolean(objectId) && Number.isFinite(parsedObjectId);

  const objectQuery = useQuery({
    queryKey: objectKeys.detail(parsedObjectId),
    queryFn: () => getAstroObject(parsedObjectId),
    enabled,
  });
  const projectsQuery = useQuery({
    queryKey: objectKeys.projects(parsedObjectId),
    queryFn: () => getProjects(parsedObjectId),
    enabled,
  });

  const projectIds = useMemo(
    () =>
      projectsQuery.data?.map((project) => project.id).sort((a, b) => a - b),
    [projectsQuery.data],
  );

  const sessionsQuery = useQuery({
    queryKey: objectKeys.sessions(projectIds),
    queryFn: async () => {
      const sessionGroups = await Promise.all(
        projectIds?.map((projectId) => getSessions(projectId)) ?? [],
      );

      return sessionGroups.flat();
    },
    enabled: Boolean(projectIds),
  });
  const filesQuery = useQuery({
    queryKey: objectKeys.files(projectIds),
    queryFn: async () => {
      const fileGroups = await Promise.all(
        projectIds?.map((projectId) => getFiles(projectId)) ?? [],
      );

      return fileGroups.flat();
    },
    enabled: Boolean(projectIds),
  });

  const data = useMemo<ObjectDetail | undefined>(() => {
    if (
      !objectQuery.data ||
      !projectsQuery.data ||
      !sessionsQuery.data ||
      !filesQuery.data
    ) {
      return undefined;
    }

    return buildObjectSummary(
      objectQuery.data,
      projectsQuery.data,
      sessionsQuery.data,
      filesQuery.data,
    );
  }, [
    filesQuery.data,
    objectQuery.data,
    projectsQuery.data,
    sessionsQuery.data,
  ]);

  return {
    data,
    isError:
      objectQuery.isError ||
      projectsQuery.isError ||
      sessionsQuery.isError ||
      filesQuery.isError,
    isLoading:
      objectQuery.isLoading ||
      projectsQuery.isLoading ||
      sessionsQuery.isLoading ||
      filesQuery.isLoading,
  };
}
