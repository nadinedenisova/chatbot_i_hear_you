import Pagination from '@mui/material/Pagination';

import { drawerWidth } from '@components/AppHeader/AppHeader';
import QuestionCard from '@components/QuestionCard/QuestionCard';

export default function QuestionsPage() {
  return (
    <div
      style={{
        display: 'flex',
        position: 'absolute',
        top: '83px',
        left: `calc(${drawerWidth}px + 20px)`,
        flexDirection: 'column',
        gap: '20px',
        paddingBottom: '10px',
      }}
    >
      <QuestionCard
        phone={'88002352525'}
        date={'24.01.1005'}
        content={
          'Есть ли что-то, что мне нужно знать о тебе, но ты боишься это рассказать?'
        }
        isChecked={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <Pagination count={10} />
    </div>
  );
}
