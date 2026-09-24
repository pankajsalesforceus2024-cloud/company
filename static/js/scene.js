/* =============================================================================
   SUMAN INFO — HERO 3D SCENE (Three.js)
   -----------------------------------------------------------------------
   Renders an interactive icosahedron core surrounded by an orbiting
   particle field inside the hero canvas.
   Interactions:
     - Drag / touch  -> rotate the scene
     - Mouse move    -> parallax + raycaster hover highlight
     - Click on core -> particle "burst" animation
   Uses Three.js r128 (MIT License) loaded via CDN in index.html.
   ============================================================================= */
(function () {
    const canvas = document.getElementById("heroCanvas");
    if (!canvas || typeof THREE === "undefined") return;

    const theme = window.SITE_THEME || { primary: "#5b8cff", secondary: "#7c5cff", accent: "#22d3c8" };

    let width = window.innerWidth;
    let height = window.innerHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, width / height, 0.1, 1000);
    camera.position.set(0, 0, 9);

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);

    // ---------- Lighting ----------
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const point = new THREE.PointLight(new THREE.Color(theme.primary), 1.4, 100);
    point.position.set(6, 6, 8);
    scene.add(point);
    const point2 = new THREE.PointLight(new THREE.Color(theme.accent), 1, 100);
    point2.position.set(-6, -4, 6);
    scene.add(point2);

    // ---------- Core: interactive icosahedron ----------
    const coreGeo = new THREE.IcosahedronGeometry(2.1, 1);
    const coreMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(theme.primary),
        metalness: 0.35,
        roughness: 0.25,
        flatShading: true,
        emissive: new THREE.Color(theme.secondary),
        emissiveIntensity: 0.12,
    });
    const core = new THREE.Mesh(coreGeo, coreMat);
    scene.add(core);

    const wireGeo = new THREE.IcosahedronGeometry(2.4, 1);
    const wireMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(theme.accent), wireframe: true, transparent: true, opacity: 0.25 });
    const wire = new THREE.Mesh(wireGeo, wireMat);
    scene.add(wire);

    // ---------- Orbiting particle field ----------
    const particleCount = 700;
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
        const radius = 4.5 + Math.random() * 4;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
        positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
        positions[i * 3 + 2] = radius * Math.cos(phi);
    }
    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({
        color: new THREE.Color(theme.accent),
        size: 0.045,
        transparent: true,
        opacity: 0.8,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // ---------- Interaction state ----------
    let isDragging = false;
    let prevX = 0, prevY = 0;
    let targetRotX = 0, targetRotY = 0;
    let autoRotate = true;
    let mouseNX = 0, mouseNY = 0; // normalized mouse (-1..1)

    const raycaster = new THREE.Raycaster();
    const mouseVec = new THREE.Vector2();
    let hovering = false;

    function setPointer(clientX, clientY) {
        const rect = canvas.getBoundingClientRect();
        mouseNX = ((clientX - rect.left) / rect.width) * 2 - 1;
        mouseNY = -(((clientY - rect.top) / rect.height) * 2 - 1);
        mouseVec.set(mouseNX, mouseNY);
    }

    canvas.addEventListener("pointerdown", (e) => {
        isDragging = true;
        autoRotate = false;
        prevX = e.clientX;
        prevY = e.clientY;
    });
    window.addEventListener("pointerup", () => { isDragging = false; });
    window.addEventListener("pointermove", (e) => {
        setPointer(e.clientX, e.clientY);
        if (isDragging) {
            const dx = e.clientX - prevX;
            const dy = e.clientY - prevY;
            targetRotY += dx * 0.006;
            targetRotX += dy * 0.006;
            prevX = e.clientX;
            prevY = e.clientY;
        }
    });
    canvas.addEventListener("pointerleave", () => { isDragging = false; });

    // Click on the core -> burst animation
    let burstStart = 0;
    let bursting = false;
    canvas.addEventListener("click", () => {
        raycaster.setFromCamera(mouseVec, camera);
        const hit = raycaster.intersectObject(core);
        if (hit.length) {
            bursting = true;
            burstStart = performance.now();
        }
    });

    window.addEventListener("resize", () => {
        width = window.innerWidth;
        height = window.innerHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });

    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const t = clock.getElapsedTime();

        if (autoRotate) {
            targetRotY += 0.0025;
        }
        core.rotation.y += (targetRotY - core.rotation.y) * 0.08;
        core.rotation.x += (targetRotX - core.rotation.x) * 0.08;
        wire.rotation.copy(core.rotation);
        wire.rotation.y -= 0.002;

        particles.rotation.y = t * 0.03;
        particles.rotation.x = Math.sin(t * 0.05) * 0.1;

        // Parallax camera drift based on mouse
        camera.position.x += (mouseNX * 1.2 - camera.position.x) * 0.03;
        camera.position.y += (mouseNY * 0.8 - camera.position.y) * 0.03;
        camera.lookAt(0, 0, 0);

        // Hover highlight via raycasting
        raycaster.setFromCamera(mouseVec, camera);
        const hit = raycaster.intersectObject(core);
        if (hit.length && !hovering) {
            hovering = true;
            coreMat.emissiveIntensity = 0.45;
            canvas.style.cursor = "pointer";
        } else if (!hit.length && hovering) {
            hovering = false;
            coreMat.emissiveIntensity = 0.12;
            canvas.style.cursor = "grab";
        }

        // Burst animation: scale wireframe pulse outward then settle
        if (bursting) {
            const elapsed = (performance.now() - burstStart) / 1000;
            const progress = Math.min(elapsed / 0.8, 1);
            const scale = 1 + Math.sin(progress * Math.PI) * 0.35;
            wire.scale.setScalar(scale);
            particleMat.size = 0.045 + Math.sin(progress * Math.PI) * 0.05;
            if (progress >= 1) bursting = false;
        } else {
            wire.scale.setScalar(1);
        }

        renderer.render(scene, camera);
    }
    animate();

    // Resume auto-rotate after a period of inactivity
    let idleTimer = null;
    window.addEventListener("pointermove", () => {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(() => { autoRotate = true; }, 3500);
    });
})();
