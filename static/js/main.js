// ========== INICIALIZACIÓN ========== //
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeFavorites();
    initializeSearch();
    initializeAnimations();
    initializeImageLazyLoading();
    initializeFormValidation();
});

// ========== TOOLTIPS ========== //
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ========== SISTEMA DE FAVORITOS ========== //
function initializeFavorites() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const recetaId = this.dataset.id;
            toggleFavorite(recetaId, this);
        });
    });
}

function toggleFavorite(recetaId, button) {
    // Agregar clase de loading
    button.classList.add('loading');
    
    fetch(`/ajax/toggle-favorito/${recetaId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const icon = button.querySelector('i');
            if (data.es_favorita) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                button.classList.add('active');
                button.style.color = '#e74c3c';
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                button.classList.remove('active');
                button.style.color = '';
            }
            
            // Mostrar notificación
            showNotification(data.mensaje, 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al actualizar favorito', 'error');
    })
    .finally(() => {
        button.classList.remove('loading');
    });
}

// ========== BÚSQUEDA EN TIEMPO REAL ========== //
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    let searchTimeout;
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                hideSearchResults();
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
        
        // Ocultar resultados al hacer clic fuera
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults?.contains(e.target)) {
                hideSearchResults();
            }
        });
        
        // Manejar teclas de navegación
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                hideSearchResults();
                this.blur();
            }
        });
    }
}

function performSearch(query) {
    fetch(`/ajax/busqueda/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.recetas);
        })
        .catch(error => {
            console.error('Error en búsqueda:', error);
            showNotification('Error en la búsqueda', 'error');
        });
}

function displaySearchResults(recetas) {
    let searchResults = document.getElementById('search-results');
    
    if (!searchResults) {
        searchResults = document.createElement('div');
        searchResults.id = 'search-results';
        searchResults.className = 'search-results';
        const searchContainer = document.querySelector('.search-bar-container');
        if (searchContainer) {
            searchContainer.appendChild(searchResults);
        }
    }
    
    if (recetas.length === 0) {
        searchResults.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>No se encontraron recetas</p>
            </div>
        `;
    } else {
        searchResults.innerHTML = recetas.map(receta => `
            <div class="search-result-item" onclick="window.location.href='${receta.url}'">
                <img src="${receta.imagen_url}" alt="${receta.titulo}" class="search-result-image">
                <div class="search-result-content">
                    <h4 class="search-result-title">${receta.titulo}</h4>
                    <p class="search-result-description">${receta.descripcion_corta}</p>
                    <div class="search-result-meta">
                        <span class="time"><i class="fas fa-clock"></i> ${receta.tiempo_preparacion} min</span>
                        <span class="difficulty">${receta.dificultad}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    searchResults.style.display = 'block';
}

function hideSearchResults() {
    const searchResults = document.getElementById('search-results');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// ========== ANIMACIONES ========== //
function initializeAnimations() {
    // Animación de entrada para elementos
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observar elementos que necesitan animación
    document.querySelectorAll('.recipe-card-featured, .feature-card, .category-card').forEach(card => {
        observer.observe(card);
    });
    
    // Animación de hover para botones
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.classList.contains('loading')) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Parallax suave en hero
    const hero = document.querySelector('.hero-section');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
}

// ========== LAZY LOADING DE IMÁGENES ========== //
function initializeImageLazyLoading() {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ========== VALIDACIÓN DE FORMULARIOS ========== //
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Mostrar errores específicos
                const invalidFields = form.querySelectorAll(':invalid');
                if (invalidFields.length > 0) {
                    invalidFields[0].focus();
                    showNotification('Por favor, corrige los errores en el formulario', 'warning');
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Validación en tiempo real
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

// ========== NOTIFICACIONES ========== //
function showNotification(message, type = 'info', duration = 5000) {
    const container = getNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span class="notification-message">${message}</span>
            <button class="notification-close" onclick="hideNotification(this.parentElement)">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Mostrar notificación con animación
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Ocultar automáticamente
    setTimeout(() => {
        hideNotification(notification);
    }, duration);
    
    return notification;
}

function hideNotification(notification) {
    notification.classList.remove('show');
    setTimeout(() => {
        if (notification.parentElement) {
            notification.parentElement.removeChild(notification);
        }
    }, 300);
}

function getNotificationContainer() {
    let container = document.getElementById('notification-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.className = 'notification-container';
        document.body.appendChild(container);
    }
    return container;
}

function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

// ========== MODAL HELPERS ========== //
function showModal(modalId, content = null) {
    const modal = document.getElementById(modalId);
    if (modal) {
        if (content) {
            const modalBody = modal.querySelector('.modal-body');
            if (modalBody) {
                modalBody.innerHTML = content;
            }
        }
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide();
        }
    }
}

// ========== UTILIDADES ========== //
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ========== MANEJO DE ERRORES ========== //
window.addEventListener('error', function(e) {
    console.error('Error global capturado:', e.error);
    // No mostrar notificación al usuario para errores de JavaScript, solo loggear
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rechazada:', e.reason);
    // Mostrar notificación solo para errores críticos
    if (e.reason && e.reason.message && e.reason.message.includes('Network')) {
        showNotification('Error de conexión. Verifica tu conexión a internet.', 'error');
    }
});

// ========== NAVEGACIÓN SUAVE ========== //
function smoothScrollTo(elementId, offset = 100) {
    const element = document.getElementById(elementId);
    if (element) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;
        
        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}

// ========== SHARED STATE ========== //
const AppState = {
    currentUser: null,
    favorites: new Set(),
    searchQuery: '',
    currentPage: 1,
    
    addFavorite(recetaId) {
        this.favorites.add(parseInt(recetaId));
    },
    
    removeFavorite(recetaId) {
        this.favorites.delete(parseInt(recetaId));
    },
    
    isFavorite(recetaId) {
        return this.favorites.has(parseInt(recetaId));
    }
};

// ========== EXPORTAR FUNCIONES GLOBALES ========== //
window.toggleFavorite = toggleFavorite;
window.showNotification = showNotification;
window.hideNotification = hideNotification;
window.showModal = showModal;
window.hideModal = hideModal;
window.smoothScrollTo = smoothScrollTo;
