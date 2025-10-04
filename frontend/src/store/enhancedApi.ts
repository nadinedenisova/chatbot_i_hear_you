import { injectedRtkApi } from './api';
import { TAGS_CONFIG } from './tagsConfig';

export const enhancedApi = injectedRtkApi.enhanceEndpoints({
  addTagTypes: [TAGS_CONFIG.QUESTIONS, TAGS_CONFIG.ARTICLES],
  endpoints: {
    getAllQuestionsApiV1UsersQuestionsGet: {
      providesTags: [TAGS_CONFIG.QUESTIONS],
    },
    answerQuestionApiV1UsersQuestionsQuestionIdAnswerPut: {
      invalidatesTags: [TAGS_CONFIG.QUESTIONS],
    },
    getFullMenuApiV1MenuGet: {
      providesTags: [TAGS_CONFIG.ARTICLES],
    },
    updateMenuNodeApiV1MenuMenuIdPut: {
      invalidatesTags: [TAGS_CONFIG.ARTICLES],
    },
    getMenuNodeApiV1MenuMenuIdGet: {
      providesTags: [TAGS_CONFIG.ARTICLES],
    },
    deleteQuestionApiV1UsersQuestionsQuestionIdDelete: {
      invalidatesTags: [TAGS_CONFIG.QUESTIONS],
    },
  },
});
