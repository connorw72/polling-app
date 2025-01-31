import React, { useState } from "react";

const CustomEmailInput = ({ value, onChange }) => {
    const [isValid, setIsValid] = useState(true);

    const handleEmailChange = (e) => {
        const email = e.target.value;
        onChange(e);
        
        setIsValid(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email));
    };

    return (
        <div style={{ width: "100%", marginBottom: "20px" }}>
            {/* Email Input Field */}
            <input 
                type="email"
                value={value}
                onChange={handleEmailChange}
                placeholder="Your Email"
                style={{
                    width:"100%",
                    height:"40px",
                    padding: "0 12px",
                    fontSize: "16px",
                    border: isValid ? "1px solid #ccc" : "1px solid red", // if invalid
                    borderRadius: "6px",
                    backgroundColor: "#f3f3f3",
                    boxSizing: "border-box"
                }}
            />
            {/* Error Message */}
            {!isValid && (
                <span style={{ color: "red", fontSize: "12px", marginTop: "5px", display: "block "}}>
                    Please enter a valid email address
                </span>
            )}
        </div>
    )
}

export default CustomEmailInput;
