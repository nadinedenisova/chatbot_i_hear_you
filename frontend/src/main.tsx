import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from 'react-router-dom';
import { Provider } from 'react-redux';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import { ROUTES } from '@shared/routes/ROUTES';
import store from '@store/store';
import QuestionsPage from '@pages/QuestionsPage/QuestionsPage';
import App from '@components/App/App';
import ErrorPage from '@pages/ErrorPage/ErrorPage';
import Login from '@pages/LoginPage/LoginPage';

import './index.css';

async function enableMocking() {
  // if (process.env.NODE_ENV !== "development") {
  //   return;
  // }

  const { worker } = await import('./mocks/browser');

  return worker.start({ onUnhandledRequest: 'bypass', quiet: false });
}

await enableMocking();

const theme = createTheme({
  palette: {
    background: {
      default: '#e6f2fa',
      paper: '#fff',
    },
  },
});

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
        element: <div>Меню</div>,
        handle: { title: 'Меню', id: 'menu' },
      },
      {
        path: ROUTES.QUESTIONS,
        element: <QuestionsPage />,
        handle: { title: 'Вопросы и ответы', id: 'questions' },
      },
    ],
  },
  {
    path: ROUTES.LOGIN,
    element: <Login />,
  },
]);

const rootElement = createRoot(document.getElementById('root')!);

rootElement.render(
  <StrictMode>
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </Provider>
  </StrictMode>,
);
