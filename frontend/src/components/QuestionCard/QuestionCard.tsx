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
  phone: string;
  date: string;
  content: string;
  isAnswered?: string;
}

export default function QuestionCard({
  phone,
  date,
  content,
  isAnswered,
}: QuestionCardProps) {
  const [expanded, setExpanded] = React.useState(!isAnswered);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

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
            <Typography variant="subtitle2">{phone}</Typography>
            <Divider orientation="vertical" flexItem />
            <Typography variant="subtitle2">{date}</Typography>
          </Box>
        }
        action={
          <IconButton aria-label="Удалить вопрос">
            <DeleteTwoToneIcon />
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
        <CardContent sx={{ pt: 0 }}>
          <Typography variant="subtitle2">Ответ:</Typography>
          <TextField fullWidth multiline />
          <Button size="small" variant="contained" sx={{ mt: 2 }}>
            Отправить
          </Button>
        </CardContent>
      </Collapse>
    </Card>
  );
}
