const onboardingForm = document.querySelector(".onboarding-form");
const acceptedImageTypes = ["image/jpeg", "image/png", "image/webp"];
const maxImageSize = 2 * 1024 * 1024;
const maxImageDimension = 800;
const imageQuality = 0.82;

function formatBytes(bytes) {
    if (bytes < 1024 * 1024) {
        return `${Math.max(1, Math.round(bytes / 1024))} Ko`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

function getOutputType() {
    const canvas = document.createElement("canvas");

    if (canvas.toDataURL("image/webp").startsWith("data:image/webp")) {
        return "image/webp";
    }

    return "image/jpeg";
}

function getCompressedName(originalName, outputType) {
    const baseName = originalName.replace(/\.[^.]+$/, "") || "photo";
    const extension = outputType === "image/webp" ? "webp" : "jpg";

    return `${baseName}.${extension}`;
}

function loadImage(file) {
    return new Promise((resolve, reject) => {
        const image = new Image();
        const objectUrl = URL.createObjectURL(file);

        image.onload = () => {
            URL.revokeObjectURL(objectUrl);
            resolve(image);
        };

        image.onerror = () => {
            URL.revokeObjectURL(objectUrl);
            reject(new Error("Image illisible"));
        };

        image.src = objectUrl;
    });
}

function canvasToBlob(canvas, type) {
    return new Promise(resolve => {
        canvas.toBlob(resolve, type, imageQuality);
    });
}

async function compressImage(file) {
    const image = await loadImage(file);
    const scale = Math.min(1, maxImageDimension / Math.max(image.width, image.height));
    const width = Math.max(1, Math.round(image.width * scale));
    const height = Math.max(1, Math.round(image.height * scale));
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    const outputType = getOutputType();

    canvas.width = width;
    canvas.height = height;
    context.drawImage(image, 0, 0, width, height);

    let blob = await canvasToBlob(canvas, outputType);

    if (!blob && outputType === "image/webp") {
        blob = await canvasToBlob(canvas, "image/jpeg");
    }

    if (!blob) {
        throw new Error("Compression impossible");
    }

    const compressedFile = new File(
        [blob],
        getCompressedName(file.name, blob.type || outputType),
        { type: blob.type || outputType, lastModified: Date.now() }
    );

    return {
        file: compressedFile,
        width,
        height
    };
}

function replaceInputFile(input, file) {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    input.files = dataTransfer.files;
}

function setupFilePreview(input) {
    if (!input || input.dataset.previewReady === "true") return;

    input.dataset.previewReady = "true";
    input.setAttribute("accept", ".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp");
    input.classList.add("image-input-hidden");

    const preview = document.createElement("div");
    preview.className = "photo-preview-box";
    preview.textContent = "Choisir une image valide";

    const picker = document.createElement("div");
    picker.className = "image-picker";
    picker.innerHTML = `
        <button type="button" class="image-picker-button">Choisir une image</button>
        <span class="image-picker-name">JPG, PNG ou WebP uniquement</span>
    `;

    const feedback = document.createElement("p");
    feedback.className = "file-feedback";
    feedback.setAttribute("aria-live", "polite");

    input.parentNode.insertBefore(preview, input);
    input.parentNode.insertBefore(picker, input);
    input.parentNode.insertBefore(feedback, input.nextSibling);

    const pickerButton = picker.querySelector(".image-picker-button");
    const pickerName = picker.querySelector(".image-picker-name");

    pickerButton.addEventListener("click", () => input.click());

    input.addEventListener("change", async () => {
        const file = input.files && input.files[0];
        feedback.textContent = "";
        feedback.classList.remove("is-success");
        input.classList.remove("file-invalid");

        if (!file) {
            preview.textContent = "Choisir une image valide";
            pickerName.textContent = "JPG, PNG ou WebP uniquement";
            return;
        }

        if (!acceptedImageTypes.includes(file.type)) {
            preview.textContent = "Choisir une image valide";
            pickerName.textContent = "JPG, PNG ou WebP uniquement";
            feedback.textContent = "Ce fichier n'est pas une image valide. Choisis une image JPG, PNG ou WebP.";
            input.classList.add("file-invalid");
            input.value = "";
            return;
        }

        preview.textContent = "Compression de l'image...";
        pickerName.textContent = file.name;

        let compressed;

        try {
            compressed = await compressImage(file);
            replaceInputFile(input, compressed.file);
        } catch (error) {
            preview.textContent = "Choisir une image valide";
            feedback.textContent = "Impossible de compresser cette image. Essaie avec une autre image.";
            input.classList.add("file-invalid");
            input.value = "";
            return;
        }

        if (compressed.file.size > maxImageSize) {
            preview.textContent = "Choisir une image valide";
            pickerName.textContent = "JPG, PNG ou WebP uniquement";
            feedback.textContent = `Image trop lourde apres compression. Taille maximale : ${formatBytes(maxImageSize)}.`;
            input.classList.add("file-invalid");
            input.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = event => {
            preview.innerHTML = `<img src="${event.target.result}" alt="Apercu de l'image selectionnee">`;
            pickerName.textContent = compressed.file.name;
            feedback.textContent = `Image optimisee : ${compressed.width}x${compressed.height}px, ${formatBytes(compressed.file.size)}.`;
            feedback.classList.add("is-success");
        };

        reader.onerror = () => {
            preview.textContent = "Choisir une image valide";
            feedback.textContent = "Impossible de lire cette image. Essaie avec une autre image.";
            pickerName.textContent = "JPG, PNG ou WebP uniquement";
            input.classList.add("file-invalid");
            input.value = "";
        };

        reader.readAsDataURL(compressed.file);
    });
}

document.querySelectorAll('.form-fields input[type="file"]').forEach(setupFilePreview);

function keepDigitsOnly(input) {
    input.value = input.value.replace(/\D/g, "");
}

document.querySelectorAll("[data-digits-only='true']").forEach(input => {
    keepDigitsOnly(input);

    input.addEventListener("input", () => keepDigitsOnly(input));

    input.addEventListener("paste", event => {
        event.preventDefault();
        const pastedText = event.clipboardData.getData("text").replace(/\D/g, "");
        const start = input.selectionStart || 0;
        const end = input.selectionEnd || 0;
        const nextValue = `${input.value.slice(0, start)}${pastedText}${input.value.slice(end)}`;

        input.value = nextValue.slice(0, input.maxLength || nextValue.length);
        input.dispatchEvent(new Event("input", { bubbles: true }));
    });
});

function setupPhoneFields() {
    const indicatif = document.getElementById("id_telephone_indicatif");
    const numero = document.getElementById("id_telephone_numero");

    if (!indicatif || !numero) return;

    const indicatifField = indicatif.closest("p");
    const numeroField = numero.closest("p");

    if (!indicatifField || !numeroField || indicatifField.parentNode !== numeroField.parentNode) return;

    const group = document.createElement("div");
    group.className = "phone-fields";

    indicatifField.parentNode.insertBefore(group, indicatifField);
    group.appendChild(indicatifField);
    group.appendChild(numeroField);
}

setupPhoneFields();

function resizeTextarea(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
    textarea.classList.toggle("is-filled", textarea.value.trim().length > 0);
}

document.querySelectorAll(".form-fields textarea").forEach(textarea => {
    textarea.rows = 1;

    resizeTextarea(textarea);

    textarea.addEventListener("focus", () => resizeTextarea(textarea));
    textarea.addEventListener("input", () => resizeTextarea(textarea));

    textarea.addEventListener("blur", () => {
        if (textarea.value.trim().length === 0) {
            textarea.style.height = "";
            textarea.classList.remove("is-filled");
        }
    });
});

if (onboardingForm) {
    const firstField = onboardingForm.querySelector(
        'input:not([type="hidden"]):not([type="file"]), textarea, select'
    );

    if (firstField && window.matchMedia("(min-width: 769px)").matches) {
        firstField.focus({ preventScroll: true });
    }

    onboardingForm.addEventListener("submit", event => {
        const submitter = event.submitter;

        if (submitter && submitter.name === "wizard_goto_step") {
            return;
        }

        const primaryButton = onboardingForm.querySelector(".btn-primary");

        if (primaryButton) {
            onboardingForm.classList.add("is-submitting");
            primaryButton.disabled = true;
            primaryButton.textContent = primaryButton.textContent.trim() === "Terminer"
                ? "Finalisation..."
                : "Chargement...";
        }
    });
}
