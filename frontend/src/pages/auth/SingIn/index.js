import React, { useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import { Link } from 'react-router-dom';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import MireaLogo from '../../../components/elements/icons/MireaLogo';
import Container from '@mui/material/Container';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../../../hooks/useAuth';
import AppButton from '../../../components/elements/buttons/AppButton';

export default function SignIn() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { state } = useLocation();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleChangeEmail = e => {
    setEmail(e.target.value);
  };

  const handleChangePassword = e => {
    setPassword(e.target.value);
  };

  const handleSubmit = event => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    login(data.get('email'), data.get('password')).then(() => {
      navigate(state?.path || "/" + localStorage.getItem('role'));
    });
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
            <AppButton
              type='submit'
              fullWidth
              variant='contained'
              sx={{ mt: 3, mb: 2, p: 1.5 }}>
              Вход
            </AppButton>
            <Grid container>
              <Grid item xs>
                <Link to='/register'>
                  <Button
                    variant='text'
                    sx={{
                      textTransform: 'none',
                      color: 'var(--color-primary)',
                      borderRadius: '12px',
                    }}>
                    Регистрация
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
