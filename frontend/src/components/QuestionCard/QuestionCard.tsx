import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import CheckOutlinedIcon from '@mui/icons-material/CheckOutlined';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DeleteTwoToneIcon from '@mui/icons-material/DeleteTwoTone';
import { Box, Button, Divider, TextField } from '@mui/material';
import dayjs from 'dayjs';
import { skipToken } from '@reduxjs/toolkit/query/react';

import {
  useGetUsersApiV1UsersUsersGetQuery,
  useAnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutMutation,
  useDeleteQuestionApiV1UsersQuestionsQuestionIdDeleteMutation,
} from '@store/api';

import type { IconButtonProps } from '@mui/material/IconButton';

interface ExpandMoreProps extends IconButtonProps {
  expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme }) => ({
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
  ...(props: ExpandMoreProps) => ({
    transform: props.expand ? 'rotate(180deg)' : 'rotate(0deg)',
  }),
}));

interface QuestionCardProps {
  content: string;
  isAnswered?: string | null;
  date: string;
  user_id: string;
  question_id: string;
  refetch: () => Promise<unknown>;
}

export default function QuestionCard({
  content,
  isAnswered,
  date,
  user_id,
  question_id,
  refetch,
}: QuestionCardProps) {
  const [expanded, setExpanded] = React.useState(false);
  const [answerText, setAnswerText] = React.useState('');

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const [answerQuestion] =
    useAnswerQuestionApiV1UsersQuestionsQuestionIdAnswerPutMutation();

  const handleSendAnswer = async () => {
    console.log(question_id);
    console.log(answerText);
    await answerQuestion({
      questionId: question_id,
      questionAnswer: { admin_answer: answerText },
    }).unwrap();
    setAnswerText('');
  };

  const [deleteQuestion] =
    useDeleteQuestionApiV1UsersQuestionsQuestionIdDeleteMutation();

  const handleDeleteQuestion = async () => {
    try {
      console.log(question_id);
      await deleteQuestion({ questionId: question_id }).unwrap();
      await refetch();
    } catch (err) {
      console.error('Ошибка при удалении вопроса:', err);
    }
  };

  const { data: usersData } = useGetUsersApiV1UsersUsersGetQuery(
    user_id ? { id: user_id } : skipToken,
  );
  const user = usersData?.items?.find((u) => u.id === user_id);
  const phoneNumber = user?.phone_number;
  const formattedDate = dayjs(date.split('.')[0]).format('DD.MM.YYYY');

  React.useEffect(() => {
    if (typeof isAnswered === 'string') {
      setExpanded(false);
    }
  }, [isAnswered]);

  return (
    <Card sx={{ minWidth: 900 }}>
      <CardHeader
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          pb: 0,
        }}
        title={
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Typography variant="subtitle2">{phoneNumber}</Typography>
            <Divider orientation="vertical" flexItem />
            <Typography variant="subtitle2">{formattedDate}</Typography>
          </Box>
        }
        action={
          <IconButton aria-label="Удалить вопрос">
            <DeleteTwoToneIcon onClick={() => void handleDeleteQuestion()} />
          </IconButton>
        }
      />
      <CardContent sx={{ pt: 0, pb: 0 }}>
        <Divider />
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mt: 1,
          }}
        >
          <Box>
            <Typography variant="body2" sx={{ mt: 1 }}>
              {content}
            </Typography>
          </Box>
          <CheckOutlinedIcon
            sx={{
              color: isAnswered ? 'green' : 'red',
              cursor: 'default',
              pointerEvents: 'none',
              fontSize: 25,
            }}
          />
        </Box>
      </CardContent>

      <CardActions disableSpacing sx={{ pt: 0 }}>
        <ExpandMore
          aria-controls="question-content"
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="Показать ответ"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>

      <Collapse in={expanded} timeout="auto" unmountOnExit>
        {typeof isAnswered === 'string' ? (
          <CardContent sx={{ pt: 0 }}>
            <Typography variant="subtitle2">Ответ: {isAnswered}</Typography>
          </CardContent>
        ) : (
          <CardContent sx={{ pt: 0 }}>
            <Typography variant="subtitle2">Ответ:</Typography>
            <TextField
              fullWidth
              multiline
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
            />
            <Button
              size="small"
              variant="contained"
              sx={{ mt: 2 }}
              onClick={() => void handleSendAnswer()}
            >
              Отправить
            </Button>
          </CardContent>
        )}
      </Collapse>
    </Card>
  );
}
