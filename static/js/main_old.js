// Personal Website JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Navbar background change on scroll
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-white', 'shadow');
            } else {
                navbar.classList.remove('bg-white', 'shadow');
            }
        });
    }

    // Fade-in animation for elements with fade-in-text class
    function animateFadeInElements() {
        const fadeElements = document.querySelectorAll('.fade-in-text');

        fadeElements.forEach(element => {
            const delay = parseFloat(element.getAttribute('data-delay')) || 0;

            setTimeout(() => {
                element.classList.add('animate');
            }, delay * 1000);
        });
    }

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe all sections and cards
    const animatedElements = document.querySelectorAll('.section, .project-card, .skill-category');
    animatedElements.forEach(el => observer.observe(el));

    // Skills proficiency bars animation
    const skillBars = document.querySelectorAll('.proficiency-fill');
    skillBars.forEach(bar => {
        const proficiency = bar.getAttribute('data-proficiency');
        if (proficiency) {
            setTimeout(() => {
                bar.style.width = proficiency + '%';
            }, 500);
        }
    });

    // Contact form validation and submission
    const contactForm = document.querySelector('#contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Basic validation
            const name = this.querySelector('[name="name"]').value.trim();
            const email = this.querySelector('[name="email"]').value.trim();
            const subject = this.querySelector('[name="subject"]').value.trim();
            const message = this.querySelector('[name="message"]').value.trim();

            if (!name || !email || !subject || !message) {
                showAlert('Please fill in all fields.', 'danger');
                return;
            }

            if (!isValidEmail(email)) {
                showAlert('Please enter a valid email address.', 'danger');
                return;
            }

            // Simulate form submission (replace with actual AJAX call)
            showAlert('Sending message...', 'info');

            // In a real application, you would send the data via AJAX
            setTimeout(() => {
                showAlert('Message sent successfully!', 'success');
                this.reset();
            }, 2000);
        });
    }

    // Project filtering (if implemented)
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            const filter = this.getAttribute('data-filter');

            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');

            // Filter projects
            projectCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Initialize fade-in animations
    animateFadeInElements();

    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function () {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Close mobile menu when clicking on a link
    const mobileNavLinks = document.querySelectorAll('.navbar-nav .nav-link');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function () {
            if (navbarCollapse.classList.contains('show')) {
                navbarCollapse.classList.remove('show');
            }
        });
    });

    // Typing effect for hero section (optional)
    const heroTitle = document.querySelector('.hero h1');
    if (heroTitle && heroTitle.textContent) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';

        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };

        // Start typing effect after a short delay
        setTimeout(typeWriter, 500);
    }
});

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert alert at the top of the page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Auto-remove alert after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Add loading animation for images
function preloadImages() {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        const src = img.getAttribute('data-src');
        if (src) {
            const newImg = new Image();
            newImg.onload = function () {
                img.src = src;
                img.classList.add('fade-in');
            };
            newImg.src = src;
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', preloadImages);
} else {
    preloadImages();
}

// Timeline Animation
function animateTimeline() {
    const timelineItems = document.querySelectorAll('.timeline .timeline-item');

    timelineItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            item.style.transition = 'all 0.6s ease';

            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 100);
        }, index * 200);
    });
}

// Skill Progress Bar Animation
function animateSkillProgress() {
    const progressBars = document.querySelectorAll('.skill-progress .progress-bar');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target;
                const width = progressBar.style.width;
                progressBar.style.width = '0%';

                setTimeout(() => {
                    progressBar.style.width = width;
                }, 300);

                observer.unobserve(progressBar);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => observer.observe(bar));
}

// Research Area Cards Animation
function animateResearchCards() {
    const researchCards = document.querySelectorAll('.research-area-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(30px)';
                entry.target.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    researchCards.forEach(card => observer.observe(card));
}

// Project Cards Animation
function animateProjectCards() {
    const projectCards = document.querySelectorAll('.project-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'scale(0.9)';
                entry.target.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'scale(1)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    projectCards.forEach(card => observer.observe(card));
}

// Contact Info Cards Animation
function animateContactCards() {
    const contactCards = document.querySelectorAll('.contact-info-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    contactCards.forEach(card => observer.observe(card));
}

// Collaboration Cards Animation
function animateCollaborationCards() {
    const collaborationCards = document.querySelectorAll('.collaboration-type-card');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'rotateY(15deg)';
                entry.target.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'rotateY(0deg)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    collaborationCards.forEach(card => observer.observe(card));
}

// Enhanced Tooltip System
function initializeEnhancedTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');

    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = document.createElement('div');
            tooltip.className = 'enhanced-tooltip';
            tooltip.textContent = e.target.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0,0,0,0.9);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.9rem;
                z-index: 1000;
                max-width: 250px;
                white-space: nowrap;
                pointer-events: none;
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.3s ease;
            `;

            document.body.appendChild(tooltip);

            const rect = e.target.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.bottom + 10 + 'px';

            setTimeout(() => {
                tooltip.style.opacity = '1';
                tooltip.style.transform = 'translateY(0)';
            }, 10);

            element._tooltip = tooltip;
        });

        element.addEventListener('mouseleave', () => {
            if (element._tooltip) {
                element._tooltip.style.opacity = '0';
                element._tooltip.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    if (element._tooltip && element._tooltip.parentNode) {
                        element._tooltip.parentNode.removeChild(element._tooltip);
                    }
                    element._tooltip = null;
                }, 300);
            }
        });
    });
}

// Page-specific animations
function initializePageAnimations() {
    const currentPage = window.location.pathname;

    if (currentPage.includes('/about/')) {
        animateTimeline();
    }

    if (currentPage.includes('/skills/')) {
        animateSkillProgress();
    }

    if (currentPage.includes('/projects/')) {
        animateResearchCards();
        animateProjectCards();
    }

    if (currentPage.includes('/contact/')) {
        animateContactCards();
        animateCollaborationCards();
    }
}

// Enhanced scroll animations for new elements
function enhanceScrollAnimations() {
    const newElements = document.querySelectorAll('.skill-category-card, .method-card, .methodology-card, .highlight-item');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(30px)';
                entry.target.style.transition = 'all 0.6s ease';

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    newElements.forEach(element => observer.observe(element));
}

// Animate hobbies section elements
function animateHobbiesSection() {
    const hobbyCards = document.querySelectorAll('.hobby-card');
    const hobbyImage = document.querySelector('.hobby-image-container');

    if (hobbyCards.length > 0 || hobbyImage) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    if (entry.target.classList.contains('hobby-card')) {
                        entry.target.style.opacity = '0';
                        entry.target.style.transform = 'translateX(-30px)';
                        entry.target.style.transition = 'all 0.6s ease';

                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'translateX(0)';
                        }, 200);
                    } else if (entry.target.classList.contains('hobby-image-container')) {
                        entry.target.style.opacity = '0';
                        entry.target.style.transform = 'scale(0.9)';
                        entry.target.style.transition = 'all 0.8s ease';

                        setTimeout(() => {
                            entry.target.style.opacity = '1';
                            entry.target.style.transform = 'scale(1)';
                        }, 400);
                    }

                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        hobbyCards.forEach(card => observer.observe(card));
        if (hobbyImage) observer.observe(hobbyImage);
    }
}

// Initialize all new functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    // ... existing initialization code ...

    // Initialize new animations and interactions
    initializePageAnimations();
    enhanceScrollAnimations();
    initializeEnhancedTooltips();
    animateHobbiesSection();

    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Enhanced form validation for contact form
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const requiredFields = contactForm.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    field.style.borderColor = '#28a745';
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger mt-3';
                errorDiv.textContent = 'Please fill in all required fields.';
                contactForm.appendChild(errorDiv);

                setTimeout(() => {
                    if (errorDiv.parentNode) {
                        errorDiv.parentNode.removeChild(errorDiv);
                    }
                }, 3000);
            }
        });
    }
});
