import { styled } from '@mui/material/styles';
import MuiAppBar, {
  type AppBarProps as MuiAppBarProps,
} from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import IconButton from '@mui/material/IconButton';

import type { FC } from 'react';

interface AppHeaderStyled extends MuiAppBarProps {
  open?: boolean;
}

export const drawerWidth = 240;

const AppHeaderStyled = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})<AppHeaderStyled>(({ theme }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  variants: [
    {
      props: ({ open }) => open,
      style: {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: `${drawerWidth}px`,
        transition: theme.transitions.create(['margin', 'width'], {
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen,
        }),
      },
    },
  ],
}));

interface AppHeader {
  open: boolean;
  onClick: () => void;
  title: string;
}

export const AppHeader: FC<AppHeader> = ({ open, onClick, title }) => {
  return (
    <AppHeaderStyled position="fixed" open={open} component="header">
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          onClick={onClick}
          edge="start"
          sx={[
            {
              mr: 2,
            },
            open && { display: 'none' },
          ]}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div">
          {title}
        </Typography>
      </Toolbar>
    </AppHeaderStyled>
  );
};
