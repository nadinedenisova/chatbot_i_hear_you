import Button from '@mui/material/Button';
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useEffect, useMemo, useState, type SyntheticEvent } from 'react';
import { styled, alpha } from '@mui/material/styles';
import { TreeItem, treeItemClasses } from '@mui/x-tree-view/TreeItem';
import { useTreeViewApiRef } from '@mui/x-tree-view/hooks';
import { Grid } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';

import {
  useGetFullMenuApiV1MenuGetQuery,
  type AllMenuNodeOut,
} from '@store/api';
import { Article } from '@components/Article/Article';

import type { TreeViewItemId } from '@mui/x-tree-view';

const getItemLabel = (item: AllMenuNodeOut) => item.name;

const getAllItemsWithChildrenItemIds = (menu: AllMenuNodeOut[]) => {
  const itemIds: TreeViewItemId[] = [];
  const registerItemId = (item: AllMenuNodeOut) => {
    if (item.children?.length) {
      itemIds.push(item.id);
      item.children.forEach(registerItemId);
    }
  };

  menu.forEach(registerItemId);

  return itemIds;
};

const CustomTreeItem = styled(TreeItem)(({ theme }) => ({
  color: theme.palette.grey[200],
  [`& .${treeItemClasses.content}`]: {
    borderRadius: theme.spacing(0.5),
    padding: theme.spacing(0.5, 1),
    margin: theme.spacing(0.2, 0),
    [`& .${treeItemClasses.label}`]: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  [`& .${treeItemClasses.iconContainer}`]: {
    borderRadius: '50%',
    backgroundColor: theme.palette.primary.dark,
    padding: theme.spacing(0, 1.2),
    ...theme.applyStyles('light', {
      backgroundColor: alpha(theme.palette.primary.main, 0.25),
    }),
    ...theme.applyStyles('dark', {
      color: theme.palette.primary.contrastText,
    }),
  },
  [`& .${treeItemClasses.groupTransition}`]: {
    marginLeft: 15,
    paddingLeft: 18,
    borderLeft: `1px dashed ${alpha(theme.palette.text.primary, 0.4)}`,
  },
  ...theme.applyStyles('light', {
    color: theme.palette.grey[800],
  }),
}));

export const MenuPage = () => {
  const apiRef = useTreeViewApiRef();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null);

  const {
    data: menuData,
    isLoading,
    isError,
  } = useGetFullMenuApiV1MenuGetQuery();

  const menu = useMemo(() => {
    return menuData ? [menuData] : [];
  }, [menuData]);

  useEffect(() => {
    if (!selectedItemId) return;

    const item = apiRef?.current?.getItem(
      selectedItemId,
    ) as AllMenuNodeOut | null;

    if (item) return;

    setSelectedItemId(null);
  }, [apiRef, menuData, selectedItemId]);

  const handleSelectedItemsChange = (
    _: SyntheticEvent | null,
    itemId: string | null,
  ) => {
    setSelectedItemId(itemId);
  };

  const handleExpandedItemsChange = (
    _: SyntheticEvent | null,
    itemIds: string[],
  ) => {
    setExpandedItems(itemIds);
  };

  const handleExpandClick = () => {
    setExpandedItems((oldExpanded) =>
      oldExpanded.length === 0 ? getAllItemsWithChildrenItemIds(menu) : [],
    );
  };

  if (isLoading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        height="100%"
      >
        <CircularProgress />
      </Box>
    );
  }
  if (isError) {
    return (
      <Alert severity="error">
        Не удалось загрузить меню, попробуйте обновить страницу
      </Alert>
    );
  }

  return (
    <>
      <Grid container spacing={2}>
        <Grid
          size={5}
          sx={{
            maxHeight: '100vh',
            overflowY: 'auto',
            pr: 2,
          }}
        >
          <Button onClick={handleExpandClick}>
            {expandedItems.length === 0 ? 'Развернуть всё' : 'Свернуть всё'}
          </Button>
          <RichTreeView
            items={menu}
            expandedItems={expandedItems}
            onExpandedItemsChange={handleExpandedItemsChange}
            getItemLabel={getItemLabel}
            defaultExpandedItems={['grid']}
            slots={{ item: CustomTreeItem }}
            apiRef={apiRef}
            selectedItems={selectedItemId}
            onSelectedItemsChange={handleSelectedItemsChange}
          />
        </Grid>
        <Grid
          size={7}
          sx={{
            position: 'sticky',
            top: 0,
            alignSelf: 'flex-start',
            height: '100vh',
            overflowY: 'auto',
          }}
        >
          {selectedItemId && <Article id={selectedItemId} />}
        </Grid>
      </Grid>
    </>
  );
};
