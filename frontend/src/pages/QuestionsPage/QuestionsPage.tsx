import Pagination from '@mui/material/Pagination';
import Box from '@mui/material/Box';
import { useState } from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';

import QuestionCard from '@components/QuestionCard/QuestionCard';
import { useGetAllQuestionsApiV1UsersQuestionsGetQuery } from '@store/api';

export default function QuestionsPage() {
  const [pageNumber, setPageNumber] = useState(1);
  const pageSize = 10;

  const {
    data: questionsData,
    refetch,
    isLoading,
    isError,
  } = useGetAllQuestionsApiV1UsersQuestionsGetQuery({
    pageNumber,
    pageSize,
  });
  const hasNextPage = questionsData?.items?.length === pageSize;
  const totalPages = pageNumber + (hasNextPage ? 1 : 0);

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100%"
      >
        <CircularProgress />
      </Box>
    );
  }
  if (isError) {
    return (
      <Alert severity="error">
        Не удалось загрузить меню, попробуйте обновить страницу
      </Alert>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        pb: 1,
      }}
    >
      {questionsData?.items?.map((question) => (
        <QuestionCard
          key={question.id}
          question_id={question.id}
          user_id={question.user_id}
          date={question.created_at}
          content={question.text}
          adminAnswer={question.admin_answer}
          refetch={refetch}
        />
      ))}
      <Pagination
        page={pageNumber}
        count={totalPages}
        onChange={(_, value) => setPageNumber(value)}
      />
    </Box>
  );
}
