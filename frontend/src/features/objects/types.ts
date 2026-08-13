import type {
  AstroObjectRead,
  FileRead,
  ProjectRead,
  SessionRead,
} from '../../shared/api/generated';

export type BackendAstroObject = AstroObjectRead;
export type BackendProject = ProjectRead;
export type BackendSession = SessionRead;
export type BackendFile = FileRead;

export type ObjectSummary = {
  object: BackendAstroObject;
  projects: BackendProject[];
  sessions: BackendSession[];
  files: BackendFile[];
  heroFile: BackendFile | null;
  sessionCount: number;
  totalIntegrationSeconds: number;
  latestSessionDate: string | null;
};

export type ObjectDetail = ObjectSummary;

export type ObjectsResponse = {
  objects: ObjectSummary[];
};
