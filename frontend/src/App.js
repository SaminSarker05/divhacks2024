// import { useState } from 'react'
// import axios from "axios";
// import './App.css';
import './index.css'; // or your relevant CSS file
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Login from './login';
import Register from './register';
import Home from './home';

function App() {
  return (
    <Router>
        <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/login" element={<Login/>} />
            <Route exact path="/register" element={<Register />} />

        </Routes>
    </Router>
  );
}

export default App;