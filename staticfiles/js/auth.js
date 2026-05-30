document.querySelectorAll(".toggle-password").forEach(btn => {
    btn.addEventListener("click", () => {
        // Récupère l'input cible via l'attribut data-target
        const input = document.getElementById(btn.dataset.target);
        if (!input) return;

        // Récupère les icônes à l'intérieur du bouton
        const eyeOn = btn.querySelector(".icon-eye");
        const eyeOff = btn.querySelector(".icon-eye-off");

        // Bascule le type de l'input
        const isHidden = input.type === "password";
        input.type = isHidden ? "text" : "password";

        // Mise à jour de l'affichage des icônes (avec sécurité si null)
        if (eyeOn && eyeOff) {
            eyeOn.style.display = isHidden ? "none" : "block";
            eyeOff.style.display = isHidden ? "block" : "none";
        } else {
            console.warn("Les éléments .eye ou .eye-off sont manquants dans le bouton:", btn);
        }
    });
});

const icons = {
    check_succes: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" class="lucide lucie-badge-check-icon lucide-badge-check">
    <path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/>
    <path d="m9 12 2 2 4-4"/>
</svg>`,
    check_error: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-x-icon lucide-badge-x"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><line x1="15" x2="9" y1="9" y2="15"/><line x1="9" x2="15" y1="9" y2="15"/></svg>`
}

function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

/* USERNAME CHECK */
const usernameInput = document.getElementById("id_username");
const usernameFeedback = document.getElementById("username-feedback");
let lastUsernameValue = "";

if (usernameInput && usernameFeedback) {
    
    usernameInput.addEventListener("blur", function () {
        const value = this.value.trim();
        
        // Ne vérifier que si la valeur a changé et n'est pas vide
        if (value.length < 1 || value === lastUsernameValue) {
            usernameFeedback.innerHTML = "";
            return;
        }
        
        lastUsernameValue = value;
        
        fetch(`/auth/check-username/?username=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                
                usernameFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";
                
                if (data.available) {
                    usernameFeedback.innerHTML = icons.check_succes;
                } else {
                    usernameFeedback.innerHTML = icons.check_error;
                }
            })
            .catch(error => {
                console.error("Erreur vérification username:", error);
                usernameFeedback.innerHTML = "";
            });
    });
}


/* EMAIL CHECK (format + existence) */
const emailInput = document.getElementById("id_email");
const emailFeedback = document.getElementById("email-feedback");
let lastEmailValue = "";

if (emailInput && emailFeedback) {
    
    emailInput.addEventListener("blur", function () {
        const value = this.value.trim();
        
        // Ne vérifier que si la valeur a changé et n'est pas vide
        if (value.length < 1 || value === lastEmailValue) {
            emailFeedback.innerHTML = "";
            return;
        }
        
        // Vérifier le format email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            emailFeedback.innerHTML = icons.check_error;
            emailFeedback.style.color = "#FF6B6B";
            return;
        }
        
        lastEmailValue = value;
        
        // Vérifier l'existence de l'email sur le serveur
        fetch(`/auth/check-email/?email=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                
                emailFeedback.style.color = data.available ? "#2ECC71" : "#FF6B6B";
                
                if (data.available) {
                    emailFeedback.innerHTML = icons.check_succes;
                } else {
                    emailFeedback.innerHTML = icons.check_error;
                }
            })
            .catch(error => {
                console.error("Erreur vérification email:", error);
                emailFeedback.innerHTML = "";
            });
    });
} else console.log("Erreur");