import { styled } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';

import { drawerWidth } from '@components/AppHeader/AppHeader';
import { MenuItem } from '@components/MenuItem/MenuItem';
import { ROUTES } from '@shared/routes/ROUTES';

import type { FC } from 'react';

const menuItems = [
  {
    title: 'Меню',
    icon: <MenuBookIcon />,
    path: ROUTES.MENU,
    id: 'menu',
  },
  {
    title: 'Вопросы',
    icon: <QuestionAnswerIcon />,
    path: ROUTES.QUESTIONS,
    id: 'questions',
  },
];

export const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

interface SidebarProps {
  open: boolean;
  onClick: () => void;
}

export const Sidebar: FC<SidebarProps> = ({ open, onClick }) => (
  <Drawer
    sx={{
      width: drawerWidth,
      flexShrink: 0,
      '& .MuiDrawer-paper': {
        width: drawerWidth,
        boxSizing: 'border-box',
      },
    }}
    variant="persistent"
    anchor="left"
    open={open}
  >
    <DrawerHeader>
      <IconButton onClick={onClick}>
        <ChevronLeftIcon />
      </IconButton>
    </DrawerHeader>
    <Divider />
    <List component="nav">
      {menuItems.map((data, i) => (
        <MenuItem key={i} {...data} />
      ))}
    </List>
  </Drawer>
);
