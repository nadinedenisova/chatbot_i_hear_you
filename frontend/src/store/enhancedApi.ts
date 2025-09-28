import { injectedRtkApi } from './api';
import { TAGS_CONFIG } from './tagsConfig';

export const enhancedApi = injectedRtkApi.enhanceEndpoints({
  addTagTypes: [TAGS_CONFIG.QUESTIONS],
  endpoints: {
    getAllQuestionsApiV1UsersQuestionsGet: {
      providesTags: [TAGS_CONFIG.QUESTIONS],
    },
    answerQuestionApiV1UsersQuestionsQuestionIdAnswerPut: {
      invalidatesTags: [TAGS_CONFIG.QUESTIONS],
    },
  },
});
