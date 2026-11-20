import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import {
    createUserWithEmailAndPassword,
    getAuth,
    signInWithEmailAndPassword,
    updateProfile,
} from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";

const config = JSON.parse(document.getElementById("firebase-config").textContent);
const app = initializeApp(config);
const auth = getAuth(app);

function csrfToken() {
    return document.querySelector("input[name=csrfmiddlewaretoken]")?.value || "";
}

function showError(id, message) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = message;
        element.classList.remove("d-none");
    }
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken(),
        },
        body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok || !data.ok) {
        throw new Error(data.message || "No fue posible completar la operación.");
    }

    return data;
}

const loginForm = document.getElementById("login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const credential = await signInWithEmailAndPassword(
                auth,
                document.getElementById("login-email").value.trim(),
                document.getElementById("login-password").value,
            );

            const data = await postJson("/api/login/firebase/", {
                idToken: await credential.user.getIdToken(),
            });

            window.location.href = data.redirect;
        } catch (error) {
            showError(
                "auth-error",
                "Correo o contraseña incorrectos o Firebase no está disponible.",
            );
        }
    });
}

const registerForm = document.getElementById("register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const name = document.getElementById("register-name").value.trim();
            const email = document.getElementById("register-email").value.trim();
            const password = document.getElementById("register-password").value;

            const credential = await createUserWithEmailAndPassword(
                auth,
                email,
                password,
            );

            await updateProfile(credential.user, { displayName: name });

            await postJson("/api/perfil/firebase/", {
                idToken: await credential.user.getIdToken(true),
                nombre: name,
            });

            document.getElementById("register-success").textContent =
                "Cuenta creada correctamente. Redirigiendo al inicio de sesión...";
            document.getElementById("register-success").classList.remove("d-none");

            await auth.signOut();

            setTimeout(() => {
                window.location.href = "/login/";
            }, 800);
        } catch (error) {
            showError(
                "register-error",
                "No se pudo crear la cuenta. Verifica el correo, la contraseña y la configuración de Firebase.",
            );
        }
    });
}
