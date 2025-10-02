import {
  Card,
  CardContent,
  Typography,
  IconButton,
  CardHeader,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { useState, type FC } from 'react';

import {
  useGetMenuNodeApiV1MenuMenuIdGetQuery,
  useUpdateMenuNodeApiV1MenuMenuIdPutMutation,
} from '@store/api';
import { ArticleEditor } from '@components/ArticleEditor/ArticleEditor';

export interface ArticleProps {
  id: string;
}

export const Article: FC<ArticleProps> = ({ id }) => {
  const { data } = useGetMenuNodeApiV1MenuMenuIdGetQuery({ menuId: id });
  const [isEditorOpen, setEditorOpen] = useState(false);
  const [updateMenuNode, { isLoading: isArticleUpdating }] =
    useUpdateMenuNodeApiV1MenuMenuIdPutMutation();

  const openArticleEditor = () => setEditorOpen(true);

  const closeArticleEditor = () => setEditorOpen(false);

  const handleSave = async ({
    title,
    description,
  }: {
    title: string;
    description: string;
  }) => {
    await updateMenuNode({
      menuId: id,
      menuNodeUpdate: {
        name: title,
        text: description,
      },
    });

    setEditorOpen(false);
  };

  return (
    <>
      {isEditorOpen && (
        <ArticleEditor
          initialTitle={data?.name ?? ''}
          initialDescription={data?.text ?? ''}
          open={isEditorOpen}
          onClose={closeArticleEditor}
          onSave={handleSave}
          disableSaveButton={isArticleUpdating}
        />
      )}
      <Card variant="outlined" component="article">
        <CardHeader
          title={
            <Typography variant="h5" fontWeight={'bold'}>
              {data?.name}
            </Typography>
          }
          action={
            <IconButton
              aria-label="редактировать статью"
              onClick={openArticleEditor}
            >
              <EditIcon />
            </IconButton>
          }
        />
        <CardContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="subtitle1">{data?.text}</Typography>
        </CardContent>
      </Card>
    </>
  );
};
