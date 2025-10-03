import Pagination from '@mui/material/Pagination';
import Box from '@mui/material/Box';
import { useState } from 'react';

import QuestionCard from '@components/QuestionCard/QuestionCard';
import { useGetAllQuestionsApiV1UsersQuestionsGetQuery } from '@store/api';

export default function QuestionsPage() {
  const [pageNumber, setPageNumber] = useState(1);
  const pageSize = 10;

  const { data: questionsData, refetch } =
    useGetAllQuestionsApiV1UsersQuestionsGetQuery({
      pageNumber,
      pageSize,
    });
  const hasNextPage = questionsData?.items?.length === pageSize;
  const totalPages = pageNumber + (hasNextPage ? 1 : 0);
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
          isAnswered={question.admin_answer}
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
