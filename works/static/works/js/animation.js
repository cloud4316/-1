(function(){
	// Typewriter для hero
	const codeBlock = document.querySelector('.code-window .window-content pre code');
	if(codeBlock){
		const full = codeBlock.textContent;
		codeBlock.textContent = '';
		const cursor = document.createElement('span');
		cursor.className = 'tw-cursor';
		cursor.textContent = '▌';
		codeBlock.parentElement.appendChild(cursor);
		let i = 0; function type(){ if(i<=full.length){ codeBlock.textContent = full.slice(0,i++); setTimeout(type,18);} else { cursor.classList.add('blink'); } }
		setTimeout(type, 300);
	}

	// Login interactivity
	const form = document.getElementById('login-form');
	const username = document.getElementById('username');
	const password = document.getElementById('password');
	const submit = document.getElementById('login-submit');
	const toggle = document.getElementById('toggle-password');
	const caps = document.getElementById('caps-indicator');
	const card = document.getElementById('login-card');

	function updateSubmit(){ if(submit) submit.disabled = !(username && username.value && password && password.value); }
	if(username){ username.addEventListener('input', updateSubmit); }
	if(password){ password.addEventListener('input', updateSubmit); password.addEventListener('keyup', function(e){ if(caps){ caps.style.display = e.getModifierState && e.getModifierState('CapsLock') ? 'inline' : 'none'; } }); }
	if(toggle && password){ toggle.addEventListener('click', function(){ const isPwd = password.type === 'password'; password.type = isPwd ? 'text' : 'password'; toggle.innerHTML = isPwd ? '<i class="fas fa-eye-slash"></i>' : '<i class="fas fa-eye"></i>'; }); }
	updateSubmit();

	// Tilt эффект карточки
	if(card){
		card.addEventListener('mousemove', function(e){
			const rect = card.getBoundingClientRect();
			const x = e.clientX - rect.left; const y = e.clientY - rect.top;
			const rx = (y/rect.height - 0.5) * -6; // вращение X
			const ry = (x/rect.width - 0.5) * 6;  // вращение Y
			card.style.transform = 'perspective(800px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
		});
		card.addEventListener('mouseleave', function(){ card.style.transform = 'none'; });
	}
})();

// Мини-игра на логине
(function(){
	const canvas = document.getElementById('login-game');
	if(!canvas) return;
	const ctx = canvas.getContext('2d');
	const W = canvas.width, H = canvas.height;
	let score = 0, time = 30, running = true, finished = false;
	const scoreEl = document.getElementById('game-score');
	const timeEl = document.getElementById('game-time');
	const restartBtn = document.getElementById('game-restart');

	function declension(n){
		const mod10 = n % 10, mod100 = n % 100;
		if(mod10 === 1 && mod100 !== 11) return 'балл';
		if(mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return 'балла';
		return 'баллов';
	}

	const player = { x: W/2 - 20, y: H - 20, w: 48, h: 10, speed: 6, vx: 0 };
	let items = [];
	function createItem(y){
		// 20% шанс на золотой кубик со x2 очками и чуть медленнее
		const isGold = Math.random() < 0.2;
		const s = 14;
		const vy = isGold ? (1.4 + Math.random()*0.8) : (1.6 + Math.random()*1.2); // замедлено
		return { x: Math.random()*(W-s), y: y, s: s, vy: vy, gold: isGold, value: isGold ? 2 : 1 };
	}
	function spawn(){ items.push(createItem(-14)); }
	function primeSpawns(){ for(let i=0;i<4;i++){ items.push(createItem(-i*40 - 14)); } }
	let spawnTimer = 0;
	let iv = null, timerRunning = false;
	function tick(){ if(!running) return; time--; if(timeEl) timeEl.textContent=time+'s'; if(time<=0){ running=false; finished=true; if(iv){ clearInterval(iv); timerRunning=false; } } }

	function reset(){
		score = 0; time = 30; running = true; finished = false; items = []; player.x = W/2 - player.w/2; keys.left = keys.right = false; player.vx = 0; if(scoreEl) scoreEl.textContent = '0'; if(timeEl) timeEl.textContent='30s'; spawnTimer=0; primeSpawns(); if(!timerRunning){ iv = setInterval(tick,1000); timerRunning = true; } update();
	}

	function drawGameOver(){
		ctx.fillStyle = 'rgba(2,6,23,0.65)'; ctx.fillRect(0,0,W,H);
		ctx.fillStyle = '#e2e8f0'; ctx.textAlign = 'center';
		ctx.font = 'bold 20px Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
		ctx.fillText('Игра окончена', W/2, H/2 - 14);
		ctx.font = '16px Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif';
		ctx.fillText('Ваш результат: ' + score + ' ' + declension(score), W/2, H/2 + 10);
	}
	function update(){
		ctx.fillStyle = '#0b1020';
		ctx.fillRect(0,0,W,H);
		if(running){
			player.vx = (keys.left ? -player.speed : 0) + (keys.right ? player.speed : 0);
			player.x += player.vx; if(player.x < 0) player.x = 0; if(player.x+player.w>W) player.x=W-player.w;
			if(spawnTimer++ % 24 === 0) spawn();
			for(let i=items.length-1;i>=0;i--){
				const it=items[i]; it.y+=it.vy;
				if(it.y+it.s>=player.y && it.x<player.x+player.w && it.x+it.s>player.x){ score += it.value; items.splice(i,1); continue; }
				if(it.y>H){ items.splice(i,1); }
			}
		}
		ctx.fillStyle = '#22d3ee'; ctx.fillRect(player.x, player.y, player.w, player.h);
		// обычные кубики
		items.forEach(it=>{
			ctx.fillStyle = it.gold ? '#facc15' : '#a78bfa';
			ctx.fillRect(it.x,it.y,it.s,it.s);
		});
		if(scoreEl) scoreEl.textContent = score;
		if(finished){ drawGameOver(); return; }
		requestAnimationFrame(update);
	}

	// управление
const keys = { left:false, right:false };
// Флаг активации игры - по умолчанию игра не активна
let gameActive = false;

// Функция для активации игры по клику
function activateGame() {
    gameActive = true;
    // Добавляем визуальную индикацию активации
    const canvas = document.getElementById('login-game');
    if (canvas) {
        canvas.style.border = '2px solid #4CAF50';
    }
    const regCanvas = document.getElementById('register-game');
    if (regCanvas) {
        regCanvas.style.border = '2px solid #4CAF50';
    }
}

function handleKey(e, down){ 
    // Если игра не активирована или игра завершена - не обрабатываем клавиши
    if(!gameActive || finished) return; 
    
    // Проверяем, находится ли фокус в поле ввода
    if (document.activeElement && (document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
        return; // Не обрабатываем клавиши, если фокус в поле ввода
    }
    
    const k = e.key; 
    // Используем только стрелки, игнорируем A и D
    if(k==='ArrowLeft'){ 
        keys.left = down; 
        e.preventDefault(); 
    } 
    if(k==='ArrowRight'){ 
        keys.right = down; 
        e.preventDefault(); 
    } 
}
	document.addEventListener('keydown', e=>handleKey(e,true), { passive: false });
document.addEventListener('keyup', e=>handleKey(e,false), { passive: false });

// Добавляем обработчики клика по игровому полю для активации игры
document.addEventListener('DOMContentLoaded', function() {
    const loginCanvas = document.getElementById('login-game');
    if (loginCanvas) {
        loginCanvas.addEventListener('click', activateGame);
    }
    
    const registerCanvas = document.getElementById('register-game');
    if (registerCanvas) {
        registerCanvas.addEventListener('click', activateGame);
    }
});
	window.addEventListener('blur', ()=>{ keys.left = keys.right = false; });

	if(restartBtn){ restartBtn.addEventListener('click', function(){ reset(); }); }

	// старт
	reset();
})();

// Регистрация: интерактив
(function(){
	const form = document.getElementById('register-form');
	if(!form) return;
	const pass1 = document.getElementById('password1');
	const pass2 = document.getElementById('password2');
	const caps1 = document.getElementById('caps1');
	const caps2 = document.getElementById('caps2');
	const bar = document.getElementById('strength-bar');
	const barText = document.getElementById('strength-text');
	const matchText = document.getElementById('match-text');
	const submit = document.getElementById('register-submit');

	// Toggle
	form.querySelectorAll('.toggle-pass').forEach(btn=>{
		btn.addEventListener('click', ()=>{
			const target = document.getElementById(btn.getAttribute('data-target'));
			if(target){ const isPwd = target.type==='password'; target.type = isPwd? 'text':'password'; btn.innerHTML = isPwd? '<i class="fas fa-eye-slash"></i>' : '<i class="fas fa-eye"></i>'; }
		});
	});

	// CapsLock indicators
	function capsHandler(e, el){ if(!el) return; el.style.display = e.getModifierState && e.getModifierState('CapsLock') ? 'inline' : 'none'; }
	if(pass1) pass1.addEventListener('keyup', e=>capsHandler(e,caps1));
	if(pass2) pass2.addEventListener('keyup', e=>capsHandler(e,caps2));

	// Strength meter
	function strength(p){ let s=0; if(p.length>=8) s++; if(/[A-Z]/.test(p)) s++; if(/[a-z]/.test(p)) s++; if(/[0-9]/.test(p)) s++; if(/[^A-Za-z0-9]/.test(p)) s++; return s; }
	function renderStrength(){
		if(!bar) return;
		const s = strength(pass1.value||'');
		const map = [0,20,40,60,80,100][s];
		bar.style.setProperty('--w', map+'%');
		bar.style.position='relative';
		bar.style.setProperty('--c', s<=2? '#ef4444' : s<=4? '#f59e0b' : '#10b981');
		bar.style.setProperty('--bg', '#e5e7eb');
		bar.style.background = 'var(--bg)';
		const after = bar.querySelector('i');
		bar.style.setProperty('--dummy','');
		bar.style.setProperty('--barWidth', map+'%');
		bar.style.setProperty('--barColor', (s<=2? '#ef4444' : s<=4? '#f59e0b' : '#10b981'));
		bar.style.setProperty('--barShadow', '0 0 0');
		bar.style.setProperty('--barRadius', '4px');
		bar.style.setProperty('--bar', '');
		bar.style.setProperty('--w', map+'%');
		bar.style.setProperty('--c', (s<=2? '#ef4444' : s<=4? '#f59e0b' : '#10b981'));
		bar.style.setProperty('--dummy2', '');
		bar.style.setProperty('--dummy3', '');
		bar.style.setProperty('--dummy4', '');
		bar.style.setProperty('--dummy5', '');
		bar.style.setProperty('--dummy6', '');
		bar.style.setProperty('--dummy7', '');
		// update ::after width via inline style (fallback)
		bar.style.setProperty('--afterWidth', map+'%');
		bar.style.setProperty('--afterColor', (s<=2? '#ef4444' : s<=4? '#f59e0b' : '#10b981'));
		bar.style.setProperty('background', '#e5e7eb');
		bar.style.setProperty('position', 'relative');
		barText && (barText.textContent = s<=2? 'Слабый пароль' : s<=4? 'Средний пароль' : 'Надёжный пароль');
	}
	if(pass1) pass1.addEventListener('input', renderStrength);

	// Match + submit enable
	function updateSubmit(){
		const okUser = document.getElementById('username').value.trim().length>=3;
		const okP1 = (pass1.value||'').length>=6;
		const okMatch = pass1.value && pass1.value === pass2.value;
		if(matchText){ matchText.style.color = okMatch? '#10b981' : '#dc2626'; matchText.textContent = okMatch? 'Пароли совпадают' : 'Пароли должны совпадать'; }
		submit && (submit.disabled = !(okUser && okP1 && okMatch));
	}
	if(pass1) pass1.addEventListener('input', updateSubmit);
	if(pass2) pass2.addEventListener('input', updateSubmit);
	updateSubmit();
})();

// Мини-игра регистрации (клик по целям)
(function(){
	// Отключаем обработку клавиш A и D для формы регистрации
	document.addEventListener('keydown', function(e) {
		if ((e.key === 'a' || e.key === 'A' || e.key === 'd' || e.key === 'D') && 
			(document.activeElement.tagName === 'INPUT' || document.activeElement.tagName === 'TEXTAREA')) {
			// Не блокируем стандартное поведение для полей ввода
			return true;
		}
	});
	
	const canvas = document.getElementById('register-game');
	if(!canvas) return;
	const ctx = canvas.getContext('2d');
	const W = canvas.width, H = canvas.height;
	let score = 0, time = 30, running = true, finished=false;
	const scoreEl = document.getElementById('reg-score');
	const timeEl = document.getElementById('reg-time');
	const restart = document.getElementById('reg-restart');

	function declension(n){ const m10=n%10,m100=n%100; if(m10===1&&m100!==11) return 'балл'; if(m10>=2&&m10<=4&&(m100<10||m100>=20)) return 'балла'; return 'баллов'; }

	let targets = [];
	function spawn(){
		const r = 14 + Math.random()*10;
		const x = r + Math.random()*(W-2*r);
		const y = r + Math.random()*(H-2*r);
		const isGold = Math.random() < 0.2;
		const ttl = 120 + Math.floor(Math.random()*90); // 2–3.5 сек
		targets.push({x,y,r,ttl,gold:isGold,value:isGold?2:1});
	}
	let spawnTick = 0;

	function reset(){ score=0; time=30; running=true; finished=false; targets=[]; if(scoreEl) scoreEl.textContent='0'; if(timeEl) timeEl.textContent='30s'; spawnTick=0; update(); if(!timerRunning){ iv=setInterval(tick,1000); timerRunning=true; } }
	function drawGameOver(){ ctx.fillStyle='rgba(2,6,23,0.65)'; ctx.fillRect(0,0,W,H); ctx.fillStyle='#e2e8f0'; ctx.textAlign='center'; ctx.font='bold 20px Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif'; ctx.fillText('Игра окончена', W/2, H/2-14); ctx.font='16px Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif'; ctx.fillText('Ваш результат: '+score+' '+declension(score), W/2, H/2+10);} 

	function update(){
		ctx.fillStyle='#0b1020'; ctx.fillRect(0,0,W,H);
		if(running){
			if(spawnTick++ % 30 === 0 && targets.length < 6) spawn();
			targets.forEach(t=> t.ttl--);
			targets = targets.filter(t=> t.ttl>0);
		}
		targets.forEach(t=>{
			ctx.beginPath(); ctx.arc(t.x,t.y,t.r,0,Math.PI*2);
			ctx.fillStyle = t.gold? '#facc15' : '#3b82f6';
			ctx.fill();
			ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(255,255,255,.2)'; ctx.stroke();
		});
		if(scoreEl) scoreEl.textContent = score;
		if(finished){ drawGameOver(); return; }
		requestAnimationFrame(update);
	}
	let iv=null, timerRunning=false; function tick(){ if(!running) return; time--; if(timeEl) timeEl.textContent=time+'s'; if(time<=0){ running=false; finished=true; if(iv){ clearInterval(iv); timerRunning=false; } } }

	canvas.addEventListener('click', function(e){
		if(!running) return;
		const rect = canvas.getBoundingClientRect();
		// масштаб между CSS размером и внутренним буфером канваса
		const scaleX = canvas.width / rect.width;
		const scaleY = canvas.height / rect.height;
		const x = (e.clientX - rect.left) * scaleX;
		const y = (e.clientY - rect.top) * scaleY;
		for(let i=targets.length-1;i>=0;i--){
			const t=targets[i]; const dx=x-t.x, dy=y-t.y;
			if(dx*dx+dy*dy<=t.r*t.r){ score += t.value; targets.splice(i,1); break; }
		}
	});
	if(restart){ restart.addEventListener('click', reset); }

	reset();
})();
