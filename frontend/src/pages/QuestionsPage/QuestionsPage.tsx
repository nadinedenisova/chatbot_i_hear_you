import QuestionCard from '@components/QuestionCard/QuestionCard';

export default function QuestionsPage() {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '20px',
        paddingTop: '985px',
      }}
    >
      <QuestionCard
        name={'Александр'}
        phone={'88002352525'}
        date={'24.01.1005'}
        content={
          'Есть ли что-то, что мне нужно знать о тебе, но ты боишься это рассказать?'
        }
        isChecked={'true'}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={''}
      />
      <QuestionCard
        name={'Шурик'}
        phone={'+79992352525'}
        date={'24.01.2025'}
        content={'Есть ли что-то, что тебя сейчас беспокоит?'}
        isChecked={'true'}
      />
    </div>
  );
}
