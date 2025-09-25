import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import App from '@components/App/App';

import './index.css';

async function enableMocking() {
  // if (process.env.NODE_ENV !== "development") {
  //   return;
  // }

  const { worker } = await import('./mocks/browser');

  return worker.start({ onUnhandledRequest: 'bypass', quiet: false });
}

await enableMocking();

const rootElement = createRoot(document.getElementById('app')!);

rootElement.render(
  <StrictMode>
    <App />
  </StrictMode>,
);
