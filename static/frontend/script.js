document.addEventListener("DOMContentLoaded", function () {
    let selectedRole = "seeker"; // Default: Job Seeker
    let selectedAuth = "login";  // Default: Login

    function updateToggleUI() {
        document.getElementById("seekerBtn").classList.toggle("active", selectedRole === "seeker");
        document.getElementById("providerBtn").classList.toggle("active", selectedRole === "provider");

        document.querySelector('.toggle-btn[onclick="toggleAuth(\'login\')"]').classList.toggle("active", selectedAuth === "login");
        document.querySelector('.toggle-btn[onclick="toggleAuth(\'register\')"]').classList.toggle("active", selectedAuth === "register");

        const roleSlider = document.querySelector("#roleSlider");
        const authSlider = document.querySelector("#authSlider");

        roleSlider.style.transform = selectedRole === "seeker" ? "translateX(0%)" : "translateX(100%)";
        authSlider.style.transform = selectedAuth === "login" ? "translateX(0%)" : "translateX(100%)";
    }

    function updateForm() {
        if (selectedRole === "seeker" && selectedAuth === "login") {
            window.location.href = "job_seeker_login.html";
        } else if (selectedRole === "seeker" && selectedAuth === "register") {
            window.location.href = "job_seeker_signup.html";
        } else if (selectedRole === "provider" && selectedAuth === "login") {
            window.location.href = "job_provider_login.html";
        } else if (selectedRole === "provider" && selectedAuth === "register") {
            window.location.href = "job_provider_signup.html";
        }
    }

    window.toggleRole = function (role) {
        selectedRole = role;
        updateToggleUI();
    };

    window.toggleAuth = function (authType) {
        selectedAuth = authType;
        updateToggleUI();
        updateForm();
    };

    updateToggleUI();
});

// API CALLS

async function registerJobSeeker(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("http://127.0.0.1:8000/register/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const result = await response.json();

        if (response.ok) {
            alert("Registration successful! Please login.");
            window.location.href = "job_seeker_login.html";
        } else {
            alert("Error: " + result.detail);
        }
    } catch (error) {
        alert("Network error: " + error.message);
    }
}

async function loginJobSeeker(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("http://127.0.0.1:8000/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("access_token", result.access);
            alert("Login successful!");
            window.location.href = "index.html";
        } else {
            alert("Error: " + result.detail);
        }
    } catch (error) {
        alert("Network error: " + error.message);
    }
}
