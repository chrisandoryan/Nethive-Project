"use strict";

class Particle {

    constructor(position, mousePosition, ub, particleMap, chunkSize) {
        this.position = position;
        this.mousePosition = mousePosition;
        this.ub = ub;
        this.particleMap = particleMap;
        this.chunkSize = chunkSize;

        this.radius = 1;
        this.radiusLb = this.radius + 1;
        this.radiusUb = (this.radius + 1) * 2;
        this.maxSpeed = Math.random() * 1.0;
        this.maxForce = .01;
        this.velocity = new Vector(Math.random() * 20 - 10, Math.random() * 20 - 10);
        this.acceleration = new Vector(0, 0);

        this.deleteLineDataQueue = [];
        this.drawedLines = {};
    }

    update() {
        this.velocity.add(this.acceleration);
        this.velocity.truncate(this.maxSpeed);
        this.position.add(this.velocity);
        this.acceleration.mult(0);

        if (this.position.x > this.ub.x) this.position.x = 0;
        else if (this.position.x < 0) this.position.x = this.ub.x;

        if (this.position.y > this.ub.y) this.position.y = 0;
        else if (this.position.y < 0) this.position.y = this.ub.y;

        return this;
    }

    clear(ctx) {
        ctx.clearRect(this.position.x - this.radiusLb, this.position.y - this.radiusLb, this.radiusUb, this.radiusUb);

        this.deleteLineDataQueue
            .splice(0, this.deleteLineDataQueue.length)
            .forEach(function (data) {
                ctx.save();
                ctx.translate(data.x, data.y);
                ctx.rotate(data.degInRad);
                ctx.clearRect(0, -2, data.mag, 4);
                ctx.restore();

                if (data.end)
                    for (var key in data.end.drawedLines[data.positionKey])
                        delete data.end.drawedLines[data.positionKey][key];
            });
    }

    draw(ctx) {
        let mag = Vector.diff(this.mousePosition, this.position).magnitude();
        if (mag < 150) {
            ctx.strokeStyle = 'rgba(154, 204, 20, ' + ((150 - mag) / 300) + ')';
            this.drawLine(ctx, this.position, this.mousePosition);
            //this.moveTo(this.mousePosition);
            ctx.fillStyle = 'rgba(154, 204, 20, '+ (0.5 + ((150 - mag) / 300)) +')';
        } else {
            ctx.fillStyle = 'rgba(149, 199, 15, 0.5)';
        }

        var row = Math.floor(this.position.y / this.chunkSize.y);
        var col = Math.floor(this.position.x / this.chunkSize.x);
        for (var i = Math.max(row - 1, 0) ; i <= row + 1; i++) {

            if (!this.particleMap[i]) continue;

            for (var j = Math.max(col - 1, 0) ; j <= col + 1; j++) {
                if (!this.particleMap[i][j] || this.particleMap[i][j].length == 0) continue;

                this.particleMap[i][j].forEach(particle => {
                    if (particle.position == this.position) return;
                    else if (this.drawedLines[particle.position.key] == true) return;

                    let mag = Vector.diff(particle.position, this.position).magnitude();

                    if (mag < this.chunkSize.x) {
                        ctx.strokeStyle = 'rgba(154, 204, 20, '+ ((this.chunkSize.x - mag) / this.chunkSize.x) + ')';
                               
                        particle.drawedLines[this.position.key] = true;
                        this.drawLine(ctx, this.position, particle.position);
                        this.deleteLineDataQueue[this.deleteLineDataQueue.length - 1]['end'] = particle;
                        this.deleteLineDataQueue[this.deleteLineDataQueue.length - 1]['positionKey'] = this.position.key;
                    }
                });
            }
        }

        ctx.beginPath();
        ctx.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
    }

    drawLine(ctx, start, end) {
        var degInRad = this._getDegInRad(start, end);
        var mag = Vector.diff(end, start).magnitude();
        ctx.beginPath();
        ctx.moveTo(start.x, start.y);
        ctx.lineTo(end.x, end.y);
        ctx.stroke();

        this.deleteLineDataQueue.push({
            degInRad: degInRad,
            x: start.x,
            y: start.y,
            mag: mag
        });
    }

    _getDegInRad(v1, v2) {
        var deg = Math.atan((v2.y - v1.y) / (v2.x - v1.x));
        if (v2.x < v1.x) deg += Math.PI;
        return deg;
    }

    moveTo(targetPosition) {
        var desired = Vector.diff(targetPosition, this.position);
        desired.normalize().mult(this.maxSpeed);

        var steer = Vector.diff(desired, this.velocity);
        steer.truncate(this.maxForce);
        this.acceleration.add(steer);
    }

}