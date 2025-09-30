import { TextField, Button, Typography } from '@mui/material';
import './LoginPage.css';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    let valid = true;

    if (!email.includes('@')) {
      setEmailError('Введите корректный email');
      valid = false;
    } else {
      setEmailError('');
    }

    if (password.length < 4) {
      setPasswordError('Пароль должен быть не менее 4 символов');
      valid = false;
    } else {
      setPasswordError('');
    }
    if (valid) void navigate('/');
  };
  return (
    <form noValidate className="login" onSubmit={handleSubmit}>
      <Typography variant="h5" align="center">
        Вход
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
  );
}
