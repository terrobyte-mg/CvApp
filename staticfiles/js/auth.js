document.querySelectorAll(".toggle-password").forEach(btn => {
    btn.addEventListener("click", () => {
        const input = document.getElementById(btn.dataset.target);
        if (!input) return;

        const eyeOn = btn.querySelector(".icon-eye");
        const eyeOff = btn.querySelector(".icon-eye-off");

        const isHidden = input.type === "password";
        input.type = isHidden ? "text" : "password";

        if (eyeOn && eyeOff) {
            eyeOn.style.display = isHidden ? "none" : "block";
            eyeOff.style.display = isHidden ? "block" : "none";
        } else {
            console.warn("Les éléments .eye ou .eye-off sont manquants dans le bouton:", btn);
        }
    });
});

/* ===== SÉCURITÉ : Désactiver copier-coller sur les mots de passe ===== */
document.querySelectorAll("input[type='password'], input#register_password1, input#register_password2, input#login_password").forEach(input => {
    input.addEventListener("copy", (e) => {
        e.preventDefault();
        console.warn("Copier les mots de passe est désactivé pour des raisons de sécurité.");
    });
    
    input.addEventListener("paste", (e) => {
        e.preventDefault();
        console.warn("Coller dans les mots de passe est désactivé pour des raisons de sécurité.");
    });
    
    input.addEventListener("cut", (e) => {
        e.preventDefault();
        console.warn("Couper les mots de passe est désactivé pour des raisons de sécurité.");
    });
});

const icons = {
    check_succes: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" class="lucide lucie-badge-check-icon lucide-badge-check">
    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/>
    <path d="m9 12 2 2 4-4"/>
</svg>`,
    check_error: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-x-icon lucide-badge-x"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><line x1="15" x2="9" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="15"/></svg>`
}

/* ===== VALIDATION STATE TRACKING ===== */
const validationState = {
    username: false,
    email: false,
    password1: false,
    password2: false,
    passwordsMatch: false
};

const usernameInput = document.getElementById("id_username");
const usernameFeedback = document.getElementById("username-feedback");
const emailInput = document.getElementById("id_email");
const emailFeedback = document.getElementById("email-feedback");
const password1Input = document.getElementById("register_password1");
const password2Input = document.getElementById("register_password2");
const submitBtn = document.getElementById("register-submit-btn");

let lastUsernameValue = "";
let lastEmailValue = "";

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

function updateSubmitButton() {
    if (!submitBtn) return;
    
    const allValid = validationState.username && 
                     validationState.email && 
                     validationState.password1 && 
                     validationState.password2 && 
                     validationState.passwordsMatch;
    
    submitBtn.disabled = !allValid;
}

/* ===== USERNAME VALIDATION ===== */
if (usernameInput && usernameFeedback) {
    usernameInput.addEventListener("blur", function () {
        const value = this.value.trim();
        
        if (value.length < 2) {
            validationState.username = false;
            usernameFeedback.innerHTML = "";
            updateSubmitButton();
            return;
        }
        
        if (value === lastUsernameValue) {
            updateSubmitButton();
            return;
        }
        
        lastUsernameValue = value;
        
        fetch(`/auth/check-username/?username=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                validationState.username = data.available;
                usernameFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";
                usernameFeedback.innerHTML = data.available ? icons.check_succes : icons.check_error;
                updateSubmitButton();
            })
            .catch(error => {
                console.error("Erreur vérification username:", error);
                validationState.username = false;
                usernameFeedback.innerHTML = "";
                updateSubmitButton();
            });
    });
}

/* ===== EMAIL VALIDATION ===== */
if (emailInput && emailFeedback) {
    emailInput.addEventListener("blur", function () {
        const value = this.value.trim();
        
        if (value.length < 5) {
            validationState.email = false;
            emailFeedback.innerHTML = "";
            updateSubmitButton();
            return;
        }
        
        if (!emailRegex.test(value)) {
            validationState.email = false;
            emailFeedback.innerHTML = icons.check_error;
            emailFeedback.style.color = "#FF6B6B";
            updateSubmitButton();
            return;
        }
        
        if (value === lastEmailValue) {
            updateSubmitButton();
            return;
        }
        
        lastEmailValue = value;
        
        fetch(`/auth/check-email/?email=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                validationState.email = data.available;
                emailFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";
                emailFeedback.innerHTML = data.available ? icons.check_succes : icons.check_error;
                updateSubmitButton();
            })
            .catch(error => {
                console.error("Erreur vérification email:", error);
                validationState.email = false;
                emailFeedback.innerHTML = "";
                updateSubmitButton();
            });
    });
}

/* ===== PASSWORD VALIDATION ===== */
if (password1Input && password2Input) {
    function validatePasswords() {
        const pass1 = password1Input.value.trim();
        const pass2 = password2Input.value.trim();
        
        validationState.password1 = pass1.length >= 8;
        validationState.password2 = pass2.length >= 8;
        validationState.passwordsMatch = pass1.length >= 8 && pass2.length >= 8 && pass1 === pass2;
        
        updateSubmitButton();
    }
    
    password1Input.addEventListener("input", validatePasswords);
    password2Input.addEventListener("input", validatePasswords);
    password1Input.addEventListener("blur", validatePasswords);
    password2Input.addEventListener("blur", validatePasswords);
}

/* ===== LOGIN FORM VALIDATION ===== */
const loginUsernameInput = document.getElementById("id_username");
const loginPasswordInput = document.getElementById("login_password");
const loginSubmitBtn = document.getElementById("login-submit-btn");

if (loginUsernameInput && loginPasswordInput && loginSubmitBtn) {
    function validateLoginForm() {
        const username = loginUsernameInput.value.trim();
        const password = loginPasswordInput.value.trim();
        
        const isValid = username.length >= 2 && password.length >= 6;
        loginSubmitBtn.disabled = !isValid;
    }
    
    loginUsernameInput.addEventListener("input", validateLoginForm);
    loginPasswordInput.addEventListener("input", validateLoginForm);
    loginUsernameInput.addEventListener("blur", validateLoginForm);
    loginPasswordInput.addEventListener("blur", validateLoginForm);
}
