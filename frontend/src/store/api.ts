import { api } from './baseApi';
export const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    getFullMenuApiV1MenuGet: build.query<
      GetFullMenuApiV1MenuGetApiResponse,
      GetFullMenuApiV1MenuGetApiArg
    >({
      query: () => ({ url: `/api/v1/menu/` }),
    }),
    getMenuNodeByNameApiV1MenuSearchByNameGet: build.query<
      GetMenuNodeByNameApiV1MenuSearchByNameGetApiResponse,
      GetMenuNodeByNameApiV1MenuSearchByNameGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/search-by-name`,
        params: {
          name: queryArg.name,
        },
      }),
    }),
    getMenuRootApiV1MenuRootGet: build.query<
      GetMenuRootApiV1MenuRootGetApiResponse,
      GetMenuRootApiV1MenuRootGetApiArg
    >({
      query: () => ({ url: `/api/v1/menu/root` }),
    }),
    addMenuNodeApiV1MenuAddPost: build.mutation<
      AddMenuNodeApiV1MenuAddPostApiResponse,
      AddMenuNodeApiV1MenuAddPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/add`,
        method: 'POST',
        body: queryArg.menuNodeCreate,
      }),
    }),
    getMenuNodeApiV1MenuMenuIdGet: build.query<
      GetMenuNodeApiV1MenuMenuIdGetApiResponse,
      GetMenuNodeApiV1MenuMenuIdGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/menu/${queryArg.menuId}` }),
    }),
    updateMenuNodeApiV1MenuMenuIdPut: build.mutation<
      UpdateMenuNodeApiV1MenuMenuIdPutApiResponse,
      UpdateMenuNodeApiV1MenuMenuIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/${queryArg.menuId}`,
        method: 'PUT',
        body: queryArg.menuNodeUpdate,
      }),
    }),
    deleteMenuNodeApiV1MenuMenuIdDelete: build.mutation<
      DeleteMenuNodeApiV1MenuMenuIdDeleteApiResponse,
      DeleteMenuNodeApiV1MenuMenuIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/${queryArg.menuId}`,
        method: 'DELETE',
      }),
    }),
    addMenuContentApiV1MenuMenuIdContentAddPost: build.mutation<
      AddMenuContentApiV1MenuMenuIdContentAddPostApiResponse,
      AddMenuContentApiV1MenuMenuIdContentAddPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/${queryArg.menuId}/content/add`,
        method: 'POST',
        body: queryArg.contentCreate,
      }),
    }),
    updateMenuContentApiV1MenuMenuIdContentChangeContentIdPut: build.mutation<
      UpdateMenuContentApiV1MenuMenuIdContentChangeContentIdPutApiResponse,
      UpdateMenuContentApiV1MenuMenuIdContentChangeContentIdPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/${queryArg.menuId}/content/change/${queryArg.contentId}`,
        method: 'PUT',
        body: queryArg.contentCreate,
      }),
    }),
    deleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDelete:
      build.mutation<
        DeleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDeleteApiResponse,
        DeleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDeleteApiArg
      >({
        query: (queryArg) => ({
          url: `/api/v1/menu/${queryArg.menuId}/content/delete/${queryArg.contentId}`,
          method: 'DELETE',
        }),
      }),
    getMenuNodeRateApiV1MenuMenuIdRateGet: build.query<
      GetMenuNodeRateApiV1MenuMenuIdRateGetApiResponse,
      GetMenuNodeRateApiV1MenuMenuIdRateGetApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/menu/${queryArg.menuId}/rate` }),
    }),
    rateMenuNodeApiV1MenuMenuIdRatePost: build.mutation<
      RateMenuNodeApiV1MenuMenuIdRatePostApiResponse,
      RateMenuNodeApiV1MenuMenuIdRatePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/menu/${queryArg.menuId}/rate`,
        method: 'POST',
        body: queryArg.ratingCreate,
      }),
    }),
    getUsersApiV1UsersUsersGet: build.query<
      GetUsersApiV1UsersUsersGetApiResponse,
      GetUsersApiV1UsersUsersGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/users`,
        params: {
          page_size: queryArg.pageSize,
          page_number: queryArg.pageNumber,
        },
      }),
    }),
    createUserApiV1UsersCreatePost: build.mutation<
      CreateUserApiV1UsersCreatePostApiResponse,
      CreateUserApiV1UsersCreatePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/create`,
        method: 'POST',
        body: queryArg.userCreate,
      }),
    }),
    getLongTimeLostUsersApiV1UsersLongTimeLostGet: build.query<
      GetLongTimeLostUsersApiV1UsersLongTimeLostGetApiResponse,
      GetLongTimeLostUsersApiV1UsersLongTimeLostGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/long-time-lost`,
        params: {
          days_count: queryArg.daysCount,
          page_size: queryArg.pageSize,
          page_number: queryArg.pageNumber,
        },
      }),
    }),
    getUserQuestionsApiV1UsersQuestionsUserIdGet: build.query<
      GetUserQuestionsApiV1UsersQuestionsUserIdGetApiResponse,
      GetUserQuestionsApiV1UsersQuestionsUserIdGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/questions/${queryArg.userId}`,
      }),
    }),
    getAllQuestionsApiV1UsersQuestionsGet: build.query<
      GetAllQuestionsApiV1UsersQuestionsGetApiResponse,
      GetAllQuestionsApiV1UsersQuestionsGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/questions`,
        params: {
          page_size: queryArg.pageSize,
          page_number: queryArg.pageNumber,
        },
      }),
    }),
    createQuestionApiV1UsersQuestionsCreatePost: build.mutation<
      CreateQuestionApiV1UsersQuestionsCreatePostApiResponse,
      CreateQuestionApiV1UsersQuestionsCreatePostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/questions/create`,
        method: 'POST',
        body: queryArg.questionCreate,
      }),
    }),
    answerQuestionApiV1UsersQuestionsQuestionIdAnswerPut: build.mutation<
      AnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutApiResponse,
      AnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/questions/${queryArg.questionId}/answer`,
        method: 'PUT',
        body: queryArg.questionAnswer,
      }),
    }),
    deleteQuestionApiV1UsersQuestionsQuestionIdDelete: build.mutation<
      DeleteQuestionApiV1UsersQuestionsQuestionIdDeleteApiResponse,
      DeleteQuestionApiV1UsersQuestionsQuestionIdDeleteApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/questions/${queryArg.questionId}`,
        method: 'DELETE',
      }),
    }),
    createUserActionRecordApiV1UsersUserIdHistoryAddPost: build.mutation<
      CreateUserActionRecordApiV1UsersUserIdHistoryAddPostApiResponse,
      CreateUserActionRecordApiV1UsersUserIdHistoryAddPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/${queryArg.userId}/history/add`,
        method: 'POST',
        body: queryArg.historyCreate,
      }),
    }),
    getUserHistoryApiV1UsersUserIdHistoryGet: build.query<
      GetUserHistoryApiV1UsersUserIdHistoryGetApiResponse,
      GetUserHistoryApiV1UsersUserIdHistoryGetApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/users/${queryArg.userId}/history`,
        params: {
          page_size: queryArg.pageSize,
          page_number: queryArg.pageNumber,
        },
      }),
    }),
    addMenuContentWithUploadApiFilesMenuIdContentUploadPost: build.mutation<
      AddMenuContentWithUploadApiFilesMenuIdContentUploadPostApiResponse,
      AddMenuContentWithUploadApiFilesMenuIdContentUploadPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/files/${queryArg.menuId}/content/upload`,
        method: 'POST',
        body: queryArg.bodyAddMenuContentWithUploadApiFilesMenuIdContentUploadPost,
      }),
    }),
    updateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPut:
      build.mutation<
        UpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPutApiResponse,
        UpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPutApiArg
      >({
        query: (queryArg) => ({
          url: `/api/files/${queryArg.menuId}/content/upload/${queryArg.contentId}`,
          method: 'PUT',
          body: queryArg.bodyUpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPut,
        }),
      }),
    uploadTestFileApiFilesUploadTestPost: build.mutation<
      UploadTestFileApiFilesUploadTestPostApiResponse,
      UploadTestFileApiFilesUploadTestPostApiArg
    >({
      query: (queryArg) => ({
        url: `/api/files/upload-test`,
        method: 'POST',
        body: queryArg.bodyUploadTestFileApiFilesUploadTestPost,
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
export type GetFullMenuApiV1MenuGetApiResponse =
  /** status 200 Successful Response */ AllMenuNodeOut;
export type GetFullMenuApiV1MenuGetApiArg = void;
export type GetMenuNodeByNameApiV1MenuSearchByNameGetApiResponse =
  /** status 200 Successful Response */ MenuNodeOut;
export interface GetMenuNodeByNameApiV1MenuSearchByNameGetApiArg {
  name: string;
}
export type GetMenuRootApiV1MenuRootGetApiResponse =
  /** status 200 Successful Response */ MenuNodeOut;
export type GetMenuRootApiV1MenuRootGetApiArg = void;
export type AddMenuNodeApiV1MenuAddPostApiResponse =
  /** status 200 Successful Response */ Message;
export interface AddMenuNodeApiV1MenuAddPostApiArg {
  menuNodeCreate: MenuNodeCreate;
}
export type GetMenuNodeApiV1MenuMenuIdGetApiResponse =
  /** status 200 Successful Response */ MenuNodeOut;
export interface GetMenuNodeApiV1MenuMenuIdGetApiArg {
  menuId: string;
}
export type UpdateMenuNodeApiV1MenuMenuIdPutApiResponse =
  /** status 200 Successful Response */ Message;
export interface UpdateMenuNodeApiV1MenuMenuIdPutApiArg {
  menuId: string;
  menuNodeUpdate: MenuNodeUpdate;
}
export type DeleteMenuNodeApiV1MenuMenuIdDeleteApiResponse =
  /** status 200 Successful Response */ Message;
export interface DeleteMenuNodeApiV1MenuMenuIdDeleteApiArg {
  menuId: string;
}
export type AddMenuContentApiV1MenuMenuIdContentAddPostApiResponse =
  /** status 200 Successful Response */ Message;
export interface AddMenuContentApiV1MenuMenuIdContentAddPostApiArg {
  menuId: string;
  contentCreate: ContentCreate;
}
export type UpdateMenuContentApiV1MenuMenuIdContentChangeContentIdPutApiResponse =
  /** status 200 Successful Response */ Message;
export interface UpdateMenuContentApiV1MenuMenuIdContentChangeContentIdPutApiArg {
  menuId: string;
  contentId: string;
  contentCreate: ContentCreate;
}
export type DeleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDeleteApiResponse =
  /** status 200 Successful Response */ Message;
export interface DeleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDeleteApiArg {
  menuId: string;
  contentId: string;
}
export type GetMenuNodeRateApiV1MenuMenuIdRateGetApiResponse =
  /** status 200 Successful Response */ RatingOut;
export interface GetMenuNodeRateApiV1MenuMenuIdRateGetApiArg {
  menuId: string;
}
export type RateMenuNodeApiV1MenuMenuIdRatePostApiResponse =
  /** status 200 Successful Response */ Message;
export interface RateMenuNodeApiV1MenuMenuIdRatePostApiArg {
  menuId: string;
  ratingCreate: RatingCreate;
}
export type GetUsersApiV1UsersUsersGetApiResponse =
  /** status 200 Successful Response */ UsersListOut;
export interface GetUsersApiV1UsersUsersGetApiArg {
  /** Количество записей на странице */
  pageSize?: number;
  /** Номер страницы */
  pageNumber?: number;
}
export type CreateUserApiV1UsersCreatePostApiResponse =
  /** status 200 Successful Response */ Message;
export interface CreateUserApiV1UsersCreatePostApiArg {
  userCreate: UserCreate;
}
export type GetLongTimeLostUsersApiV1UsersLongTimeLostGetApiResponse =
  /** status 200 Successful Response */ UsersListOut;
export interface GetLongTimeLostUsersApiV1UsersLongTimeLostGetApiArg {
  daysCount?: number;
  /** Количество записей на странице */
  pageSize?: number;
  /** Номер страницы */
  pageNumber?: number;
}
export type GetUserQuestionsApiV1UsersQuestionsUserIdGetApiResponse =
  /** status 200 Successful Response */ QuestionsListOut;
export interface GetUserQuestionsApiV1UsersQuestionsUserIdGetApiArg {
  userId: string;
}
export type GetAllQuestionsApiV1UsersQuestionsGetApiResponse =
  /** status 200 Successful Response */ QuestionsListOut;
export interface GetAllQuestionsApiV1UsersQuestionsGetApiArg {
  /** Количество записей на странице */
  pageSize?: number;
  /** Номер страницы */
  pageNumber?: number;
}
export type CreateQuestionApiV1UsersQuestionsCreatePostApiResponse =
  /** status 200 Successful Response */ Message;
export interface CreateQuestionApiV1UsersQuestionsCreatePostApiArg {
  questionCreate: QuestionCreate;
}
export type AnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutApiResponse =
  /** status 200 Successful Response */ Message;
export interface AnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutApiArg {
  questionId: string;
  questionAnswer: QuestionAnswer;
}
export type DeleteQuestionApiV1UsersQuestionsQuestionIdDeleteApiResponse =
  /** status 200 Successful Response */ Message;
export interface DeleteQuestionApiV1UsersQuestionsQuestionIdDeleteApiArg {
  questionId: string;
}
export type CreateUserActionRecordApiV1UsersUserIdHistoryAddPostApiResponse =
  /** status 200 Successful Response */ Message;
export interface CreateUserActionRecordApiV1UsersUserIdHistoryAddPostApiArg {
  userId: string;
  historyCreate: HistoryCreate;
}
export type GetUserHistoryApiV1UsersUserIdHistoryGetApiResponse =
  /** status 200 Successful Response */ HistoryListOut;
export interface GetUserHistoryApiV1UsersUserIdHistoryGetApiArg {
  userId: string;
  /** Количество записей на странице */
  pageSize?: number;
  /** Номер страницы */
  pageNumber?: number;
}
export type AddMenuContentWithUploadApiFilesMenuIdContentUploadPostApiResponse =
  /** status 200 Successful Response */ Message;
export interface AddMenuContentWithUploadApiFilesMenuIdContentUploadPostApiArg {
  menuId: string;
  bodyAddMenuContentWithUploadApiFilesMenuIdContentUploadPost: BodyAddMenuContentWithUploadApiFilesMenuIdContentUploadPost;
}
export type UpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPutApiResponse =
  /** status 200 Successful Response */ Message;
export interface UpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPutApiArg {
  menuId: string;
  contentId: string;
  bodyUpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPut: BodyUpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPut;
}
export type UploadTestFileApiFilesUploadTestPostApiResponse =
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  /** status 200 Successful Response */ any;
export interface UploadTestFileApiFilesUploadTestPostApiArg {
  bodyUploadTestFileApiFilesUploadTestPost: BodyUploadTestFileApiFilesUploadTestPost;
}
export interface ContentOut {
  /** Уникальный идентификатор контента */
  id: string;
  /** Идентификатор меню, к которому относится контент */
  menu_id: string;
  /** Тип контента (числовой код) */
  type: number;
  /** Серверный путь до контента */
  server_path: string;
  /** Дата и время создания */
  created_at: string;
  /** Дата и время последнего обновления */
  updated_at: string;
}
export interface AllMenuNodeOut {
  /** Уникальный идентификатор узла меню */
  id: string;
  /** Идентификатор родительского узла (если есть) */
  parent_id?: string | null;
  /** Имя узла меню */
  name: string;
  /** Текстовое наполнение узла */
  text?: string | null;
  /** Тип подписки (если есть) */
  subscription_type?: string | null;
  /** Список контента, привязанного к узлу */
  content: ContentOut[];
  /** Имена дочерних узлов меню */
  children_names: string[];
  /** Дочерние узлы меню */
  children: AllMenuNodeOut[];
}
export interface MenuNodeOut {
  /** Уникальный идентификатор узла меню */
  id: string;
  /** Идентификатор родительского узла (если есть) */
  parent_id?: string | null;
  /** Имя узла меню */
  name: string;
  /** Текстовое наполнение узла */
  text?: string | null;
  /** Тип подписки (если есть) */
  subscription_type?: string | null;
  /** Список контента, привязанного к узлу */
  content: ContentOut[];
  /** Имена дочерних узлов меню */
  children_names: string[];
}
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}
export interface HttpValidationError {
  detail?: ValidationError[];
}
export interface Message {
  /** Сообщение об ошибке или информация */
  detail?: string;
}
export interface MenuNodeCreate {
  /** Идентификатор родительского узла (необязательный) */
  parent_id?: string | null;
  /** Имя нового узла */
  name: string;
  /** Текст узла (необязательный) */
  text?: string | null;
  /** Тип подписки (необязательный) */
  subscription_type?: string | null;
}
export interface MenuNodeUpdate {
  /** Идентификатор родительского узла (необязательный) */
  parent_id?: string | null;
  /** Имя нового узла */
  name: string;
  /** Текст узла (необязательный) */
  text?: string | null;
  /** Тип подписки (необязательный) */
  subscription_type?: string | null;
}
export interface ContentCreate {
  /** Идентификатор меню, к которому привязывается контент */
  menu_id: string;
  /** Тип контента (числовой код) */
  type: number;
  /** Серверный путь для загружаемого контента */
  server_path: string;
}
export interface RatingOut {
  /** Идентификатор пользователя */
  user_id: string;
  /** Оценка (например, от 1 до 5) */
  node_rating: number;
  /** Идентификатор меню/узла, к которому привязана оценка */
  menu_id: string;
  /** Дата и время создания оценки */
  created_at: string;
  /** Дата и время обновления оценки */
  updated_at: string;
}
export interface RatingCreate {
  /** Идентификатор пользователя */
  user_id: string;
  /** Оценка (например, от 1 до 5) */
  node_rating: number;
}
export interface UserOut {
  /** Уникальный идентификатор пользователя */
  id: string;
  /** Номер телефона пользователя */
  phone_number: string;
  /** Дата и время создания пользователя */
  created_at: string;
  /** Дата и время последнего обновления пользователя */
  updated_at: string;
}
export interface UsersListOut {
  /** Список пользователей */
  items: UserOut[];
}
export interface UserCreate {
  /** Уникальный идентификатор пользователя */
  id: string;
  /** Номер телефона пользователя */
  phone_number: string;
}
export interface QuestionOut {
  /** Уникальный идентификатор вопроса */
  id: string;
  /** Идентификатор пользователя, задавшего вопрос */
  user_id: string;
  /** Текст вопроса */
  text: string;
  /** Ответ администратора (может отсутствовать) */
  admin_answer?: string | null;
  /** Дата и время создания */
  created_at: string;
  /** Дата и время последнего обновления */
  updated_at: string;
}
export interface QuestionsListOut {
  /** Список вопросов */
  items: QuestionOut[];
}
export interface QuestionCreate {
  /** Идентификатор пользователя, задающего вопрос */
  user_id: string;
  /** Текст вопроса */
  text: string;
}
export interface QuestionAnswer {
  /** Текст вопроса */
  admin_answer: string;
}
export interface HistoryCreate {
  /** Идентификатор меню (необязательный) */
  menu_id?: string | null;
  /** Дата и время действия */
  action_date: string;
}
export interface HistoryOut {
  /** Идентификатор меню (необязательный) */
  menu_id?: string | null;
  /** Дата и время действия */
  action_date: string;
  /** Идентификатор пользователя */
  user_id: string;
  /** Идентификатор действия */
  action_id: string;
  /** Дата и время создания записи истории */
  created_at: string;
}
export interface HistoryListOut {
  /** Список действий */
  items: HistoryOut[];
}
export interface BodyAddMenuContentWithUploadApiFilesMenuIdContentUploadPost {
  /** Тип контента (1-изображение, 2-видео, 3-документ) */
  file_type: number;
  /** Файл для загрузки */
  file: Blob;
}
export interface BodyUpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPut {
  /** Тип контента (1-изображение, 2-видео, 3-документ) */
  file_type: number;
  /** Новый файл для загрузки */
  file: Blob;
}
export interface BodyUploadTestFileApiFilesUploadTestPost {
  file: Blob;
}
export const {
  useGetFullMenuApiV1MenuGetQuery,
  useGetMenuNodeByNameApiV1MenuSearchByNameGetQuery,
  useGetMenuRootApiV1MenuRootGetQuery,
  useAddMenuNodeApiV1MenuAddPostMutation,
  useGetMenuNodeApiV1MenuMenuIdGetQuery,
  useUpdateMenuNodeApiV1MenuMenuIdPutMutation,
  useDeleteMenuNodeApiV1MenuMenuIdDeleteMutation,
  useAddMenuContentApiV1MenuMenuIdContentAddPostMutation,
  useUpdateMenuContentApiV1MenuMenuIdContentChangeContentIdPutMutation,
  useDeleteMenuContentApiV1MenuMenuIdContentDeleteContentIdDeleteMutation,
  useGetMenuNodeRateApiV1MenuMenuIdRateGetQuery,
  useRateMenuNodeApiV1MenuMenuIdRatePostMutation,
  useGetUsersApiV1UsersUsersGetQuery,
  useCreateUserApiV1UsersCreatePostMutation,
  useGetLongTimeLostUsersApiV1UsersLongTimeLostGetQuery,
  useGetUserQuestionsApiV1UsersQuestionsUserIdGetQuery,
  useGetAllQuestionsApiV1UsersQuestionsGetQuery,
  useCreateQuestionApiV1UsersQuestionsCreatePostMutation,
  useAnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutMutation,
  useDeleteQuestionApiV1UsersQuestionsQuestionIdDeleteMutation,
  useCreateUserActionRecordApiV1UsersUserIdHistoryAddPostMutation,
  useGetUserHistoryApiV1UsersUserIdHistoryGetQuery,
  useAddMenuContentWithUploadApiFilesMenuIdContentUploadPostMutation,
  useUpdateMenuContentWithUploadApiFilesMenuIdContentUploadContentIdPutMutation,
  useUploadTestFileApiFilesUploadTestPostMutation,
} = injectedRtkApi;
