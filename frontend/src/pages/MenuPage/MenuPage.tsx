import Button from '@mui/material/Button';
import { RichTreeView } from '@mui/x-tree-view/RichTreeView';
import { useState, type SyntheticEvent } from 'react';
import { styled, alpha } from '@mui/material/styles';
import { TreeItem, treeItemClasses } from '@mui/x-tree-view/TreeItem';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { useTreeViewApiRef } from '@mui/x-tree-view/hooks';
import { Grid } from '@mui/material';

import {
  MOCK_MENU_TREE,
  type TreeViewBaseItem,
} from '../../mocks/generateTree';

import type { TreeViewItemId } from '@mui/x-tree-view';

const getItemLabel = (item: TreeViewBaseItem) => item.name;

const getAllItemsWithChildrenItemIds = () => {
  const itemIds: TreeViewItemId[] = [];
  const registerItemId = (item: TreeViewBaseItem) => {
    if (item.children?.length) {
      itemIds.push(item.id);
      item.children.forEach(registerItemId);
    }
  };

  MOCK_MENU_TREE.forEach(registerItemId);

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
  const [selectedItem, setSelectedItem] = useState<TreeViewBaseItem | null>(
    null,
  );

  const handleSelectedItemsChange = (
    _: SyntheticEvent | null,
    itemId: string | null,
  ) => {
    if (itemId == null) {
      setSelectedItem(null);
    } else {
      setSelectedItem(apiRef.current!.getItem(itemId) as TreeViewBaseItem);
    }
  };

  const handleExpandedItemsChange = (
    _: SyntheticEvent | null,
    itemIds: string[],
  ) => {
    setExpandedItems(itemIds);
  };

  const handleExpandClick = () => {
    setExpandedItems((oldExpanded) =>
      oldExpanded.length === 0 ? getAllItemsWithChildrenItemIds() : [],
    );
  };

  return (
    <Grid container spacing={2}>
      <Grid size={3}>
        <Button onClick={handleExpandClick}>
          {expandedItems.length === 0 ? 'Развернуть всё' : 'Свернуть всё'}
        </Button>
        <RichTreeView
          items={MOCK_MENU_TREE}
          expandedItems={expandedItems}
          onExpandedItemsChange={handleExpandedItemsChange}
          getItemLabel={getItemLabel}
          defaultExpandedItems={['grid']}
          slots={{ item: CustomTreeItem }}
          apiRef={apiRef}
          selectedItems={selectedItem?.id ?? null}
          onSelectedItemsChange={handleSelectedItemsChange}
        />
      </Grid>
      <Grid size={9}>
        {selectedItem && (
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h5" component="div">
                {selectedItem?.name}
              </Typography>
              <Typography variant="body2">{selectedItem?.text}</Typography>
            </CardContent>
          </Card>
        )}
      </Grid>
    </Grid>
  );
};
