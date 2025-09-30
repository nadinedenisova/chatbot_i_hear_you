import { useMatches, type UIMatch } from 'react-router-dom';

import type { AppRouteHandle } from 'src/main';

export function useCurrentRouteData() {
  const matches = useMatches() as UIMatch<AppRouteHandle>[];

  const current = matches[matches.length - 1];

  const handle = current?.handle as AppRouteHandle | undefined;

  const title = handle?.title ?? 'Админка';
  const selectedMenuItem = handle?.id ?? 'menu';

  return { title, selectedMenuItem, handle };
}
