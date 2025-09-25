import { Routes, Route } from 'react-router-dom';

import Main from '@components/Main/Main';

import './App.css';

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/login" element={<></>} />
        <Route path="*" element={<></>} />
      </Routes>
    </div>
  );
}

export default App;
