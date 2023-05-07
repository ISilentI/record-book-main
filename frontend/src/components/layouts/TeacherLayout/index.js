import { Box } from '@mui/material';
import { Stack } from '@mui/system';
import React from 'react';
import ProfileCard from '../../elements/cards/ProfileCard';
import AllRecordBooksTable from '../../elements/tables/AllRecordBooksTable';
import TestInfoGroup from '../../modules/groups/TestInfoGroup';

export default function TeacherLayout() {
  return (
    <Box sx={{ p: '32px' }}>
      <Stack sx={{ gap: '32px', maxWidth: 'var(--max-width)', m: '0 auto' }}>
        <ProfileCard role="teacher"/>
        <TestInfoGroup />
        <AllRecordBooksTable />
      </Stack>
    </Box>
  );
}
