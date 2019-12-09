"use strict";

class Vector {

    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    static diff(v1, v2) {
        return new Vector(v1.x - v2.x, v1.y - v2.y);
    }

    static add(v1, v2) {
        return Vector(v1.x + v2.x, v1.y + v2.y);
    }

    add(v) {
        this.x += v.x;
        this.y += v.y;
        return this;
    }

    mult(factor) {
        this.x *= factor;
        this.y *= factor;
        return this;
    }

    setValue(x, y) {
        this.x = x;
        this.y = y;
    }

    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    normalize() {
        var magnitudeVal = this.magnitude();
        this.x /= Math.abs(magnitudeVal);
        this.y /= Math.abs(magnitudeVal);
        return this;
    }

    truncate(maxValue) {
        var magnitudeVal = this.magnitude();
        if (magnitudeVal > maxValue) {
            this.normalize();
            this.mult(maxValue);
        }
        return this;
    }

    get key() {
        return Math.floor(this.x) + "|" + Math.floor(this.y);
    }
}
