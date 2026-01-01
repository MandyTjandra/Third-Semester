document.addEventListener('DOMContentLoaded', function () {

    // =================================================================
    // KONTROL INISIALISASI SKRIP
    // =================================================================
    const isMainPage = document.querySelector('.hero') !== null;
    const isMateriPage = document.querySelector('.materi-wrapper') !== null;
    const isAuthPage = document.querySelector('.auth-body') !== null;

    // Fitur Global (berjalan di semua halaman)
    initThemeToggle();
    initMobileMenu(); // ✅ Sekarang aman dipanggil karena fungsinya sudah ada di global scope

    // Fitur untuk halaman utama dan materi (halaman yang panjang)
    if (isMainPage || isMateriPage) {
        initNavbarShadow();
        initScrollToTop();
        initScrollProgressBar();
    }

    // Fitur khusus halaman utama
    if (isMainPage) {
        initFadeInOnScroll();
    }

    // Fitur untuk halaman login/register
    if (isAuthPage) {
        initAuthForms();
    }
});


// =================================================================
// [BARU] FUNGSI UNTUK MENU MOBILE (HAMBURGER)
// =================================================================
function initMobileMenu() {
    const menuToggle = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.navbar nav');

    // Cek apakah elemen ada (untuk menghindari error di halaman tanpa navbar)
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function () {
            // Toggle class 'active' untuk menu (muncul/hilang)
            navMenu.classList.toggle('active');
            
            // Toggle class 'is-active' untuk animasi tombol hamburger (jadi X)
            this.classList.toggle('is-active');
        });

        // Opsional: Tutup menu saat salah satu link diklik agar tidak menutupi layar
        const navLinks = document.querySelectorAll('.navbar nav a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('is-active');
            });
        });
    }
}


// =================================================================
// FUNGSI UNTUK FORM LOGIN & REGISTER
// =================================================================
function initAuthForms() {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Selalu cegah submit default

            const password = document.getElementById('reg-password');
            const confirmPassword = document.getElementById('reg-password-confirm');

            if (password.value !== confirmPassword.value) {
                showNotification('Password dan Konfirmasi Password tidak cocok!', 'error'); 
            } else {
                showNotification('Registrasi berhasil! ✨', 'info');
                // Di aplikasi nyata, di sini Anda akan mengirim data ke server
                // registerForm.submit(); 
            }
        });
    }

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            showNotification('Login berhasil! Selamat datang kembali. 👋', 'info');
            // Logika login ke server
        });
    }
}


// =================================================================
// SISTEM NOTIFIKASI
// =================================================================
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    const style = document.createElement('style');
    document.head.appendChild(style);
    style.sheet.insertRule(`.notification { position: fixed; bottom: -100px; left: 50%; transform: translateX(-50%); min-width: 280px; text-align: center; padding: 15px 20px; border-radius: 8px; color: #fff; font-family: 'Poppins', sans-serif; font-size: 0.9rem; z-index: 2000; box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: all 0.5s ease-in-out; }`, 0);
    style.sheet.insertRule('.notification.info { background-color: #0c508a; }', 1);
    style.sheet.insertRule('.notification.error { background-color: #c0392b; }', 2);
    style.sheet.insertRule('.notification.show { bottom: 20px; }', 3);

    document.body.appendChild(notification);

    setTimeout(() => { notification.classList.add('show'); }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => { notification.remove(); style.remove(); }, 500);
    }, 3000);
}


// =================================================================
// FUNGSI-FUNGSI VISUAL
// =================================================================

function initFadeInOnScroll() {
    const animatedContainers = document.querySelectorAll('.course-info .container, .topic-grid, .quote-section');
    if (animatedContainers.length === 0) return;

    const style = document.createElement('style');
    style.textContent = `.fade-in-child { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease-out, transform 0.6s ease-out; } .fade-in-child.visible { opacity: 1; transform: translateY(0); }`;
    document.head.appendChild(style);

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const children = entry.target.querySelectorAll('.info-card, .topic-card');
                if (children.length > 0) {
                    children.forEach((child, index) => {
                        child.classList.add('fade-in-child');
                        child.style.transitionDelay = `${index * 100}ms`;
                        child.classList.add('visible');
                    });
                } else {
                    entry.target.classList.add('fade-in-child');
                    entry.target.classList.add('visible');
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    animatedContainers.forEach(el => observer.observe(el));
}

function initScrollProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress-bar';
    document.body.prepend(progressBar);
    window.addEventListener('scroll', () => {
        const totalHeight = document.body.scrollHeight - window.innerHeight;
        const progress = (window.pageYOffset / totalHeight) * 100;
        progressBar.style.width = `${progress}%`;
    });
}

function initScrollToTop() {
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollTopBtn.className = 'scroll-to-top';
    document.body.appendChild(scrollTopBtn);
    
    // Pastikan style tombol ini tidak konflik dengan CSS utama
    const style = document.createElement('style');
    style.textContent = `
        body.dark-mode .scroll-to-top { background-color: #16213e; color: #64b5f6; } 
        .scroll-to-top { position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px; background-color: #007bff; color: white; border: none; border-radius: 50%; cursor: pointer; font-size: 1.2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); z-index: 998; opacity: 0; visibility: hidden; transform: translateY(20px); transition: all 0.3s ease; } 
        .scroll-to-top.show { opacity: 1; visibility: visible; transform: translateY(0); } 
        .scroll-to-top:hover { background-color: #0056b3; transform: translateY(-5px); }
    `;
    document.head.appendChild(style);
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) { scrollTopBtn.classList.add('show'); } else { scrollTopBtn.classList.remove('show'); }
    });
    scrollTopBtn.addEventListener('click', () => { window.scrollTo({ top: 0, behavior: 'smooth' }); });
}

function initNavbarShadow() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) { navbar.classList.add('scrolled'); } else { navbar.classList.remove('scrolled'); }
    });
}

function initThemeToggle() {
    const themeToggle = document.createElement('button');
    themeToggle.className = 'theme-toggle';
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.setAttribute('aria-label', 'Toggle dark mode');
    document.body.appendChild(themeToggle);

    const themeStyle = document.createElement('style');
    themeStyle.textContent = `
        /* --- 1. ATURAN DASAR DARK MODE --- */
        body.dark-mode { background-color: #1a1a2e; color: #e0e0e0; }
        body.dark-mode h1, body.dark-mode h2, body.dark-mode h3, body.dark-mode h4 { color: #ffffff; }
        body.dark-mode a { color: #64b5f6; }
        body.dark-mode .logo { color: #64b5f6; }
        /* --- 2. GAYA HALAMAN UTAMA (index.html) --- */
        body.dark-mode .navbar, body.dark-mode .course-info, body.dark-mode .topics, body.dark-mode .quote-section { background-color: transparent; }
        body.dark-mode .navbar a { color: #e0e0e0; }
        body.dark-mode a.btn-primary { color: #0056b3; }
        body.dark-mode .navbar.scrolled { background-color: #16213e; }
        body.dark-mode .hero p { color: #c7d2fe; }
        body.dark-mode .info-card, body.dark-mode .topic-card { background-color: #16213e; box-shadow: 0 5px 25px rgba(255, 255, 255, 0.08); }
        body.dark-mode .info-card:hover, body.dark-mode .topic-card:hover { box-shadow: 0 8px 30px rgba(255, 255, 255, 0.12); }
        body.dark-mode .info-card p, body.dark-mode .topic-card p, body.dark-mode .footer p { color: #a2b3c7 !important; }
        body.dark-mode .info-card h3 { color: #ffffff; }
        body.dark-mode .topic-card h3 { color: #64b5f6; }
        body.dark-mode .quote-section blockquote, body.dark-mode .quote-section blockquote footer { color: #e0e0e0; border-color: #64b5f6; }
        body.dark-mode .footer { background-color: #16213e; }
        /* --- 3. GAYA HALAMAN MATERI (html.html, dll.) --- */
        body.dark-mode .materi-body { background-color: #1a1a2e; }
        body.dark-mode .materi-wrapper .container { background-color: transparent; box-shadow: none; }
        body.dark-mode .materi-header { background-color: #0f3460; }
        body.dark-mode .materi-content { background-color: #16213e; box-shadow: none; }
        body.dark-mode .back-to-home-dark { color: #64b5f6; }
        body.dark-mode .materi-content h2 { border-bottom-color: #64b5f6; }
        body.dark-mode .materi-content code { background-color: #0f3460; color: #a2b3c7; }
        body.dark-mode .materi-content pre { background-color: #0f3460; color: #f0f0f0; }
        body.dark-mode .output { background-color: #1a1a2e; border-color: #0f3460; }
        body.dark-mode .output, body.dark-mode .output p, body.dark-mode .output li, body.dark-mode .image-caption { color: #e0e0e0 !important; }
        body.dark-mode .output th { background-color: #0f3460; }
        body.dark-mode .output th, body.dark-mode .output td { border-color: #3b4a6b; }
        body.dark-mode .more-info { background-color: #16213e; border-left-color: #64b5f6; }
        body.dark-mode .more-info h3 { color: #64b5f6; }
        /* --- 4. GAYA HALAMAN LOGIN/REGISTER --- */
        body.dark-mode .auth-body { background: #1a1a2e; }
        body.dark-mode .back-to-home { color: #e0e0e0; }
        body.dark-mode .form-container { background-color: #16213e; }
        body.dark-mode .auth-form h2, body.dark-mode .form-group label { color: #ffffff; }
        body.dark-mode .form-group input { background-color: #0f3460; color: #e0e0e0; border-color: #3b4a6b; }
        body.dark-mode .form-switch-link { color: #a2b3c7; }
        /* --- 5. GAYA TOMBOL TOGGLE & LAINNYA --- */
        .theme-toggle { position: fixed; bottom: 30px; left: 30px; width: 50px; height: 50px; background-color: #fff; color: #333; border: 2px solid #e9ecef; border-radius: 50%; cursor: pointer; font-size: 1.2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); transition: all 0.3s ease; z-index: 999; }
        .theme-toggle:hover { transform: translateY(-5px) rotate(15deg); }
        body.dark-mode .theme-toggle { background-color: #16213e; color: #ffd700; border-color: #0f3460; }
    `;
    document.head.appendChild(themeStyle);

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    themeToggle.addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');

        if (isDark) {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
            showNotification('🌙 Mode gelap aktif', 'info');
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
            showNotification('☀️ Mode terang aktif', 'info');
        }
    });
}