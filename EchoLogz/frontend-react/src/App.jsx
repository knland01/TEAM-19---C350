import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navbar from './components/navbar';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Navbar />
      <div>
        <h1>Welcome to EchoLogz</h1>
        <p>Your new React front-end is running.</p>
      </div>
    </>
  );
}

export default App;
