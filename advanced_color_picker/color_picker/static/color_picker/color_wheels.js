function x_y_to_angle(x, y) {
    let dist = Math.sqrt(x**2+y**2);
    let angle = 0;
    if (y > 0) {
        angle = Math.acos(x/dist)*180/Math.PI;
    } else if (y < 0) {
        angle = -Math.acos(x/dist)*180/Math.PI;
    } else if (x > 0) {
        angle = 0
    } else {
        angle = 180
    }
    return angle;
}

function mapRange(x, a, b, c, d) {
    return c + (x - a) * (d - c) / (b - a);
    }

function hsl_hs_wheel(margin) {
    const canvas = document.getElementById("hsl-wheel-1");
    const ctx = canvas.getContext("2d");

    const canvas_w = canvas.clientWidth;
    const canvas_h = canvas.clientHeight;

    const wheel_w = canvas_w - 2 * margin;
    const wheel_h = canvas_h - 2 * margin;
    const wheel_r = Math.min(wheel_w, wheel_h)/2;

    const wheel_center_x = canvas_w  / 2;
    const wheel_center_y = canvas_h / 2;

    const x_min_wheel = wheel_center_x - wheel_r;
    const x_max_wheel = wheel_center_x + wheel_r;
    const y_min_wheel = wheel_center_y - wheel_r;
    const y_max_wheel = wheel_center_y + wheel_r;

    for (let x_cvs = x_min_wheel; x_cvs < x_max_wheel; x_cvs++) {
        for (let y_cvs = y_min_wheel; y_cvs < y_max_wheel; y_cvs++) {
            // X vers la droite
            // Y vers le bas

            let x_wrt_center = x_cvs-wheel_center_x;
            let y_wrt_center = y_cvs-wheel_center_y;
            let dist_to_center = Math.sqrt((x_wrt_center)**2 + (y_wrt_center)**2);
            
            if (dist_to_center <= wheel_r) {
                let h = -x_y_to_angle(x_wrt_center, y_wrt_center)
                let s = 100*dist_to_center/wheel_r;
                let l = 85;

                ctx.fillStyle = `hsl(${h}, ${s}%, ${l}%)`;
                ctx.fillRect(x_cvs, y_cvs, 1, 1);
            }
        }
    }
    return [ctx, wheel_center_x, wheel_center_y, wheel_r];
}

function hsl_sl_rect(margin) {
    const canvas = document.getElementById("hsl-wheel-2");
    const ctx = canvas.getContext("2d");

    const canvas_w = canvas.clientWidth;
    const canvas_h = canvas.clientHeight;

    const rect_w = canvas_w - 2 * margin;
    const rect_h = canvas_h - 2 * margin;

    const x_min_rect = margin;
    const x_max_rect = margin + rect_w;
    const y_min_rect = margin;
    const y_max_rect = margin + rect_h;

    for (let x_cvs = x_min_rect; x_cvs < x_max_rect; x_cvs++) {
        for (let y_cvs = y_min_rect; y_cvs < y_max_rect; y_cvs++) {
            // X vers la droite
            // Y vers le bas

            let h = 0;
            let s = mapRange(x_cvs, x_min_rect, x_max_rect, 0, 80);
            let l = 100 - mapRange(y_cvs, y_min_rect, y_max_rect, 20, 80);

            ctx.fillStyle = `hsl(${h}, ${s}%, ${l}%)`;
            ctx.fillRect(x_cvs, y_cvs, 1, 1);
        }
    }
    return [ctx, x_min_rect, x_max_rect, y_min_rect, y_max_rect];
}

function colors_on_hsl_hs_wheel(colors, ctx, wheel_center_x, wheel_center_y, wheel_r) {
    colors.forEach(c => {
        const angle = c.h * Math.PI / 180;
        const radius = c.s * wheel_r;

        const x = wheel_center_x + Math.cos(angle) * radius;
        const y = wheel_center_y - Math.sin(angle) * radius;

        ctx.beginPath();
        ctx.fillStyle = c.css;
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    });
}

function colors_on_hsl_sl_rect(colors, ctx, rect_x_min, rect_x_max, rect_y_min, rect_y_max) {
    colors.forEach(c => {
        const x = mapRange(c.s, 0, 1, rect_x_min, rect_x_max);
        const y = mapRange(c.l, 0, 1, rect_y_max, rect_y_min);

        ctx.beginPath();
        ctx.fillStyle = c.css;
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    });
}

async function oklch_ch_wheel(margin) {
    const canvas = document.getElementById("oklch-wheel-1");
    const ctx = canvas.getContext("2d");

    const canvas_w = canvas.clientWidth;
    const canvas_h = canvas.clientHeight;

    const wheel_w = canvas_w - 2 * margin;
    const wheel_h = canvas_h - 2 * margin;
    const wheel_r = Math.min(wheel_w, wheel_h)/2;

    const wheel_center_x = canvas_w  / 2;
    const wheel_center_y = canvas_h / 2;

    const saved = localStorage.getItem("oklch-colorwheel_1");

    if (saved) {
        const img = await loadImage(saved);
        ctx.drawImage(img, 0, 0);
    } else {
        const x_min_wheel = wheel_center_x - wheel_r;
        const x_max_wheel = wheel_center_x + wheel_r;
        const y_min_wheel = wheel_center_y - wheel_r;
        const y_max_wheel = wheel_center_y + wheel_r;

        for (let x_cvs = x_min_wheel; x_cvs < x_max_wheel; x_cvs++) {
            for (let y_cvs = y_min_wheel; y_cvs < y_max_wheel; y_cvs++) {
                // X vers la droite
                // Y vers le bas
                
                let x_wrt_center = x_cvs-wheel_center_x;
                let y_wrt_center = y_cvs-wheel_center_y;
                let dist_to_center = Math.sqrt((x_wrt_center)**2 + (y_wrt_center)**2);
                
                if (dist_to_center <= wheel_r) {
                    let h = -x_y_to_angle(x_wrt_center, y_wrt_center)
                    let c = mapRange(dist_to_center/wheel_r, 0, 1, 0, 0.09);
                    let l = 0.95;

                    ctx.fillStyle = `oklch(${l} ${c} ${h})`;
                    ctx.fillRect(x_cvs, y_cvs, 1, 1);
                }
            }
        }
        const data = canvas.toDataURL("image/png");
        localStorage.setItem("oklch-colorwheel_1", data);
    }
    return [ctx, wheel_center_x, wheel_center_y, wheel_r];
}


async function oklch_lc_rect(margin) {
    const canvas = document.getElementById("oklch-wheel-2");
    const ctx = canvas.getContext("2d");

    const canvas_w = canvas.clientWidth;
    const canvas_h = canvas.clientHeight;

    const rect_w = canvas_w - 2 * margin;
    const rect_h = canvas_h - 2 * margin;

    const x_min_rect = margin;
    const x_max_rect = margin + rect_w;
    const y_min_rect = margin;
    const y_max_rect = margin + rect_h;

    const saved = localStorage.getItem("oklch-colorwheel_2");

    if (saved) {
        const img = await loadImage(saved);
        ctx.drawImage(img, 0, 0);
    } else {
        for (let x_cvs = x_min_rect; x_cvs < x_max_rect; x_cvs++) {
            for (let y_cvs = y_min_rect; y_cvs < y_max_rect; y_cvs++) {
                // X vers la droite
                // Y vers le bas

                let h = 0;
                let c = mapRange(x_cvs, x_min_rect, x_max_rect, 0, 0.05);
                let l = mapRange(y_cvs, y_max_rect, y_min_rect, 0.15, 0.9);

                ctx.fillStyle = `oklch(${l} ${c} ${h})`;
                ctx.fillRect(x_cvs, y_cvs, 1, 1);
            }
        }

        const data = canvas.toDataURL("image/png");
        localStorage.setItem("oklch-colorwheel_2", data);
    }

    return [ctx, x_min_rect, x_max_rect, y_min_rect, y_max_rect];
}

function colors_on_oklch_ch_wheel(colors, ctx, wheel_center_x, wheel_center_y, wheel_r) {
    colors.forEach(c => {
        const angle = c.h * Math.PI / 180;
        const radius = c.c/0.37 * wheel_r;

        const x = wheel_center_x + Math.cos(angle) * radius;
        const y = wheel_center_y - Math.sin(angle) * radius;

        ctx.beginPath();
        ctx.fillStyle = c.css;
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    });
}

function colors_on_oklch_lc_rect(colors, ctx, rect_x_min, rect_x_max, rect_y_min, rect_y_max) {
    colors.forEach(c => {
        const x = mapRange(c.c, 0, 0.37, rect_x_min, rect_x_max);
        const y = mapRange(c.l, 0, 1, rect_y_max, rect_y_min);

        ctx.beginPath();
        ctx.fillStyle = c.css;
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
    });
}

function loadImage(src) {
    return new Promise(resolve => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.src = src;
    });
}

async function render_colorwheels(colors) {
    let margin = 50;

    const [wheel_ctx, cx, cy, r] = await oklch_ch_wheel(margin);
    colors_on_oklch_ch_wheel(colors, wheel_ctx, cx, cy, r);

    const [rect_ctx, x_min, x_max, y_min, y_max] = await oklch_lc_rect(margin);
    colors_on_oklch_lc_rect(colors, rect_ctx, x_min, x_max, y_min, y_max);
}

function oklchToXYZ(l, c, h) {
    const angle = h * Math.PI / 180;

    const radius = c;
    const y = l;

    const x = Math.cos(angle) * radius;
    const z = -Math.sin(angle) * radius;

    return {"x": x, "y": y, "z": z};
}

