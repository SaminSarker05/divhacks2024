// import { useState } from 'react'
// import axios from "axios";
import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import Login from './login';
import Register from './register';
// import Test from './test';

function App() {
  return (
      <Router>
          <Routes>
              <Route exact path="/" element={<Login />} />
          </Routes>
      </Router>
  );
}

export default App;