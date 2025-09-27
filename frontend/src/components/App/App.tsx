import { Routes, Route } from 'react-router-dom';

import MainPage from '../../pages/MainPage/MainPage';
import Login from '../../pages/Login/Login';

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/login" element={<Login />} />
      {/* <Route path="/statistics" element={<Statistics />} /> */}
    </Routes>
  );
}

export default App;
