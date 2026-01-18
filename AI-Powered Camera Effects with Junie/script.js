document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d', { alpha: false });
    const buttons = document.querySelectorAll('.filter-btn');
    const errorMessage = document.getElementById('error-message');
    const pixelControl = document.getElementById('pixel-control');
    const pixelSizeInput = document.getElementById('pixel-size');

    let currentFilter = 'none';
    let animationId = null;

    // Access camera
    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                    facingMode: "user"
                },
                audio: false
            });
            video.srcObject = stream;
            
            // Wait for video metadata to be loaded to set canvas dimensions
            video.onloadedmetadata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            };
        } catch (err) {
            console.error("Error accessing camera: ", err);
            errorMessage.textContent = "Unable to access camera. Please make sure you have granted permission.";
        }
    }

    function renderPixelated() {
        if (currentFilter !== 'pixelate') {
            cancelAnimationFrame(animationId);
            return;
        }

        const pixelSize = parseInt(pixelSizeInput.value);
        
        // Calculate dimensions for the low-res version
        const w = canvas.width;
        const h = canvas.height;
        const smallW = Math.ceil(w / pixelSize);
        const smallH = Math.ceil(h / pixelSize);

        // Draw video scaled down
        ctx.drawImage(video, 0, 0, smallW, smallH);
        
        // Disable image smoothing to get sharp pixels when scaling back up
        ctx.imageSmoothingEnabled = false;
        
        // Draw back scaled up
        ctx.drawImage(canvas, 0, 0, smallW, smallH, 0, 0, w, h);

        animationId = requestAnimationFrame(renderPixelated);
    }

    function renderHalftone() {
        if (currentFilter !== 'halftone') {
            cancelAnimationFrame(animationId);
            return;
        }

        const w = canvas.width;
        const h = canvas.height;
        const spacing = 10; // Grid spacing for halftone dots

        // Clear canvas with white background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, w, h);

        // Draw video to a temporary canvas or just get data
        // For performance, we can draw the video at a smaller scale or just full scale once per frame
        // Here we draw it to get the pixel data
        ctx.drawImage(video, 0, 0, w, h);
        const imageData = ctx.getImageData(0, 0, w, h);
        const data = imageData.data;

        // Clear again for drawing dots
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = 'black';

        for (let y = 0; y < h; y += spacing) {
            for (let x = 0; x < w; x += spacing) {
                // Get pixel index
                const i = (y * w + x) * 4;
                const r = data[i];
                const g = data[i + 1];
                const b = data[i + 2];

                // Calculate brightness (0-255)
                const avg = (r + g + b) / 3;
                
                // Darkness is inverted brightness
                const darkness = (255 - avg) / 255;
                
                // Radius based on darkness
                const radius = (spacing / 2) * darkness * 1.5; // multiplier for better effect

                if (radius > 0.1) {
                    ctx.beginPath();
                    ctx.arc(x, y, radius, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }

        animationId = requestAnimationFrame(renderHalftone);
    }

    // Handle filter selection
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.getAttribute('data-filter');
            currentFilter = filter;
            
            // Update UI state
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            if (filter === 'pixelate') {
                video.style.display = 'none';
                canvas.style.display = 'block';
                pixelControl.style.display = 'flex';
                renderPixelated();
            } else if (filter === 'halftone') {
                video.style.display = 'none';
                canvas.style.display = 'block';
                pixelControl.style.display = 'none';
                renderHalftone();
            } else {
                cancelAnimationFrame(animationId);
                video.style.display = 'block';
                canvas.style.display = 'none';
                pixelControl.style.display = 'none';
                video.style.filter = filter;
            }
        });
    });

    initCamera();
});
