function switchTab(tab) {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const resetForm = document.getElementById("resetForm");
    const loginBtn = document.getElementById("loginTabBtn");
    const regBtn = document.getElementById("registerTabBtn");
    const message = document.getElementById("message");

    message.textContent = "";

    loginForm.classList.add("hidden");
    registerForm.classList.add("hidden");
    resetForm.classList.add("hidden");
    loginBtn.classList.remove("active");
    regBtn.classList.remove("active");

    if (tab === "login") {
        loginForm.classList.remove("hidden");
        loginBtn.classList.add("active");
    } else if (tab === "register") {
        registerForm.classList.remove("hidden");
        regBtn.classList.add("active");
    } else if (tab === "reset") {
        resetForm.classList.remove("hidden");
    }
}

// Handle Login
document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;
    const message = document.getElementById("message");

    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    if (result.success) {
        window.location.href = result.redirect;
    } else {
        message.textContent = result.message;
        message.style.color = "red";
    }
});

// Handle Register
document.getElementById("registerForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPassword").value;
    const message = document.getElementById("message");

    const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    message.textContent = result.message;
    message.style.color = result.success ? "green" : "red";
});

// Handle Password Reset
document.getElementById("resetForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const email = document.getElementById("resetEmail").value.trim();
    const password = document.getElementById("newPassword").value;
    const message = document.getElementById("message");

    const response = await fetch("/reset-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    message.textContent = result.message;
    message.style.color = result.success ? "green" : "red";
    if (result.success) {
        setTimeout(() => switchTab("login"), 1500);
    }
});