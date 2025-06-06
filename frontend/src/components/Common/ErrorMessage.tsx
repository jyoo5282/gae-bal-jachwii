import React from 'react';
import { Alert, AlertTitle, Box } from '@mui/material';

interface ErrorMessageProps {
  title?: string;
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ 
  title = '오류가 발생했습니다', 
  message 
}) => {
  return (
    <Box my={2}>
      <Alert severity="error">
        <AlertTitle>{title}</AlertTitle>
        {message}
      </Alert>
    </Box>
  );
};

export default ErrorMessage; 