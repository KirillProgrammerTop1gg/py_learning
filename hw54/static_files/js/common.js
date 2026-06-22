// TechBlog Глобальний JS файл
document.addEventListener('DOMContentLoaded', () => {
    console.log('⚡ TechBlog loaded successfully with minimalistic black-and-yellow styling!');
    
    // Можна додати плавні переходи або ефекти при прокрутці сторінки
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.style.padding = '12px 0';
                navbar.style.background = 'rgba(10, 10, 12, 0.95)';
                navbar.style.borderBottomColor = 'var(--accent)';
            } else {
                navbar.style.padding = '20px 0';
                navbar.style.background = 'rgba(10, 10, 12, 0.8)';
                navbar.style.borderBottomColor = 'var(--border-color)';
            }
        });
    }
});
