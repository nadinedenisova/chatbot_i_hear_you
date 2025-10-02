import { useState, type FC } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  Stack,
} from '@mui/material';

interface ArticleEditorProps {
  open: boolean;
  initialTitle?: string;
  initialDescription?: string;
  disableSaveButton?: boolean;
  onSave: (data: { title: string; description: string }) => Promise<void>;
  onClose: () => void;
}

export const ArticleEditor: FC<ArticleEditorProps> = ({
  open,
  initialTitle = '',
  initialDescription = '',
  disableSaveButton,
  onSave,
  onClose,
}) => {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    void onSave({ title, description });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Редактирование статьи</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <Stack spacing={2} mt={1}>
            <TextField
              label="Заголовок"
              fullWidth
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <TextField
              label="Описание"
              fullWidth
              multiline
              rows={8}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Отменить</Button>
          <Button type="submit" disabled={disableSaveButton}>
            Сохранить
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};
