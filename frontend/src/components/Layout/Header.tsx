import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  IconButton,
  useTheme,
  Box
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';

interface HeaderProps {
  onRefresh: () => void;
}

const Header: React.FC<HeaderProps> = ({ onRefresh }) => {
  const theme = useTheme();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          한국 경제 뉴스
        </Typography>
        <Box>
          <IconButton
            color="inherit"
            onClick={onRefresh}
            title="뉴스 새로고침"
          >
            <RefreshIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 