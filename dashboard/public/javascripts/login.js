"use strict";

var canvas = document.getElementById("myCanvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var mousePosition = new Vector(0, 0);
window.onmousemove = function (e) {
    mousePosition.setValue(e.clientX, e.clientY);
};

var particleCanvas = new ParticleCanvas(canvas, mousePosition);
particleCanvas.init();
particleCanvas.draw();

