import React, { useState } from "react";

const CustomPasswordInput = ({ value, onChange }) => {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <div
            style={{
                position: "relative", // For absolute positioning of toggle
                width: "100%", // Full width container
                marginBottom: "20px", // Spacing below input
            }}
        >
            {/* Input Field */}
            <input
                type={showPassword ? "text" : "password"}
                value={value}
                onChange={onChange}
                placeholder="Your Password"
                style={{
                    width: "100%", // Full width
                    height: "40px", // Fixed height
                    padding: "0 40px 0 12px", // Space for toggle button
                    fontSize: "16px", // Font size for input text
                    border: "1px solid #ccc", // Border styling
                    borderRadius: "6px", // Rounded corners
                    backgroundColor: "#f3f3f3", // Light gray background
                    boxSizing: "border-box"
                }}
            />

            {/* Toggle Button */}
            <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                    position: "absolute", // Positioned relative to the parent
                    top: "50%", // Center vertically
                    right: "10px", // Align to the right
                    transform: "translateY(-50%)", // Adjust for proper centering
                    background: "none", // Transparent background
                    border: "none", // No border
                    color: "#007BFF", // Blue text
                    fontSize: "14px", // Font size for toggle text
                    cursor: "pointer", // Pointer cursor on hover
                }}
            >
                {showPassword ? "Hide" : "Show"}
            </button>
        </div>
    );
};

export default CustomPasswordInput;
