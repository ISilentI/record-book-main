import React, { useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import { Link } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import MireaLogo from '../../../components/elements/icons/MireaLogo';
import Container from '@mui/material/Container';
import { useNavigate } from 'react-router-dom';
import AppButton from '../../../components/elements/buttons/AppButton';
import API from '../../../api';

export default function SignUp() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [middleName, setMiddleName] = useState('');
  const [group, setGroup] = useState('');
  const [course, setCourse] = useState(1);

  const handleChangeEmail = e => {
    setEmail(e.target.value);
  };

  const handleChangePassword = e => {
    setPassword(e.target.value);
  };

  const handleChangeName = e => {
    setFirstName(e.target.value);
  };

  const handleChangeSurname = e => {
    setLastName(e.target.value);
  };

  const handleChangePatronymic = e => {
    setMiddleName(e.target.value);
  };

  const handleChangeGroup = e => {
    setGroup(e.target.value);
  };

  const handleChangeCourse = e => {
    setCourse(e.target.value);
  };

  const handleSubmit = event => {
    event.preventDefault();
    const data = {
      "email": email,
      "password": password,
      "first_name": firstName,
      "last_name": lastName,
      "middle_name": middleName,
      "group": group,
      "course": course
    }
    const registerUser = async () => {
      const result = await API.post(`/signup`, data, {headers: {Authorization: `Bearer ${localStorage.getItem('access_token')}`}});
      if (result.status === 200) {
        navigate("/");
      }
    };
    registerUser();
  };

  return (
    <Box
      component='section'
      sx={{
        width: '100%',
        height: '100vh',
        pt: 16,
      }}>
      <Container component='main' maxWidth='xs'>
        <CssBaseline />
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}>
          <MireaLogo />
          <Box
            component='form'
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}>
            <TextField
              value={email}
              onChange={handleChangeEmail}
              margin='normal'
              required
              fullWidth
              id='email'
              label='Почта'
              name='email'
              autoComplete='email'
              autoFocus
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={password}
              onChange={handleChangePassword}
              margin='normal'
              required
              fullWidth
              name='password'
              label='Пароль'
              type='password'
              id='password'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={firstName}
              onChange={handleChangeName}
              margin='normal'
              required
              fullWidth
              name='first_name'
              label='Имя'
              type='text'
              id='first_name'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={lastName}
              onChange={handleChangeSurname}
              margin='normal'
              required
              fullWidth
              name='last_name'
              label='Фамилия'
              type='text'
              id='last_name'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={middleName}
              onChange={handleChangePatronymic}
              margin='normal'
              required
              fullWidth
              name='middle_name'
              label='Отчество'
              type='text'
              id='middle_name'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={group}
              onChange={handleChangeGroup}
              margin='normal'
              required
              fullWidth
              name='group'
              label='Группа'
              type='text'
              id='group'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <TextField
              value={course}
              onChange={handleChangeCourse}
              margin='normal'
              required
              fullWidth
              name='сourse'
              label='Курс'
              type='number'
              id='сourse'
              autoComplete='current-password'
              sx={{
                '& .MuiInputBase-root': {
                  borderRadius: '12px',
                },
              }}
            />
            <AppButton type='submit' fullWidth sx={{ mt: 3, mb: 2, p: 1.5 }}>
              Регистрация
            </AppButton>
            <Grid container>
              <Grid item xs>
                <Link to='/'>
                  <Button
                    variant='text'
                    sx={{
                      textTransform: 'none',
                      color: 'var(--color-primary)',
                      borderRadius: '12px',
                    }}>
                    Вход
                  </Button>
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </Box>
  );
}
