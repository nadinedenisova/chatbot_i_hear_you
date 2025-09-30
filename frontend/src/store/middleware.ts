import { isRejectedWithValue } from '@reduxjs/toolkit';

import type { Middleware } from '@reduxjs/toolkit';
// import { toast } from 'react-toastify';

export const rtkQueryErrorLogger: Middleware = () => (next) => (action) => {
  if (isRejectedWithValue(action)) {
    console.warn('We got a rejected action!');
    // TODO: add display message to user
    // toast.error((action.payload as { data: { detail: string } }).data.detail);
  }

  return next(action);
};
