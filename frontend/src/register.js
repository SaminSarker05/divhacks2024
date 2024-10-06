import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/register', {
        username,
        password,
      });
      alert(response.data.message);
    } catch (error) {
      console.log('hello world');
      console.log(error);
      alert(error.response.data.message);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <input 
        type="text" 
        placeholder="Username" 
        value={username}
        onChange={(e) => setUsername(e.target.value)} 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password}
        onChange={(e) => setPassword(e.target.value)} 
      />
      <button type="submit">Register</button>
    </form>
  );
}

export default Register;
