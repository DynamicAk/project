// Mobile Navigation Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }));
}

// Smooth Scrolling
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

// Testimonials Carousel
let currentSlide = 0;
const slides = document.querySelectorAll('.testimonial-slide');
const dots = document.querySelectorAll('.dot');

if (slides.length > 0 && dots.length > 0) {
    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        slides[index].classList.add('active');
        dots[index].classList.add('active');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    // Auto-advance carousel
    setInterval(nextSlide, 5000);

    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            showSlide(currentSlide);
        });
    });
}

// Header Background on Scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, observerOptions);

// Observe all sections
document.querySelectorAll('section').forEach(section => {
    observer.observe(section);
});

// Flash Messages Auto-close
function closeAlert(id) {
    const alert = document.getElementById(id);
    if (alert) {
        alert.style.opacity = '0';
        setTimeout(() => {
            alert.remove();
        }, 300);
    }
}

// Auto-close flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        setTimeout(() => {
            if (alert && alert.parentElement) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000 + (index * 500)); // Stagger the auto-close
    });
});

// Contact Form Submission
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                showAlert('success', 'Message sent successfully! We\'ll get back to you soon.');
                this.reset();
            } else {
                showAlert('error', 'Failed to send message. Please try again.');
            }
        } catch (error) {
            showAlert('error', 'Network error. Please check your connection and try again.');
        }
    });
}

// Event Registration Functions
async function registerForEvent(eventId) {
    try {
        const response = await fetch(`/api/register/${eventId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('success', data.message);
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('error', data.error);
        }
    } catch (error) {
        showAlert('error', 'Registration failed. Please try again.');
    }
}

async function unregisterFromEvent(eventId) {
    if (!confirm('Are you sure you want to unregister from this event?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/unregister/${eventId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('success', data.message);
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('error', data.error);
        }
    } catch (error) {
        showAlert('error', 'Unregistration failed. Please try again.');
    }
}

// Show Alert Function
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button type="button" class="close-alert" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    let flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        flashContainer = document.createElement('div');
        flashContainer.className = 'flash-messages';
        document.body.insertBefore(flashContainer, document.querySelector('main'));
    }
    
    flashContainer.appendChild(alertDiv);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            alertDiv.style.opacity = '0';
            setTimeout(() => {
                if (alertDiv.parentElement) {
                    alertDiv.remove();
                }
            }, 300);
        }
    }, 4000);
}

// Load Events Dynamically
async function loadEvents() {
    try {
        const response = await fetch('/api/events');
        const events = await response.json();
        
        const eventsContainer = document.querySelector('.events-grid');
        if (eventsContainer && events.length > 0) {
            // Update events display
            // This would be implemented based on your specific needs
        }
    } catch (error) {
        console.error('Failed to load events:', error);
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Load events if on events page
    if (window.location.pathname.includes('events') || document.querySelector('.events-grid')) {
        // loadEvents();
    }
    
    // Initialize any other page-specific functionality
    console.log('Sangam Yoga Club website loaded successfully!');
});