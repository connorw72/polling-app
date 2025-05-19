import React, {useState} from 'react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <div style = {navbarStyle}>
        <NavButton to="/">Home</NavButton>
        <NavButton to="/vote">Votes</NavButton>
        <NavButton to="/history">History</NavButton>
   </div>
  );
}

const NavButton = ({ to, children }) => {
    const [hover, setHover] = useState(false);

    return (
        <NavLink to={to} style={{ textDecoration: "none"}}>
            <button
                style = {{
                    ...buttonStyle,
                    backgroundColor: hover ? "b8860b" : "transparent",
                    color: hover ? "#fed800" : "white",
                }}
                onMouseEnter={() => setHover(true)}
                onMouseLeave={() => setHover(false)}
            >
                {children}
            </button>
        </NavLink>
    );
};

const navbarStyle = {
    display: "flex", 
    justifyContent: "center", 
    alignItems: "center",
    width: "100%",
    padding: "15px 0",
    backgroundColor: "#333",
    position: "fixed",
    top: "0",
    left: "0",
    zIndex: "1000"
}


const buttonStyle = {
    margin: "0 15px",
    padding: "10px 20px",
    fontSize: "18px",
    border: "none",
    borderRadius: "8px",
    backgroundColor: "transparent",
    color: "white",
    cursor: "pointer",
    transition: "background-color 0.3s ease, color 0.3s ease",
};


export default Navbar;