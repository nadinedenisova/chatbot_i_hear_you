import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  styled,
} from '@mui/material';
import { Link } from 'react-router-dom';

import { useCurrentRouteData } from '@hooks/useCurrentRouteData';

import styles from './MenuItem.module.css';

import type { JSX } from '@emotion/react/jsx-runtime';
import type { FC } from 'react';

const StyledListItemButton = styled(ListItemButton)(() => ({
  '&.Mui-selected': {
    backgroundColor: '#d7ebff',
    color: '#1976d2',
    borderRadius: '5px',
  },
}));

interface MenuItemProps {
  title: string;
  icon: JSX.Element;
  path: string;
  selected?: boolean;
  id: string;
}

export const MenuItem: FC<MenuItemProps> = ({
  title,
  icon,
  path,
  selected,
  id,
}) => {
  const { selectedMenuItem } = useCurrentRouteData();

  return (
    <ListItem className={styles.item} disablePadding component={Link} to={path}>
      <StyledListItemButton selected={selectedMenuItem === id}>
        <ListItemIcon sx={{ color: selected ? '#1976d2' : 'inherit' }}>
          {icon}
        </ListItemIcon>
        <ListItemText primary={title} />
      </StyledListItemButton>
    </ListItem>
  );
};
