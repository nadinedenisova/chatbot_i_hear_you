import { http, HttpResponse } from 'msw';

//import database from './db';

export const handlers = [
  http.get(`${'BASE_URL'}/.......`, () => {
    return HttpResponse.json('response');
  }),
];
