// Filter definitions - Instagram-like filters using CSS filters
const filters = {
    none: '',
    clarendon: 'contrast(1.2) saturate(1.35) brightness(1.1)',
    gingham: 'contrast(1.1) brightness(1.05) saturate(1.1) hue-rotate(-10deg)',
    moon: 'grayscale(1) contrast(1.1) brightness(1.1)',
    lark: 'contrast(0.9) brightness(1.1) saturate(1.1)',
    reyes: 'sepia(0.22) contrast(0.85) brightness(1.1) saturate(0.75)',
    juno: 'contrast(1.15) brightness(1.1) saturate(1.2) hue-rotate(-10deg)',
    slumber: 'contrast(0.95) brightness(1.05) saturate(0.9) sepia(0.2)',
    crema: 'contrast(1.1) brightness(1.15) saturate(1.1) sepia(0.2)',
    ludwig: 'contrast(1.05) brightness(1.05) saturate(1.1)',
    aden: 'contrast(0.9) brightness(1.2) saturate(0.85) hue-rotate(-20deg)',
    perpetua: 'contrast(1.1) brightness(1.1) saturate(1.1) sepia(0.3)'
};

// DOM elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const displayCanvas = document.getElementById('displayCanvas');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const captureBtn = document.getElementById('captureBtn');
const filtersGrid = document.getElementById('filtersGrid');
const filterItems = document.querySelectorAll('.filter-item');
const pixelateControl = document.getElementById('pixelateControl');
const pixelSizeInput = document.getElementById('pixelSize');
const pixelSizeValue = document.getElementById('pixelSizeValue');
const halftoneControl = document.getElementById('halftoneControl');
const halftoneSizeInput = document.getElementById('halftoneSize');
const halftoneSizeValue = document.getElementById('halftoneSizeValue');

let stream = null;
let currentFilter = 'none';
let pixelSize = 10;
let halftoneSize = 8;
let animationFrameId = null;

// Initialize filter selection - use event delegation for dynamic filters
filtersGrid.addEventListener('click', (e) => {
    const filterItem = e.target.closest('.filter-item');
    if (filterItem) {
        const filterName = filterItem.dataset.filter;
        selectFilter(filterName);
    }
});

// Pixelation function
function pixelate(ctx, imageData, pixelSize) {
    const data = imageData.data;
    const width = imageData.width;
    const height = imageData.height;
    
    for (let y = 0; y < height; y += pixelSize) {
        for (let x = 0; x < width; x += pixelSize) {
            // Get the color of the center pixel in this block
            const centerX = Math.min(x + Math.floor(pixelSize / 2), width - 1);
            const centerY = Math.min(y + Math.floor(pixelSize / 2), height - 1);
            const index = (centerY * width + centerX) * 4;
            
            const r = data[index];
            const g = data[index + 1];
            const b = data[index + 2];
            const a = data[index + 3];
            
            // Fill the entire block with this color
            for (let py = y; py < y + pixelSize && py < height; py++) {
                for (let px = x; px < x + pixelSize && px < width; px++) {
                    const pixelIndex = (py * width + px) * 4;
                    data[pixelIndex] = r;
                    data[pixelIndex + 1] = g;
                    data[pixelIndex + 2] = b;
                    data[pixelIndex + 3] = a;
                }
            }
        }
    }
    
    return imageData;
}

// Halftone function - optimized version
let halftoneCanvas = null;
let halftoneCtx = null;

function halftone(ctx, imageData, dotSpacing) {
    const width = imageData.width;
    const height = imageData.height;
    const data = imageData.data;
    
    // Reuse canvas for better performance
    if (!halftoneCanvas || halftoneCanvas.width !== width || halftoneCanvas.height !== height) {
        halftoneCanvas = document.createElement('canvas');
        halftoneCanvas.width = width;
        halftoneCanvas.height = height;
        halftoneCtx = halftoneCanvas.getContext('2d');
    }
    
    // Fill with white background
    halftoneCtx.fillStyle = '#ffffff';
    halftoneCtx.fillRect(0, 0, width, height);
    
    // Set dot color
    halftoneCtx.fillStyle = '#000000';
    
    // Process in grid pattern
    const sampleRadius = Math.max(1, Math.floor(dotSpacing / 2));
    
    for (let y = 0; y < height; y += dotSpacing) {
        for (let x = 0; x < width; x += dotSpacing) {
            // Sample a small area around this point
            let totalBrightness = 0;
            let sampleCount = 0;
            
            const startY = Math.max(0, y - sampleRadius);
            const endY = Math.min(height, y + sampleRadius);
            const startX = Math.max(0, x - sampleRadius);
            const endX = Math.min(width, x + sampleRadius);
            
            for (let sy = startY; sy < endY; sy++) {
                for (let sx = startX; sx < endX; sx++) {
                    const index = (sy * width + sx) * 4;
                    const r = data[index];
                    const g = data[index + 1];
                    const b = data[index + 2];
                    // Convert to grayscale and invert (darker = higher value)
                    const brightness = 1 - (0.299 * r + 0.587 * g + 0.114 * b) / 255;
                    totalBrightness += brightness;
                    sampleCount++;
                }
            }
            
            if (sampleCount > 0) {
                const avgBrightness = totalBrightness / sampleCount;
                // Dot size is proportional to darkness (brightness value)
                const dotRadius = (avgBrightness * dotSpacing * 0.45);
                
                if (dotRadius > 0.5) {
                    // Draw the dot
                    halftoneCtx.beginPath();
                    halftoneCtx.arc(x, y, dotRadius, 0, Math.PI * 2);
                    halftoneCtx.fill();
                }
            }
        }
    }
    
    // Copy the halftone result back to the original context
    ctx.clearRect(0, 0, width, height);
    ctx.drawImage(halftoneCanvas, 0, 0);
    
    return imageData;
}

// Render pixelated video
function renderPixelated() {
    if (!video.srcObject || currentFilter !== 'pixelate') {
        return;
    }
    
    const ctx = displayCanvas.getContext('2d');
    ctx.drawImage(video, 0, 0, displayCanvas.width, displayCanvas.height);
    
    const imageData = ctx.getImageData(0, 0, displayCanvas.width, displayCanvas.height);
    const pixelatedData = pixelate(ctx, imageData, pixelSize);
    ctx.putImageData(pixelatedData, 0, 0);
    
    animationFrameId = requestAnimationFrame(renderPixelated);
}

// Render halftone video
function renderHalftone() {
    if (!video.srcObject || currentFilter !== 'halftone') {
        return;
    }
    
    const ctx = displayCanvas.getContext('2d');
    ctx.drawImage(video, 0, 0, displayCanvas.width, displayCanvas.height);
    
    const imageData = ctx.getImageData(0, 0, displayCanvas.width, displayCanvas.height);
    halftone(ctx, imageData, halftoneSize);
    
    animationFrameId = requestAnimationFrame(renderHalftone);
}

// Select filter function
function selectFilter(filterName) {
    currentFilter = filterName;
    
    // Stop pixelation animation if switching away
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
    }
    
    // Update active state
    filterItems.forEach(item => {
        if (item.dataset.filter === filterName) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Show/hide controls
    if (filterName === 'pixelate') {
        pixelateControl.style.display = 'block';
        halftoneControl.style.display = 'none';
    } else if (filterName === 'halftone') {
        pixelateControl.style.display = 'none';
        halftoneControl.style.display = 'block';
    } else {
        pixelateControl.style.display = 'none';
        halftoneControl.style.display = 'none';
    }
    
    // Apply filter to video
    if (video.srcObject) {
        if (filterName === 'pixelate') {
            // Hide video, show canvas
            video.style.display = 'none';
            displayCanvas.style.display = 'block';
            renderPixelated();
        } else if (filterName === 'halftone') {
            // Hide video, show canvas
            video.style.display = 'none';
            displayCanvas.style.display = 'block';
            renderHalftone();
        } else {
            // Show video, hide canvas
            video.style.display = 'block';
            displayCanvas.style.display = 'none';
            video.style.filter = filters[filterName] || '';
        }
    }
}

// Start camera
startBtn.addEventListener('click', async () => {
    try {
        // Request camera access
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: 'user'
            },
            audio: false
        });
        
        // Set video source
        video.srcObject = stream;
        
        // Apply current filter
        video.style.filter = filters[currentFilter];
        
        // Update button states
        startBtn.disabled = true;
        stopBtn.disabled = false;
        captureBtn.disabled = false;
        
        // Wait for video to be ready
        video.addEventListener('loadedmetadata', () => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            displayCanvas.width = video.videoWidth;
            displayCanvas.height = video.videoHeight;
            
            // Re-apply current filter
            if (currentFilter === 'pixelate') {
                video.style.display = 'none';
                displayCanvas.style.display = 'block';
                renderPixelated();
            } else if (currentFilter === 'halftone') {
                video.style.display = 'none';
                displayCanvas.style.display = 'block';
                renderHalftone();
            } else {
                video.style.display = 'block';
                displayCanvas.style.display = 'none';
                video.style.filter = filters[currentFilter] || '';
            }
        }, { once: true });
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Unable to access camera. Please make sure you grant camera permissions and that your camera is connected.');
    }
});

// Stop camera
stopBtn.addEventListener('click', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
        video.srcObject = null;
        video.style.filter = '';
        
        // Stop pixelation animation
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
        
        // Reset displays
        video.style.display = 'block';
        displayCanvas.style.display = 'none';
        
        // Update button states
        startBtn.disabled = false;
        stopBtn.disabled = true;
        captureBtn.disabled = true;
    }
});

// Capture photo
captureBtn.addEventListener('click', () => {
    if (!video.srcObject) return;
    
    const ctx = canvas.getContext('2d');
    
    if (currentFilter === 'pixelate') {
        // For pixelate, draw from displayCanvas or process directly
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const pixelatedData = pixelate(ctx, imageData, pixelSize);
        ctx.putImageData(pixelatedData, 0, 0);
    } else if (currentFilter === 'halftone') {
        // For halftone, process directly
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        halftone(ctx, imageData, halftoneSize);
    } else {
        // Draw video frame to canvas with current filter
        ctx.filter = filters[currentFilter] || '';
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        ctx.filter = 'none';
    }
    
    // Create download link
    canvas.toBlob(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `filtered-photo-${Date.now()}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        // Visual feedback
        captureBtn.style.transform = 'scale(0.9)';
        setTimeout(() => {
            captureBtn.style.transform = 'scale(1)';
        }, 150);
    }, 'image/png');
});

// Pixel size control
pixelSizeInput.addEventListener('input', (e) => {
    pixelSize = parseInt(e.target.value);
    pixelSizeValue.textContent = pixelSize;
});

// Halftone size control
halftoneSizeInput.addEventListener('input', (e) => {
    halftoneSize = parseInt(e.target.value);
    halftoneSizeValue.textContent = halftoneSize;
});

// Set initial filter
selectFilter('none');

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
    }
});
