const API_BASE =
    location.hostname === "askyellow.nl" || location.hostname === "www.askyellow.nl"
        ? "https://askyellow-ai.onrender.com"
        : "https://askyellow-staging.onrender.com";

function showError(message) {
    const box = document.getElementById("errorBox");
    if (box) box.textContent = message;
}

function clearError() {
    const box = document.getElementById("errorBox");
    if (box) box.textContent = "";
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".toggle-password").forEach(toggle => {
        toggle.addEventListener("click", () => {
            const input = document.getElementById(toggle.dataset.target);
            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            toggle.textContent = isPassword ? "🙈" : "👁️";
        });
    });

    const form = document.getElementById("registerForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        clearError();

        const first_name = document.getElementById("firstName").value.trim();
        const last_name = document.getElementById("lastName").value.trim();
        const email = document.getElementById("email").value.trim().toLowerCase();
        const password = document.getElementById("password").value;
        const password2 = document.getElementById("password2").value;

        if (!first_name || !last_name || !email || !password || !password2) {
            showError("Vul alle velden in.");
            return;
        }

        if (password.length < 6) {
            showError("Wachtwoord moet minimaal 6 tekens hebben.");
            return;
        }

        if (password !== password2) {
            showError("Wachtwoorden komen niet overeen.");
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/auth/register`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    first_name,
                    last_name,
                    email,
                    password
                })
            });

            const data = await res.json();

            if (!res.ok) {
                showError(data.detail || "Registreren mislukt.");
                return;
            }

            window.location.href = `/test/login.html?registered=1`;
        } catch (err) {
            console.error("Register failed:", err);
            showError("Kon geen account aanmaken. Probeer het later opnieuw.");
        }
    });
});




// const BASE_PATH = "";

// function showError(msg) {
//     document.getElementById("errorBox").textContent = msg;
// }

// document
//     .getElementById("registerForm")
//     .addEventListener("submit", async (e) => {
//         e.preventDefault();

//         const first = document.getElementById("firstName").value.trim();
//         const last = document.getElementById("lastName").value.trim();
//         const email = document.getElementById("email").value.trim().toLowerCase();
//         const pw = document.getElementById("password").value;
//         const pw2 = document.getElementById("password2").value.trim();

//         // ----------- VALIDATIE -----------
//         if (!first || !last || !email || !pw || !pw2) {
//             return showError("Vul alle velden in.");
//         }

//         if (!email.includes("@") || !email.includes(".")) {
//             return showError("Vul een geldig emailadres in.");
//         }

//         if (pw.length < 6) {
//             return showError("Wachtwoord moet minimaal 6 tekens zijn.");
//         }

//         if (pw !== pw2) {
//             return showError("Wachtwoorden komen niet overeen.");
//         }

//         showError("");

//         try {
//             // ✅ BACKEND
//             const API_BASE = "https://askyellow-staging.onrender.com";
//             const res = await fetch(`${API_BASE}/auth/register`, {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({
//                     email: email,
//                     password: pw,
//                     first_name: first,
//                     last_name: last
//                 })
//             });

//             const data = await res.json();

//             if (!res.ok) {
//                 showError(data.detail || "Registratie mislukt.");
//                 return;
//             }

//             // ----------- SUCCES -----------
//             // Registratie = login

//             localStorage.setItem("ay_session_id", data.session_id);
//             localStorage.setItem("authUserName", data.first_name || first);

//             // Door naar chat
//             window.location.href = `${BASE_PATH}/chat.html`;
//             // // Session opslaan (DIT MAG NU)
//             // localStorage.setItem("authSession", loginData.session_id);
//             // localStorage.setItem("authUserName", loginData.first_name || first);
//             // Door naar chat
//             window.location.href = `${BASE_PATH}/chat.html`;


//         } catch (err) {
//             console.error(err);
//             showError("Kon geen verbinding maken met de server.");
//         }
//     });

// document.querySelectorAll(".toggle-password").forEach(toggle => {
//     toggle.addEventListener("click", () => {
//         const input = document.getElementById(toggle.dataset.target);
//         const isPassword = input.type === "password";

//         input.type = isPassword ? "text" : "password";
//         toggle.textContent = isPassword ? "🙈" : "👁️";
//     });
// });

