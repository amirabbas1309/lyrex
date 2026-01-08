// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    // مدیریت پاپ‌آپ تبلیغاتی (فقط در صفحه اصلی)
    function initPopup() {
        const isIndexPage = window.location.pathname.includes('index.html') || 
                           window.location.pathname === '/' || 
                           window.location.pathname.endsWith('/');
        
        if (!isIndexPage) return;
        
        const popupModal = document.getElementById('popupModal');
        const popupClose = document.getElementById('popupClose');
        const timerElement = document.getElementById('timer');
        
        if (!popupModal) return;
        
        // چک کردن کوکی برای نمایش یکباره
        if (localStorage.getItem('popupShown')) {
            return;
        }
        
        // نمایش پاپ‌آپ بعد از 1 ثانیه
        setTimeout(() => {
            popupModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
            
            // ذخیره کوکی
            localStorage.setItem('popupShown', 'true');
            
            // تایمر خودکار
            let timeLeft = 8;
            const timerInterval = setInterval(() => {
                timeLeft--;
                if (timerElement) {
                    timerElement.textContent = timeLeft;
                }
                
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    popupModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            }, 1000);
            
            // نمایش دکمه بستن بعد از 3 ثانیه
            setTimeout(() => {
                if (popupClose) {
                    popupClose.style.opacity = '1';
                }
            }, 3000);
            
            // بستن با کلیک روی دکمه
            if (popupClose) {
                popupClose.addEventListener('click', () => {
                    clearInterval(timerInterval);
                    popupModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                });
            }
            
            // بستن با کلیک روی پس‌زمینه
            popupModal.addEventListener('click', (e) => {
                if (e.target === popupModal) {
                    clearInterval(timerInterval);
                    popupModal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            });
            
        }, 1000);
    }
    
    // اجرای پاپ‌آپ
    initPopup();
    
    // مدیریت مینی صفحه ارتباط با تیم
    function initContactModal() {
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
    }
    
    // اجرای مینی صفحه ارتباطی
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
                
                // بستن منو در موبایل
                if (navMenu) {
                    navMenu.classList.remove('active');
                }
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
        
        @keyframes modalSlideIn {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes neonWarning {
            0% {
                border-color: var(--neon-red);
                box-shadow: 0 0 10px var(--neon-red),
                            inset 0 0 10px rgba(255, 0, 0, 0.1);
            }
            50% {
                border-color: var(--neon-blue);
                box-shadow: 0 0 15px var(--neon-blue),
                            inset 0 0 15px rgba(0, 128, 255, 0.1);
            }
            100% {
                border-color: var(--neon-purple);
                box-shadow: 0 0 20px var(--neon-purple),
                            inset 0 0 20px rgba(255, 0, 255, 0.1);
            }
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
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
            const servicesLink = document.querySelector('a[href="#services"]');
            if (servicesLink) {
                servicesLink.click();
            }
        }
        
        // Escape to close mobile menu and modals
        if (e.key === 'Escape') {
            // بستن منوی موبایل
            if (navMenu) {
                navMenu.classList.remove('active');
            }
            
            // بستن مینی صفحه ارتباط با تیم
            const contactModal = document.getElementById('teamContactModal');
            if (contactModal && contactModal.style.display === 'flex') {
                contactModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
            
            // بستن پاپ‌آپ تبلیغاتی
            const popupModal = document.getElementById('popupModal');
            if (popupModal && popupModal.style.display === 'flex') {
                popupModal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        }
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navMenu && navMenu.classList.contains('active') && 
            !navMenu.contains(e.target) && 
            !mobileMenuBtn.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });
    
    // Initialize animations
    animateCounters();
});
