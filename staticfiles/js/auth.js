const authForms = document.querySelectorAll(".auth-form");
const passwordInputs = document.querySelectorAll("#login_password, #register_password1, #register_password2");

function preventPasswordTransfer(event) {
    event.preventDefault();
}

passwordInputs.forEach(input => {
    ["copy", "cut", "paste", "drop", "contextmenu"].forEach(eventName => {
        input.addEventListener(eventName, preventPasswordTransfer);
    });

    input.addEventListener("beforeinput", event => {
        if (event.inputType === "insertFromPaste" || event.inputType === "insertFromDrop") {
            event.preventDefault();
        }
    });
});

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
        }
    });
});

const icons = {
    check_succes: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" class="lucide lucie-badge-check-icon lucide-badge-check">
    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/>
    <path d="m9 12 2 2 4-4"/>
</svg>`,
    check_error: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-x-icon lucide-badge-x"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><line x1="15" x2="9" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="15"/></svg>`
};

const availability = {
    username: null,
    email: null
};

function setSubmitState(form) {
    const button = form.querySelector(".btn-primary");
    if (!button) return;

    let canSubmit = form.checkValidity();
    const isRegisterForm = Boolean(form.querySelector("#register_password1"));

    if (isRegisterForm) {
        const password1 = form.querySelector("#register_password1");
        const password2 = form.querySelector("#register_password2");

        canSubmit = canSubmit
            && password1
            && password2
            && password1.value.length >= 8
            && password1.value === password2.value
            && availability.username === true
            && availability.email === true;
    }

    button.disabled = !canSubmit;
}

function updateSubmitStates() {
    authForms.forEach(setSubmitState);
}

authForms.forEach(form => {
    form.noValidate = false;
    form.querySelectorAll("input").forEach(input => {
        input.addEventListener("input", updateSubmitStates);
        input.addEventListener("blur", updateSubmitStates);
    });

    form.addEventListener("submit", event => {
        setSubmitState(form);

        if (form.querySelector(".btn-primary")?.disabled) {
            event.preventDefault();
            form.reportValidity();
        }
    });
});

/* USERNAME CHECK */
const usernameInput = document.getElementById("id_username");
const usernameFeedback = document.getElementById("username-feedback");
let lastUsernameValue = "";

if (usernameInput && usernameFeedback) {
    function checkUsernameAvailability() {
        const value = usernameInput.value.trim();

        if (value.length < 1) {
            availability.username = null;
            usernameFeedback.innerHTML = "";
            updateSubmitStates();
            return;
        }

        if (value === lastUsernameValue) {
            updateSubmitStates();
            return;
        }

        lastUsernameValue = value;
        availability.username = false;
        updateSubmitStates();

        fetch(`/auth/check-username/?username=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                if (usernameInput.value.trim() !== value) return;

                availability.username = Boolean(data.available);

                usernameFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";

                if (data.available) {
                    usernameFeedback.innerHTML = icons.check_succes;
                } else {
                    usernameFeedback.innerHTML = icons.check_error;
                }

                updateSubmitStates();
            })
            .catch(error => {
                console.error("Erreur vérification username:", error);
                availability.username = false;
                usernameFeedback.innerHTML = "";
                updateSubmitStates();
            });
    }

    usernameInput.addEventListener("input", function () {
        availability.username = null;
        lastUsernameValue = "";
        usernameFeedback.innerHTML = "";
        updateSubmitStates();
    });

    usernameInput.addEventListener("blur", checkUsernameAvailability);
}


/* EMAIL CHECK (format + existence) */
const emailInput = document.getElementById("id_email");
const emailFeedback = document.getElementById("email-feedback");
let lastEmailValue = "";

if (emailInput && emailFeedback) {
    function checkEmailAvailability() {
        const value = emailInput.value.trim();

        if (value.length < 1) {
            availability.email = null;
            emailFeedback.innerHTML = "";
            updateSubmitStates();
            return;
        }

        if (value === lastEmailValue) {
            updateSubmitStates();
            return;
        }

        // Vérifier le format email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            availability.email = false;
            emailFeedback.innerHTML = icons.check_error;
            emailFeedback.style.color = "#FF6B6B";
            updateSubmitStates();
            return;
        }

        lastEmailValue = value;
        availability.email = false;
        updateSubmitStates();

        // Vérifier l'existence de l'email sur le serveur
        fetch(`/auth/check-email/?email=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                if (emailInput.value.trim() !== value) return;

                availability.email = Boolean(data.available);

                emailFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";

                if (data.available) {
                    emailFeedback.innerHTML = icons.check_succes;
                } else {
                    emailFeedback.innerHTML = icons.check_error;
                }

                updateSubmitStates();
            })
            .catch(error => {
                console.error("Erreur vérification email:", error);
                availability.email = false;
                emailFeedback.innerHTML = "";
                updateSubmitStates();
            });
    }

    emailInput.addEventListener("input", function () {
        availability.email = null;
        lastEmailValue = "";
        emailFeedback.innerHTML = "";
        updateSubmitStates();
    });

    emailInput.addEventListener("blur", checkEmailAvailability);
}

updateSubmitStates();
