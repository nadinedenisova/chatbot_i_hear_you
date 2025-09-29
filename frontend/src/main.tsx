import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from 'react-router-dom';
import { Provider } from 'react-redux';

import { ROUTES } from '@shared/routes/ROUTES';
import store from '@store/store';
import App from '@components/App/App';
import { Main } from '@components/Main/Main';
import ErrorPage from '@pages/ErrorPage/ErrorPage';

import './index.css';

async function enableMocking() {
  // if (process.env.NODE_ENV !== "development") {
  //   return;
  // }

  const { worker } = await import('./mocks/browser');

  return worker.start({ onUnhandledRequest: 'bypass', quiet: false });
}

await enableMocking();

export interface AppRouteHandle {
  title?: string;
  id?: string;
}

const router = createBrowserRouter([
  {
    path: ROUTES.ROOT,
    element: <App />,
    children: [
      {
        index: true,
        element: <Navigate to={ROUTES.MENU} />,
        errorElement: <ErrorPage />,
      },
      {
        path: ROUTES.MENU,
        element: <Main />,
        handle: { title: 'Меню', id: 'menu' },
      },
      {
        path: ROUTES.QUESTIONS,
        element: <div>Вопросы и ответы</div>,
        handle: { title: 'Вопросы и ответы', id: 'questions' },
      },
    ],
  },
  // {
  //   path: ROUTES.LOGIN,
  //    element: </>,
  // },
]);

const rootElement = createRoot(document.getElementById('root')!);

rootElement.render(
  <StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </StrictMode>,
);
