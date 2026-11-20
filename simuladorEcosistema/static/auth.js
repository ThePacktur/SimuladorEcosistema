import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, updateProfile } from "https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js";

const config = JSON.parse(document.getElementById("firebase-config").textContent);
const app = initializeApp(config);
const auth = getAuth(app);

function csrfToken() {
    return document.querySelector("input[name=csrfmiddlewaretoken]")?.value || "";
}
function showError(id, message) {
    const el = document.getElementById(id);
    if (el) { el.textContent = message; el.classList.remove("d-none"); }
}
async function postToken(idToken) {
    const response = await fetch("/api/login/firebase/", {
        method: "POST",
        headers: {"Content-Type":"application/json","X-CSRFToken":csrfToken()},
        body: JSON.stringify({idToken})
    });
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.message || "No fue posible iniciar sesión.");
    window.location.href = data.redirect;
}
const login = document.getElementById("login-form");
if (login) login.addEventListener("submit", async e => {
    e.preventDefault();
    try {
        const credential = await signInWithEmailAndPassword(auth, document.getElementById("login-email").value.trim(), document.getElementById("login-password").value);
        await postToken(await credential.user.getIdToken());
    } catch (error) { showError("auth-error","Correo o contraseña incorrectos."); }
});
const register = document.getElementById("register-form");
if (register) register.addEventListener("submit", async e => {
    e.preventDefault();
    try {
        const name=document.getElementById("register-name").value.trim();
        const email=document.getElementById("register-email").value.trim();
        const password=document.getElementById("register-password").value;
        const credential=await createUserWithEmailAndPassword(auth,email,password);
        await updateProfile(credential.user,{displayName:name});
        document.getElementById("register-success").textContent="Cuenta creada correctamente. Redirigiendo...";
        document.getElementById("register-success").classList.remove("d-none");
        setTimeout(()=>window.location.href="/login/",800);
    } catch (error) { showError("register-error","No se pudo crear la cuenta. Verifica el correo y la contraseña."); }
});