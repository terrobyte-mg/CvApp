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