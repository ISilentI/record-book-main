import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@mui/material';
import MireaLogo from '../../../elements/icons/MireaLogo';
import styles from './Header.module.scss';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../../../../hooks/useAuth';

export default function Header({ logo, exit }) {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const { state } = useLocation();

  const handleLogout = () => {
    logout().then(() => {
      navigate(state?.path || '/');
    });
  };

  return (
    <header className={styles.header}>
      <div className={styles.contentContainer}>
        {logo && (
          <div className={styles.logoContainer}>
            <Link
              to='/'
              style={{ width: 'fit-content', justifySelf: 'center' }}>
              <MireaLogo />
            </Link>
          </div>
        )}
        <p className={styles.title}>Электронная зачетная книжка</p>
        {exit && (
          <Button
            variant='text'
            color='error'
            onClick={handleLogout}
            sx={{
              textTransform: 'none',
              fontFamily: 'var(--primary-font)',
              fontWeight: 400,
              fontSize: '16px',
              lineHeight: '140%',
            }}>
            Выйти
          </Button>
        )}
      </div>
    </header>
  );
}
