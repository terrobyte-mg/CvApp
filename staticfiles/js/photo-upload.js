/**
 * Photo Upload Handler
 * Handles image preview, validation, and drag-and-drop for photo inputs
 */

class PhotoUploadHandler {
    constructor(options = {}) {
        this.maxSize = options.maxSize || 5 * 1024 * 1024; // 5 MB default
        this.acceptedTypes = options.acceptedTypes || ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
        this.init();
    }

    init() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupPhotoInputs();
        });
    }

    setupPhotoInputs() {
        // Find all file inputs that accept images
        const photoInputs = document.querySelectorAll('input[type="file"][name*="photo"], input[type="file"][accept*="image"]');
        
        photoInputs.forEach(input => {
            this.setupInput(input);
        });
    }

    setupInput(input) {
        // Set accept attribute if not already set
        if (!input.hasAttribute('accept')) {
            input.setAttribute('accept', 'image/*');
        }

        // Find the associated preview box
        const previewBox = this.findPreviewBox(input);
        
        if (!previewBox) {
            return;
        }

        // Setup file input change event
        input.addEventListener('change', (e) => {
            this.handleFileSelect(e, previewBox);
        });

        // Setup drag and drop
        if (previewBox) {
            this.setupDragAndDrop(input, previewBox);
        }
    }

    findPreviewBox(input) {
        // Try to find the photo preview box near the input
        let previewBox = document.getElementById('photoPreview');
        
        if (!previewBox) {
            // Look for it in the same form section
            const formField = input.closest('.form-fields, .photo-upload-wrapper');
            if (formField) {
                previewBox = formField.querySelector('.photo-preview-box');
            }
        }
        
        if (!previewBox) {
            // Look for it in the parent container
            const container = input.closest('.photo-upload-container, .photo-preview-wrapper');
            if (container) {
                previewBox = container.querySelector('.photo-preview-box');
            }
        }

        return previewBox;
    }

    handleFileSelect(e, previewBox) {
        const file = e.target.files[0];
        
        if (!file) {
            return;
        }

        // Validate file type
        if (!this.acceptedTypes.includes(file.type) && !file.type.startsWith('image/')) {
            this.showError(previewBox, 'Veuillez sélectionner une image uniquement (JPG, PNG, WebP, GIF)');
            e.target.value = '';
            return;
        }

        // Validate file size
        if (file.size > this.maxSize) {
            const maxMb = Math.round(this.maxSize / (1024 * 1024));
            this.showError(previewBox, `L'image doit faire moins de ${maxMb} MB`);
            e.target.value = '';
            return;
        }

        // Create preview
        this.createPreview(file, previewBox, e.target);
    }

    createPreview(file, previewBox, input) {
        const reader = new FileReader();
        
        reader.onload = (e) => {
            previewBox.innerHTML = `
                <img src="${e.target.result}" alt="Aperçu de la photo" 
                     style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;">
            `;
            
            // Update border and styling to indicate success
            previewBox.style.borderColor = 'rgba(59, 130, 246, 0.5)';
            previewBox.style.background = 'rgba(59, 130, 246, 0.08)';
        };
        
        reader.onerror = () => {
            this.showError(previewBox, 'Erreur lors de la lecture du fichier');
            input.value = '';
        };
        
        reader.readAsDataURL(file);
    }

    setupDragAndDrop(input, previewBox) {
        const container = previewBox.closest('.photo-upload-container, .photo-preview-wrapper');
        
        if (!container) {
            return;
        }

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        // Highlight drop area when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            container.addEventListener(eventName, () => {
                container.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            container.addEventListener(eventName, () => {
                container.classList.remove('drag-over');
            }, false);
        });

        // Handle dropped files
        container.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                input.files = files;
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            }
        }, false);
    }

    showError(previewBox, message) {
        alert(message);
        
        // Optional: Add error state to preview box
        previewBox.style.borderColor = 'rgba(248, 113, 113, 0.5)';
        previewBox.style.background = 'rgba(248, 113, 113, 0.08)';
        
        // Reset after 2 seconds
        setTimeout(() => {
            previewBox.style.borderColor = 'rgba(139, 92, 246, 0.3)';
            previewBox.style.background = 'rgba(139, 92, 246, 0.05)';
        }, 2000);
    }
}

// Auto-initialize on document load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new PhotoUploadHandler();
    });
} else {
    new PhotoUploadHandler();
}
