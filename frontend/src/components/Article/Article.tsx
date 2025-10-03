import {
  Card,
  CardContent,
  Typography,
  IconButton,
  CardHeader,
  Tooltip,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { useState, type FC } from 'react';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { useConfirm } from 'material-ui-confirm';

import {
  useDeleteMenuNodeApiV1MenuMenuIdDeleteMutation,
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
  const [deleteMenuNode] = useDeleteMenuNodeApiV1MenuMenuIdDeleteMutation();
  const confirm = useConfirm();

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

  const handleDelete = async () => {
    const { confirmed } = await confirm({
      title: `Вы действительно хотите удалить статью "${data?.name}"?`,
      description:
        'Эта статья будет немедленно удалена. Это действие нельзя будет отменить',
      confirmationText: 'Удалить',
      cancellationText: 'Отменить',
    });

    if (confirmed) {
      await deleteMenuNode({ menuId: id });
    }
  };

  const deleteButtonTooltip =
    data?.parent_id === null ? 'Нельзя удалить главное меню' : 'Удалить статью';

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
            <>
              <Tooltip title="Редактировать статью">
                <IconButton
                  aria-label="редактировать"
                  onClick={openArticleEditor}
                >
                  <EditIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title={deleteButtonTooltip}>
                <span>
                  <IconButton
                    aria-label="удалить"
                    onClick={() => void handleDelete()}
                    disabled={data?.parent_id === null}
                  >
                    <DeleteOutlineIcon />
                  </IconButton>
                </span>
              </Tooltip>
            </>
          }
        />
        <CardContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Typography variant="subtitle1">{data?.text}</Typography>
        </CardContent>
      </Card>
    </>
  );
};
