import React from "react";

const CustomUsernameInput = ({ value, onChange }) => {
    return (
        <div style={{width: "100%", marginBottom: "20px"}}>
            <input 
                type="text"
                value={value}
                onChange={onChange}
                placeholder="Your Username"
                style={{
                    width:"100%",
                    height:"40px",
                    padding: "0 12px",
                    fontSize: "16px",
                    border: "1px solid #ccc",
                    borderRadius: "6px",
                    backgroundColor: "#f3f3f3",
                    boxSizing: "border-box"
                    
                }}
            />
        </div>
    )
}

export default CustomUsernameInput