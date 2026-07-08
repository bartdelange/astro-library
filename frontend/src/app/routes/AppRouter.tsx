import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { AppShell } from '../layout/AppShell';
import { LibraryPage } from '../../pages/library/LibraryPage';

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<LibraryPage />} />
          <Route path="/objects" element={<LibraryPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
