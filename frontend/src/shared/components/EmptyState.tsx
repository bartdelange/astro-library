import type { ReactNode } from 'react';
import { Card } from './Card';

type EmptyStateProps = {
  title: string;
  description?: string;
  action?: ReactNode;
};

export function EmptyState({ action, description, title }: EmptyStateProps) {
  return (
    <Card className="flex min-h-56 flex-col items-center justify-center px-6 py-10 text-center">
      <h2 className="text-base font-semibold text-slate-100">{title}</h2>
      {description ? (
        <p className="mt-2 max-w-md text-sm text-slate-400">{description}</p>
      ) : null}
      {action ? <div className="mt-5">{action}</div> : null}
    </Card>
  );
}
