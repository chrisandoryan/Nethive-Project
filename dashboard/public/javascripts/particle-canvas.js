"use strict";

let lastTime = performance.now(),
    fps = 0;

function ParticleCanvas(canvas, mousePosition) {
    this.mousePosition      = mousePosition;

    this.context            = canvas.getContext('2d');
    this.canvasSize         = new Vector(canvas.width, canvas.height);
    this.chunkSize          = new Vector(100, 100);
    this.particleList       = [];
    this.particleChunkMap   = [];
}

ParticleCanvas.prototype = {

    get TOTAL_PARTICLE() { return 100; },

    getRandomPosition: function () {
        return new Vector(Math.random() * this.canvasSize.x, Math.random() * this.canvasSize.y);
    },

    init: function () {
        for (var i = 0; i < this.TOTAL_PARTICLE; i++) {
            this.particleList.push(
                new Particle(this.getRandomPosition(), this.mousePosition, this.canvasSize,
                    this.particleChunkMap, this.chunkSize));
        }

        var totalRow = this.canvasSize.y / this.chunkSize.y;
        var totalCol = this.canvasSize.x / this.chunkSize.x;
        for (var row = 0; row < totalRow; row++) {
            this.particleChunkMap[row] = [];
            for (var col = 0; col < totalCol; col++) {
                this.particleChunkMap[row][col] = [];
            }
        }
    },

    clearChunkMap: function () {
        this.particleChunkMap.forEach(function (row) {
            row.forEach(function (chunk) {
                chunk.splice(0, chunk.length);
            });
        });
    },

    setParticleInChunk: function () {
        var particleChunkMap = this.particleChunkMap,
            chunkSize = this.chunkSize;
        this.particleList.forEach(function (particle) {
            var row = Math.floor(particle.position.y / chunkSize.y);
            var col = Math.floor(particle.position.x / chunkSize.x);
            particleChunkMap[row][col].push(particle);
        });
    },

    draw: function (bool) {

        var now = performance.now(),
            shouldRender = true;

        if (now - lastTime > 1000) {
            // console.log(`particle canvas render: ${fps} fps`);
            // if (fps < 30) shouldRender = false;
            fps = 0;
            lastTime = now;
        }
        fps++;

        var ctx = this.context;
        this.clearChunkMap();
        this.setParticleInChunk();
        this.particleList.forEach(function (particle) { particle.clear(ctx); });
        this.particleList.forEach(function (particle) { particle.update(ctx); });
        this.particleList.forEach(function (particle) { particle.draw(ctx); });

        if(shouldRender)
            requestAnimationFrame(this.draw.bind(this));
    }

}


