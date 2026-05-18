
// ===== ИНТЕРАКТИВНОСТЬ ПРОФИЛЯ =====
document.addEventListener('DOMContentLoaded', function() {
    // Анимация счетчиков
    animateCounters();
    
    // Эффекты при наведении
    addHoverEffects();
    
    // Анимация прогресс-баров
    animateProgressBars();
    
    // Эффект печати для статистики
    typewriterEffect();
});

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, 16);
    });
}

function addHoverEffects() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
        });
    });
}

function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

function typewriterEffect() {
    const elements = document.querySelectorAll('.stat-number');
    
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.5s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
    });
}

// Эффект частиц для главной статистики
function createParticles() {
    const mainStat = document.querySelector('.stat-card.main-stat');
    if (!mainStat) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = 
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(255,255,255,0.6);
            border-radius: 50%;
            pointer-events: none;
            animation: float s infinite ease-in-out;
            left: %;
            top: %;
        ;
        
        mainStat.appendChild(particle);
    }
}

// CSS для частиц
const style = document.createElement('style');
style.textContent = 
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 1; }
        50% { transform: translateY(-20px) rotate(180deg); opacity: 0.5; }
    }
;
document.head.appendChild(style);

// Запускаем эффект частиц
setTimeout(createParticles, 1000);

