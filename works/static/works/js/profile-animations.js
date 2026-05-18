// Анимация появления элементов при скролле
document.addEventListener('DOMContentLoaded', function() {
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOnScroll = function() {
      revealElements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
          element.classList.add('active');
        }
      });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Проверить при загрузке
    
    // Анимация чисел
    const animateNumbers = function() {
      const numberElements = document.querySelectorAll('.num');
      
      numberElements.forEach(element => {
        const target = parseInt(element.getAttribute('data-count')) || 0;
        const duration = 2000; // 2 секунды
        const step = Math.ceil(target / (duration / 16)); // 60fps
        let current = 0;
        
        const timer = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          element.textContent = current.toLocaleString();
        }, 16);
      });
    };
    
    // Запустить анимацию чисел, когда элементы станут видимыми
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateNumbers();
          observer.disconnect();
        }
      });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('.profile-stats-grid');
    if (statsSection) {
      observer.observe(statsSection);
    }
    
    // Инициализация прогресс-баров
    initProgressBars();
  });
  
  // Инициализация прогресс-баров
  function initProgressBars() {
    const progressElements = document.querySelectorAll('[data-progress], [data-width]');
    
    progressElements.forEach(element => {
      const progressValue = element.getAttribute('data-progress') || element.getAttribute('data-width');
      const progress = Math.min(100, Math.max(0, progressValue));
      
      if (element.tagName === 'circle') {
        // Для кругового прогресса
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (progress / 100) * circumference;
        element.style.strokeDashoffset = offset;
        element.setAttribute('stroke-dasharray', circumference);
      } else {
        // Для линейного прогресса
        element.style.width = `${progress}%`;
      }
    });
  }
  
  // Обновление данных профиля (пример)
  function updateProfileData(data) {
    // Обновление текстовых данных
    document.querySelector('[data-bind="full_name"]').textContent = data.full_name;
    document.querySelector('[data-bind="username"]').textContent = data.username;
    document.querySelector('[data-bind="email"]').textContent = data.email;
    document.querySelector('[data-bind="joined"]').textContent = data.joined;
    document.querySelector('[data-bind="level"]').textContent = data.level;
    document.querySelector('[data-bind="current_xp"]').textContent = data.current_xp;
    document.querySelector('[data-bind="next_level_xp"]').textContent = data.next_level_xp;
    
    // Обновление числовых данных
    document.querySelector('[data-bind-num="total_score"]').setAttribute('data-count', data.total_score);
    document.querySelector('[data-bind-num="completed_works"]').setAttribute('data-count', data.completed_works);
    document.querySelector('[data-bind-num="streak_days"]').setAttribute('data-count', data.streak_days);
    document.querySelector('[data-bind-num="success_rate"]').setAttribute('data-count', data.success_rate);
    
    // Обновление прогресса
    document.querySelector('[data-progress]').setAttribute('data-progress', data.level_progress);
    document.querySelector('[data-width]').setAttribute('data-width', data.level_progress);
    
    // Переинициализация прогресс-баров
    initProgressBars();
  }