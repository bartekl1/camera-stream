document.querySelector("#fullscreen-button").addEventListener("click", () => {
    document.querySelector("#camera-image").requestFullscreen();
});

console.log(
    "%cCamera Stream\n\n%cby @bartekl1\nv. 1.0\n\n%chttps://github.com/bartekl1/camera-stream",
    "font-size: 36px; font-weight: 600;",
    "font-size: 16px;",
    "font-size: 14px;"
);
