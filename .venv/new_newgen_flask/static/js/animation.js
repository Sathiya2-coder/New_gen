// Canvas-based background animation: fewer DOM changes, slow movement, no flicker
document.addEventListener('DOMContentLoaded', () => {
	const container = document.getElementById('vertexBg');
	if (!container) return;

	container.style.pointerEvents = 'none';
	container.style.overflow = 'hidden';

	// Create canvas that fills the container
	const canvas = document.createElement('canvas');
	canvas.style.position = 'absolute';
	canvas.style.left = '0';
	canvas.style.top = '0';
	canvas.style.width = '100%';
	canvas.style.height = '100%';
	canvas.style.zIndex = '0';
	canvas.style.pointerEvents = 'none';
	container.appendChild(canvas);

	const ctx = canvas.getContext('2d');
	let width = 0;
	let height = 0;
	let dpr = Math.max(window.devicePixelRatio || 1, 1);

	// Detect theme and set node colors accordingly
	const isDarkTheme = document.body.classList.contains('theme-dark');
	const NODE_COLOR = isDarkTheme ? '255,255,255' : '255,215,0'; // white for dark, gold for light
	const LINE_COLOR = isDarkTheme ? '255,255,255' : '255,215,0'; // same as node color

	// Node settings (medium movement)
	const MAX_NODES = Math.min(300, Math.max(100, Math.floor(window.innerWidth / 60)));
	const NODE_COLOR_STR = NODE_COLOR;
	const LINE_COLOR_STR = LINE_COLOR;
	const MAX_DIST = 180; // pixels
	const nodes = [];

	function resize() {
		// handle devicePixelRatio for crisp rendering
		dpr = Math.max(window.devicePixelRatio || 1, 1);
		width = container.clientWidth || window.innerWidth;
		height = container.clientHeight || window.innerHeight;
		canvas.width = Math.round(width * dpr);
		canvas.height = Math.round(height * dpr);
		canvas.style.width = width + 'px';
		canvas.style.height = height + 'px';
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
	}

	function initNodes() {
		nodes.length = 0;
		const count = MAX_NODES;
		for (let i = 0; i < count; i++) {
			// randomly mark some nodes as highlighted/fast
			const isHighlight = Math.random() < 0.28; // ~28% brighter & faster (increased)
			const speedBase = isHighlight ? 0.9 : 0.32; // highlighted nodes move faster
			const brightness = isHighlight ? (1.00 + Math.random() * 1.05) : (1.00 + Math.random() * 1.25); // brighter overall
			nodes.push({
				x: Math.random() * width,
				y: Math.random() * height,
				// velocities scaled by speedBase and slightly varied
				vx: (Math.random() - 0.5) * speedBase,
				vy: (Math.random() - 0.5) * speedBase,
				r: isHighlight ? (1.8 + Math.random() * 2.2) : (1 + Math.random() * 2),
				bright: brightness,
				highlight: isHighlight
			});
		}
	}

	// Debounced resize
	let resizeTimer = null;
	window.addEventListener('resize', () => {
		if (resizeTimer) clearTimeout(resizeTimer);
		resizeTimer = setTimeout(() => {
			resize();
			initNodes();
		}, 120);
	});

	function update(dt) {
		// dt is in seconds
		for (let i = 0; i < nodes.length; i++) {
			const n = nodes[i];
			n.x += n.vx * dt * 60; // normalize to 60fps movement scale
			n.y += n.vy * dt * 60;
			// bounce at edges with gentle wrap
			if (n.x < -10) n.x = width + 10;
			if (n.x > width + 10) n.x = -10;
			if (n.y < -10) n.y = height + 10;
			if (n.y > height + 10) n.y = -10;
		}
	}

	function draw() {
		ctx.clearRect(0, 0, width, height);

		// draw lines between close nodes
		for (let i = 0; i < nodes.length; i++) {
			const a = nodes[i];
			for (let j = i + 1; j < nodes.length; j++) {
				const b = nodes[j];
				const dx = a.x - b.x;
				const dy = a.y - b.y;
				const dist = Math.sqrt(dx * dx + dy * dy);
				if (dist <= MAX_DIST) {
					const alpha = (1 - dist / MAX_DIST) * 0.28; // increased alpha for brighter lines
					ctx.strokeStyle = `rgba(${LINE_COLOR_STR}, ${alpha})`;
					ctx.lineWidth = 1.2; // slightly thicker lines for better visibility
					ctx.beginPath();
					ctx.moveTo(a.x, a.y);
					ctx.lineTo(b.x, b.y);
					ctx.stroke();
				}
			}
		}

		// draw nodes on top; highlighted nodes are brighter
		for (let i = 0; i < nodes.length; i++) {
			const n = nodes[i];
			const alpha = Math.min(1, n.bright || 0.8);
			// slightly glow for highlighted nodes using shadow
			if (n.highlight) {
				ctx.save();
				ctx.shadowColor = `rgba(${NODE_COLOR_STR}, ${Math.min(1, alpha)})`;
				ctx.shadowBlur = 16; // increased glow blur for stronger brightness
			}
			ctx.fillStyle = `rgba(${NODE_COLOR_STR}, ${alpha})`;
			ctx.beginPath();
			ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
			ctx.fill();
			if (n.highlight) ctx.restore();
		}
	}

	// Animation loop with time delta to keep movement consistent and slow
	let last = performance.now();
	function loop(now) {
		const dt = Math.max(0.001, (now - last) / 1000);
		last = now;
		update(dt);
		draw();
		requestAnimationFrame(loop);
	}

	// Initialize sizes and nodes, then start
	resize();
	initNodes();
	requestAnimationFrame(loop);
});
