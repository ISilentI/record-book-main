import { Box } from '@mui/material';
import { Stack } from '@mui/system';
import React from 'react';
import ProfileCard from '../../elements/cards/ProfileCard';
import RecordBookTabs from '../../elements/tabs/RecordBookTabs';

export default function StudentLayout() {
  return (
    <Box sx={{ p: '32px' }}>
      <Stack sx={{ gap: '32px', maxWidth: 'var(--max-width)', m: '0 auto' }}>
        <ProfileCard role="student"/>
        <RecordBookTabs />
      </Stack>
    </Box>
  );
}
