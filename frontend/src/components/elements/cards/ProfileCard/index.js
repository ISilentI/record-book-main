import { Avatar, Paper, Typography } from '@mui/material';
import { Stack } from '@mui/system';
import React, { useEffect, useState } from 'react';
import API from '../../../../api';


export default function ProfileCard({ role }) {
  const [user, setUser] = useState({});

  useEffect(() => {
    const getUserData = async () => {
      const result = await API.get(`/user/me`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      role === "student" ? setUser({
        "fullName": result.data.first_name + " " + result.data.last_name + " " + result.data.middle_name,
        "email": result.data.email,
        "group": result.data.group,
        "course": result.data.course + " курс",
      }) : setUser({
        "fullName": result.data.first_name + " " + result.data.last_name + " " + result.data.middle_name,
        "email": result.data.email,
        "departament": result.data.departament,
        "position": result.data.position,
      });
    };
    getUserData();
  }, [role])

  return (
    <Paper
      elevation={3}
      sx={{
        p: '16px',
        boxShadow: '0px 4px 20px rgba(83, 83, 83, 0.1)',
        borderRadius: '32px',
      }}>
      <Stack direction='row' alignItems='center' justifyContent='space-between'>
        <Avatar
          alt='Иванов Иван Иванович'
          src='https://static.tildacdn.com/tild6264-3065-4233-b632-356161663331/s1200.jpeg'
          sx={{ width: '192px', height: '192px' }}
        />
        <Stack sx={{ gap: '16px' }}>
          <Typography
            sx={{
              fontWeight: 700,
              fontSize: '40px',
              lineHeight: '110%',
              color: '#000',
            }}>
            {user.fullName}
          </Typography>
          <Typography
            sx={{
              fontWeight: 700,
              fontSize: '20px',
              lineHeight: '135%',
              color: '#000',
            }}>
            {user.email}
          </Typography>
        </Stack>
        <Stack sx={{ gap: '16px' }}>
          <Typography
            sx={{
              fontWeight: 600,
              fontSize: '24px',
              lineHeight: '130%',
              color: '#000',
            }}>
            {role === "student" ? user.group : user.departament}
          </Typography>
          <Typography
            sx={{
              fontWeight: 600,
              fontSize: '24px',
              lineHeight: '130%',
              color: '#000',
            }}>
            {role === "student" ? user.course : user.position}
          </Typography>
        </Stack>
      </Stack>
    </Paper>
  );
}
