/**
 * Initialisation de intl-tel-input pour Django
 * Gère : Traduction FR (ES6), Blocage de saisie (Strict Mode), Validation avant envoi.
 */
document.addEventListener("DOMContentLoaded", function() {
    const phoneInput = document.querySelector('input[name*="telephone_numero"]');
    const form = phoneInput ? phoneInput.closest('form') : null;

    if (phoneInput && form) {
        // 1. Chargement dynamique de la langue Française
        import("/static/js/i18n/fr/index.js")
            .then((module) => {
                initIti(module.default);
            })
            .catch((err) => {
                console.warn("Traductions FR non trouvées, passage en anglais:", err);
                initIti({}); // Secours en anglais
            });

        function initIti(translations) {
            const iti = window.intlTelInput(phoneInput, {
                utilsScript: "/static/js/utils.js",
                separateDialCode: true,
                initialCountry: "fr",
                strictMode: true, // Bloque la saisie si le numéro est trop long pour le pays
                i18n: translations,
            });

            // 2. Blocage des caractères non-numériques pendant la saisie
            phoneInput.addEventListener('keypress', function(e) {
                if (!/\d/.test(e.key)) {
                    e.preventDefault();
                }
            });

            // 3. Validation et Fusion avant l'envoi du formulaire
            form.addEventListener('submit', function(e) {
                // On vérifie si le numéro est valide (longueur et format)
                if (phoneInput.value.trim()) {
                    if (!iti.isValidNumber()) {
                        e.preventDefault(); // Bloque l'envoi
                        
                        // Style d'erreur visuel rapide
                        phoneInput.style.borderColor = "#f87171"; 
                        alert("Le numéro de téléphone n'est pas valide pour le pays sélectionné.");
                        return;
                    }
                    
                    /** 
                     * 4. Fusion finale : 
                     * Remplace la valeur du champ par le format international complet (ex: +261320000000)
                     * juste avant que Django ne reçoive les données.
                     */
                    phoneInput.value = iti.getNumber();
                }
            });

            // Optionnel : Feedback visuel pendant la saisie
            phoneInput.addEventListener('keyup', function() {
                if (phoneInput.value.trim()) {
                    phoneInput.style.borderColor = iti.isValidNumber() ? "#10b981" : "#f87171";
                } else {
                    phoneInput.style.borderColor = ""; // Reset si vide
                }
            });
        }
    }
});
