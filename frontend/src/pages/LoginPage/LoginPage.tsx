import { TextField, Button, Typography } from '@mui/material';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import styles from './LoginPage.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const FAKE_ADMIN_EMAIL: string = import.meta.env
    .VITE_FAKE_ADMIN_EMAIL as string;
  const FAKE_ADMIN_PASSWORD: string = import.meta.env
    .VITE_ADMIN_SERVICE_PASSWORD as string;
  const navigate = useNavigate();
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    let valid = true;

    if (!email.includes('@')) {
      setEmailError('Введите корректный email');
      valid = false;
    } else if (email !== FAKE_ADMIN_EMAIL) {
      setEmailError('Неверный email');
      valid = false;
    } else {
      setEmailError('');
    }

    if (password.length < 4) {
      setPasswordError('Пароль должен быть не менее 4 символов');
      valid = false;
    } else if (password !== FAKE_ADMIN_PASSWORD) {
      setPasswordError('Неверный пароль');
      valid = false;
    } else {
      setPasswordError('');
    }
    if (valid) void navigate('/');
  };
  return (
    <div className={styles.container}>
      <form noValidate className={styles.login} onSubmit={handleSubmit}>
        <Typography variant="h5" align="center" sx={{ mb: 2, color: 'black' }}>
          Панель администратора
        </Typography>
        <TextField
          label="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          fullWidth
          error={!!emailError}
          helperText={emailError || ' '}
        />
        <TextField
          label="Пароль"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          required
          fullWidth
          error={!!passwordError}
          helperText={passwordError || ' '}
        />
        <Button type="submit" variant="contained">
          Войти
        </Button>
      </form>
    </div>
  );
}
