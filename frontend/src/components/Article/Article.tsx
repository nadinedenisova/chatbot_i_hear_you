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
import AddIcon from '@mui/icons-material/Add';

import {
  useAddMenuNodeApiV1MenuAddPostMutation,
  useDeleteMenuNodeApiV1MenuMenuIdDeleteMutation,
  useGetMenuNodeApiV1MenuMenuIdGetQuery,
  useUpdateMenuNodeApiV1MenuMenuIdPutMutation,
} from '@store/api';
import { ArticleEditor } from '@components/ArticleEditor/ArticleEditor';
import AttachmentList from '@components/AttachmentList/AttachmentList';

export interface ArticleProps {
  id: string;
}

export const Article: FC<ArticleProps> = ({ id }) => {
  const { data } = useGetMenuNodeApiV1MenuMenuIdGetQuery({ menuId: id });

  // состояния
  const [isEditDialogOpen, setEditDialogOpen] = useState(false);
  const [isCreateDialogOpen, setCreateDialogOpen] = useState(false);

  // мутации
  const [updateMenuNode, { isLoading: isArticleUpdating }] =
    useUpdateMenuNodeApiV1MenuMenuIdPutMutation();
  const [deleteMenuNode] = useDeleteMenuNodeApiV1MenuMenuIdDeleteMutation();
  const [addMenuNode] = useAddMenuNodeApiV1MenuAddPostMutation();

  const confirm = useConfirm();

  // редактирование статьи
  const openEditDialog = () => setEditDialogOpen(true);
  const closeEditDialog = () => setEditDialogOpen(false);

  const handleEditArticle = async ({
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

    setEditDialogOpen(false);
  };

  // создание статьи
  const openCreateDialog = () => setCreateDialogOpen(true);
  const closeCreateDialog = () => setCreateDialogOpen(false);

  const handleCreateArticle = async ({
    title,
    description,
  }: {
    title: string;
    description: string;
  }) => {
    await addMenuNode({
      menuNodeCreate: {
        parent_id: id,
        name: title,
        text: description,
      },
    });
    setCreateDialogOpen(false);
  };

  // удаление статьи
  const handleDeleteArticle = async () => {
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
      {isEditDialogOpen && (
        <ArticleEditor
          initialTitle={data?.name ?? ''}
          initialDescription={data?.text ?? ''}
          open={isEditDialogOpen}
          onClose={closeEditDialog}
          onSave={handleEditArticle}
          disableSaveButton={isArticleUpdating}
          dialogTitle="Редактирование статьи"
        />
      )}
      {isCreateDialogOpen && (
        <ArticleEditor
          open={isCreateDialogOpen}
          onClose={closeCreateDialog}
          onSave={handleCreateArticle}
          dialogTitle="Добавление статьи"
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
              <Tooltip title="Добавить вложенную статью">
                <IconButton
                  aria-label="добавить вложенную статью"
                  onClick={openCreateDialog}
                >
                  <AddIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Редактировать статью">
                <IconButton aria-label="редактировать" onClick={openEditDialog}>
                  <EditIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title={deleteButtonTooltip}>
                <span>
                  <IconButton
                    aria-label="удалить"
                    onClick={() => void handleDeleteArticle()}
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
        <CardHeader
          title={
            <Typography variant="h6" fontWeight={'bold'}>
              Материалы
            </Typography>
          }
        />
        <AttachmentList />
      </Card>
    </>
  );
};
