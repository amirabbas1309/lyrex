// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
            navMenu.style.flexDirection = 'column';
            navMenu.style.position = 'absolute';
            navMenu.style.top = '100%';
            navMenu.style.right = '0';
            navMenu.style.background = 'rgba(10, 10, 15, 0.95)';
            navMenu.style.backdropFilter = 'blur(10px)';
            navMenu.style.border = '1px solid rgba(255, 255, 255, 0.1)';
            navMenu.style.borderRadius = '10px';
            navMenu.style.padding = '2rem';
            navMenu.style.width = '200px';
            navMenu.style.gap = '1rem';
        });
    }
    
    // مدیریت مینی صفحه ارتباط با تیم (برای همه صفحات)
    const initContactModal = () => {
        const modal = document.getElementById('teamContactModal');
        const closeModalBtn = document.getElementById('closeContactModal');
        const contactTriggers = document.querySelectorAll('.contact-trigger');
        
        if (!modal) return;
        
        // باز کردن مینی صفحه
        contactTriggers.forEach(trigger => {
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });
        
        // بستن مینی صفحه
        if (closeModalBtn) {
            closeModalBtn.addEventListener('click', function() {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }
        
        // بستن با کلیک خارج از مینی صفحه
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
        
        // بستن با کلید Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
        
        // افکت کلیک روی کارت‌ها
        const platformCards = document.querySelectorAll('.platform-card');
        platformCards.forEach(card => {
            card.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.3);
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    z-index: 1;
                `;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    };
    
    // فراخوانی تابع مدیریت مینی صفحه
    initContactModal();
    
    // Animate stats counters
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number[data-count]');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.textContent = Math.floor(current);
                    setTimeout(updateCounter, 16);
                } else {
                    counter.textContent = target;
                }
            };
            
            updateCounter();
        });
    }
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Animate counters when stats section is visible
                if (entry.target.classList.contains('hero-section')) {
                    setTimeout(animateCounters, 500);
                }
            }
        });
    }, observerOptions);
    
    // Observe sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.classList.contains('contact-trigger')) return;
            
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Update active nav link
                document.querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
    
    // RGB hover effect for glass cards
    const glassCards = document.querySelectorAll('.glass-card');
    
    glassCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const colors = ['#ff0000', '#00ff00', '#0080ff', '#ff00ff', '#00ffff', '#ffff00'];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            
            this.style.borderColor = `${randomColor}40`;
            this.style.boxShadow = `0 20px 40px ${randomColor}20`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.borderColor = '';
            this.style.boxShadow = '';
        });
    });
    
    // Add typing effect to hero subtitle (فقط در صفحه اصلی)
    const subtitleElement = document.querySelector('.hero-subtitle');
    if (subtitleElement && !subtitleElement.querySelector('.typing-cursor')) {
        const subtitleText = "توسعه‌دهنده سورس‌های پیشرفته گیمینگ و ربات‌های هوشمند";
        let charIndex = 0;
        
        function typeWriter() {
            if (charIndex < subtitleText.length) {
                subtitleElement.innerHTML = subtitleText.substring(0, charIndex + 1) + 
                    '<span class="typing-cursor">|</span>';
                charIndex++;
                setTimeout(typeWriter, 50);
            } else {
                subtitleElement.innerHTML = subtitleText + 
                    ' <span class="subtitle-glow">با کیفیت حرفه‌ای</span>';
            }
        }
        
        setTimeout(typeWriter, 1000);
    }
    
    // Add CSS for typing cursor
    const style = document.createElement('style');
    style.textContent = `
        .typing-cursor {
            color: var(--rgb-red);
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Parallax effect for background circles
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const circles = document.querySelectorAll('.rgb-circle');
        
        circles.forEach((circle, index) => {
            const speed = 0.5 + (index * 0.1);
            circle.style.transform = `translateY(${scrolled * speed * 0.1}px) rotate(${scrolled * 0.1}deg)`;
        });
    });
    
    // Add download notification
    const downloadButtons = document.querySelectorAll('a[href$=".py"]');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const fileName = this.getAttribute('href').split('/').pop();
            
            // Create notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                left: 20px;
                background: linear-gradient(45deg, #8b0000, #660000);
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                z-index: 10000;
                font-family: 'Vazirmatn', sans-serif;
                font-size: 14px;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 5px 15px rgba(139, 0, 0, 0.5);
                border-right: 4px solid #ffd700;
                animation: slideIn 0.3s ease;
            `;
            
            notification.innerHTML = `
                <i class="fas fa-cloud-download-alt" style="font-size: 18px;"></i>
                <span>در حال دانلود ${fileName}...</span>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    if (notification.parentNode) {
                        document.body.removeChild(notification);
                    }
                }, 500);
            }, 3000);
            
            // Actually download the file
            window.open(this.href, '_blank');
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl + S to search
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            document.querySelector('a[href="#services"]').click();
        }
        
        // Escape to close mobile menu
        if (e.key === 'Escape') {
            navMenu.style.display = 'none';
            const modal = document.getElementById('teamContactModal');
            if (modal && modal.style.display === 'flex') {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }
    });
    
    // Initialize animations
    animateCounters();
});