import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import { useCurrentRouteData } from '@hooks/useCurrentRouteData';
import { AppHeader } from '@components/AppHeader/AppHeader';
import { DrawerHeader, Sidebar } from '@components/Sidebar/Sidebar';
import { Main } from '@components/Main/Main';

function App() {
  const [open, setOpen] = useState(false);
  const { title } = useCurrentRouteData();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppHeader open={open} onClick={handleDrawerOpen} title={title} />
      <Sidebar open={open} onClick={handleDrawerClose} />
      <Main open={open}>
        <DrawerHeader />
        <Outlet />
      </Main>
    </Box>
  );
}

export default App;
