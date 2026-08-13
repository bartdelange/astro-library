import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { ObjectDetailView } from '../../features/objects/views/ObjectDetailView';
import { ObjectListView } from '../../features/objects/views/ObjectListView';
import { EmptyState } from '../../shared/components';
import { AppShell } from '../../shared/layouts/AppShell';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Navigate replace to="/objects" />} />
          <Route path="/library" element={<Navigate replace to="/objects" />} />
          <Route path="/objects" element={<ObjectListView />} />
          <Route path="/objects/:objectId" element={<ObjectDetailView />} />
          <Route
            path="/sessions"
            element={<PlaceholderRoute title="Sessions" />}
          />
          <Route
            path="/calendar"
            element={<PlaceholderRoute title="Calendar" />}
          />
          <Route path="/search" element={<PlaceholderRoute title="Search" />} />
          <Route
            path="/statistics"
            element={<PlaceholderRoute title="Statistics" />}
          />
          <Route
            path="/settings"
            element={<PlaceholderRoute title="Settings" />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

function PlaceholderRoute({ title }: { title: string }) {
  return (
    <EmptyState
      description="This section is ready to be connected as the feature structure expands."
      title={title}
    />
  );
}
