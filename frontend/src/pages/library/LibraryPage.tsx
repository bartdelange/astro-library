import { useEffect, useState } from 'react';

export function LibraryPage() {
  const [health, setHealth] = useState<string>('loading');

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => setHealth(data.ok ? 'backend ok' : 'backend not ok'))
      .catch(() => setHealth('backend unreachable'));
  }, []);

  return (
    <div className="p-4">
      <h1 className="mb-4 text-2xl font-bold">Library Page</h1>
      <p>Welcome to the Library Page!</p>
      <p>API Health: {health}</p>
    </div>
  );
}
