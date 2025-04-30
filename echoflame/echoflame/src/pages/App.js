import React from 'react';
import Navigation from './components/Navigation';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Vision from './pages/Vision';
import Harmony from './pages/Harmony';
import Assignment from './pages/Assignment';
import Ignite from './pages/Ignite';
function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/vision" element={<Vision />} />
        <Route path="/harmony" element={<Harmony />} />
        <Route path="/assignment" element={<Assignment />} />
        <Route path="/ignite" element={<Ignite />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;

