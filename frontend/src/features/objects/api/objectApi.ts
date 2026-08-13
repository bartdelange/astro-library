import type {
  BackendAstroObject,
  BackendFile,
  BackendProject,
  BackendSession,
} from '../types';
import {
  readAstroObjectApiObjectsObjectIdGet,
  readAstroObjectsApiObjectsGet,
  readFilesApiFilesGet,
  readProjectsApiProjectsGet,
  readSessionsApiSessionsGet,
} from '../../../shared/api/generated';

export async function getAstroObjects(): Promise<BackendAstroObject[]> {
  return readAstroObjectsApiObjectsGet({
    throwOnError: true,
  });
}

export async function getAstroObject(
  objectId: number,
): Promise<BackendAstroObject> {
  return readAstroObjectApiObjectsObjectIdGet({
    path: { object_id: objectId },
    throwOnError: true,
  });
}

export async function getProjects(
  objectId?: number,
): Promise<BackendProject[]> {
  return readProjectsApiProjectsGet({
    query: { object_id: objectId },
    throwOnError: true,
  });
}

export async function getSessions(
  projectId?: number,
): Promise<BackendSession[]> {
  return readSessionsApiSessionsGet({
    query: { project_id: projectId },
    throwOnError: true,
  });
}

export async function getFiles(projectId?: number): Promise<BackendFile[]> {
  return readFilesApiFilesGet({
    query: { project_id: projectId },
    throwOnError: true,
  });
}
