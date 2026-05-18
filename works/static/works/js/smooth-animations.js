// Плавные анимации для лучшей производительности
(function() {
    'use strict';
    
    // Оптимизация анимаций с использованием requestAnimationFrame
    function optimizeAnimations() {
        // Добавляем класс для GPU ускорения
        const animatedElements = document.querySelectorAll('.work-card, .bar, .fill, .topic-fill, .card');
        animatedElements.forEach(el => {
            el.style.willChange = 'transform, opacity, box-shadow';
        });
        
        // Оптимизируем анимации при скролле
        let ticking = false;
        function updateAnimations() {
            if (!ticking) {
                requestAnimationFrame(() => {
                    // Обновляем анимации только при необходимости
                    ticking = false;
                });
                ticking = true;
            }
        }
        
        window.addEventListener('scroll', updateAnimations, { passive: true });
    }
    
    // Плавная анимация появления элементов
    function animateOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // Наблюдаем за карточками работ
        const workCards = document.querySelectorAll('.work-card');
        workCards.forEach(card => {
            card.style.animationPlayState = 'paused';
            observer.observe(card);
        });
    }
    
    // Оптимизация анимаций при наведении
    function optimizeHoverAnimations() {
        const hoverElements = document.querySelectorAll('.work-card, .bar, .card');
        
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-6px) scale(1.02)';
                this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.1)';
            }, { passive: true });
            
            el.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = 'var(--shadow)';
            }, { passive: true });
        });
    }
    
    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            optimizeAnimations();
            animateOnScroll();
            optimizeHoverAnimations();
        });
    } else {
        optimizeAnimations();
        animateOnScroll();
        optimizeHoverAnimations();
    }
    
    // Оптимизация для мобильных устройств
    if ('ontouchstart' in window) {
        // Отключаем hover эффекты на мобильных
        const style = document.createElement('style');
        style.textContent = `
            @media (hover: none) {
                .work-card:hover,
                .bar:hover,
                .card:hover {
                    transform: none !important;
                    box-shadow: var(--shadow) !important;
                }
            }
        `;
        document.head.appendChild(style);
    }
})();
