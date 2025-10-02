import Pagination from '@mui/material/Pagination';
import Box from '@mui/material/Box';

import QuestionCard from '@components/QuestionCard/QuestionCard';

export default function QuestionsPage() {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        pb: 1,
      }}
    >
      <QuestionCard
        phone={'88002352525'}
        date={'24.01.1005'}
        content={
          'Есть ли что-то, что мне нужно знать о тебе, но ты боишься это рассказать?'
        }
        isAnswered={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isAnswered={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isAnswered={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isAnswered={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isAnswered={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isAnswered={'true'}
      />
      <Pagination count={10} />
    </Box>
  );
}
