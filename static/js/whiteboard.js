document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('whiteboard');
    const ctx = canvas.getContext('2d');
    const socket = io({
        // Add these options to reduce packet frequency
        pingTimeout: 3000,
        pingInterval: 5000,
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000
    });

    const whiteboardId = WHITEBOARD_ID;

    const colorPicker = document.getElementById('colorPicker');
    const lineWidth = document.getElementById('lineWidth');
    const clearBtn = document.getElementById('clearBtn');

    let isDrawing = false;
    let lastX = 0;
    let lastY = 0;

    // Throttle drawing emissions
    const throttle = (func, limit) => {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    };

    // Join the specific whiteboard room
    socket.emit('join', { whiteboard_id: whiteboardId });

    function setupCanvasListeners() {
        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', throttledDraw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseout', stopDrawing);

        // Touch support
        canvas.addEventListener('touchstart', handleTouchStart, { passive: false });
        canvas.addEventListener('touchmove', handleTouchMove, { passive: false });
        canvas.addEventListener('touchend', stopDrawing);
    }

    function startDrawing(e) {
        isDrawing = true;
        const rect = canvas.getBoundingClientRect();
        lastX = e.clientX - rect.left;
        lastY = e.clientY - rect.top;
    }

    function handleTouchStart(e) {
        e.preventDefault();
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        lastX = touch.clientX - rect.left;
        lastY = touch.clientY - rect.top;
        isDrawing = true;
    }

    function handleTouchMove(e) {
        e.preventDefault();
        if (!isDrawing) return;
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        const currentX = touch.clientX - rect.left;
        const currentY = touch.clientY - rect.top;
        draw({ clientX: currentX, clientY: currentY });
    }

    const throttledDraw = throttle(function(e) {
        draw(e);
    }, 10); // 10ms throttle

    function draw(e) {
        if (!isDrawing) return;

        const rect = canvas.getBoundingClientRect();
        const currentX = e.clientX - rect.left;
        const currentY = e.clientY - rect.top;

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(currentX, currentY);
        ctx.strokeStyle = colorPicker.value;
        ctx.lineWidth = lineWidth.value;
        ctx.lineCap = 'round';
        ctx.stroke();

        // Compact payload
        socket.emit('draw', {
            whiteboard_id: whiteboardId, // shortened key
            x0: lastX,
            y0: lastY,
            x1: currentX,
            y1: currentY,
            c: colorPicker.value, // shortened color
            l: lineWidth.value    // shortened line width
        });

        lastX = currentX;
        lastY = currentY;
    }

    function stopDrawing() {
        isDrawing = false;
    }

    // Remote drawing handler with more compact parsing
        // Remote drawing handler with more compact parsing
    socket.on('draw', (data) => {
        // Only draw if the data is for this specific whiteboard
        if (data.w === whiteboardId) {
            ctx.beginPath();
            ctx.moveTo(data.x0, data.y0);
            ctx.lineTo(data.x1, data.y1);
            ctx.strokeStyle = data.c;
            ctx.lineWidth = data.l;
            ctx.lineCap = 'round';
            ctx.stroke();
        }
    });

    // Clear canvas functionality with compact payload
    clearBtn.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        socket.emit('clear_canvas', { whiteboard_id: whiteboardId });
    });

    // Handle remote clear
    socket.on('clear_canvas', (data) => {
        // Only clear if the clear is for this specific whiteboard
        if (data.w === whiteboardId) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    });

    // Resize canvas to fit window
    function resizeCanvas() {
        const container = canvas.parentElement;
        canvas.width = container.clientWidth * 0.95;
        canvas.height = window.innerHeight * 0.6;
    }

    // Add resize listener
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Connection status indicators
    socket.on('connect', () => {
        console.log('Socket connected successfully to whiteboard:', whiteboardId);
    });

    socket.on('disconnect', (reason) => {
        console.warn('Socket disconnected:', reason);
    });

    socket.on('connect_error', (error) => {
        console.error('Socket connection error:', error);
    });

    // Initial setup
    setupCanvasListeners();
});

