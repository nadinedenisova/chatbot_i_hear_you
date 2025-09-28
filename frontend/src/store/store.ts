import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';

import { enhancedApi } from './enhancedApi';
import { rtkQueryErrorLogger } from './middleware.ts';

const store = configureStore({
  reducer: {
    [enhancedApi.reducerPath]: enhancedApi.reducer,
  },

  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(enhancedApi.middleware)
      .concat(rtkQueryErrorLogger),
});

setupListeners(store.dispatch);

export const dispatch = store.dispatch;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
