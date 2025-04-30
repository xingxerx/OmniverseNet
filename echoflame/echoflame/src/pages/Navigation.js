import React from 'react';
import { Link } from 'react-router-dom';
function Navigation() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/vision">Vision</Link></li>
        <li><Link to="/harmony">Harmony</Link></li>
        <li><Link to="/assignment">Assignment</Link></li>
        <li><Link to="/ignite">Ignite</Link></li>
      </ul>
    </nav>
  );
}
export default Navigation;
