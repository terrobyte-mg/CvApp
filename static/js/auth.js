document.addEventListener("DOMContentLoaded", () => {

    const loginBox = document.querySelector('.login-box');
    const registerBox = document.querySelector('.register-box');

    const switchBtn = document.getElementById('switch-btn');
    const switchTitle = document.getElementById('switch-title');
    const switchText = document.getElementById('switch-text');

    let loginMode = true;

    switchBtn.addEventListener('click', () => {

        loginMode = !loginMode;

        if (loginMode) {

            loginBox.classList.add('active');
            registerBox.classList.remove('active');

            switchTitle.textContent = "Bienvenue 👋";
            switchText.textContent = "Pas encore de compte ?";
            switchBtn.textContent = "S'inscrire";

        } else {

            registerBox.classList.add('active');
            loginBox.classList.remove('active');

            switchTitle.textContent = "Créer un compte";
            switchText.textContent = "Déjà inscrit ?";
            switchBtn.textContent = "Se connecter";
        }
    });

});