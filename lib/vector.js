/*
  (2D) TWO DIMENSIONAL VECTORS
*/

// NOTE: Entering a single number for functions that expect a vector will sustitute both components with that number!

Vector2 = function(x, y)
{
	if (typeof x === "number" && typeof y === "number") // Both parameters are entered
	{
		this.x = x;
		this.y = y;
	}
	else if (typeof x === "number" && typeof y !== "number") // Only one parameter is entered
	{
		this.x = x;
		this.y = x;
	}
	else // No parameters are entered
	{
		this.x = 0;
		this.y = 0;
	}
}

// Returns the vector in string format. E.G. "vec2(1, -2)"
Vector2.prototype.toString = function()
{
	return "vec2(" + this.x + ", " + this.y + ")";
}

// Adding values to the vector
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.add = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(this.x + arg1, this.y + arg2);
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(this.x + arg1, this.y + arg1);
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(this.x + arg1.x, this.y + arg1.y);
	}
	else
	{
		return this;
	}
}

// Subtracting values from the vector
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.sub = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(this.x - arg1, this.y - arg2);
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(this.x - arg1, this.y - arg1);
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(this.x - arg1.x, this.y - arg1.y);
	}
	else
	{
		return this;
	}
}

// Multiplying the vector by a number, two numbers or another vector
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.mul = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(this.x * arg1, this.y * arg2);
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(this.x * arg1, this.y * arg1);
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(this.x * arg1.x, this.y * arg1.y);
	}
	else
	{
		return this;
	}
}

// Dividing the vector by a number, two numbers or another vector
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.div = function(arg1, arg2) 
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(this.x / arg1, this.y / arg2);
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(this.x / arg1, this.y / arg1);
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(this.x / arg1.x, this.y / arg1.y);
	}
	else
	{
		return this;
	}
}

// Rounds the components of the vector up
// Takes no arguments OR a number OR two numbers OR a Vector2
Vector2.prototype.ceil = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(Math.ceil(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.ceil(this.y * Math.pow(10, arg2)) / Math.pow(10, arg2));
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(Math.ceil(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.ceil(this.y * Math.pow(10, arg1)) / Math.pow(10, arg1));
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(Math.ceil(this.x * Math.pow(10, arg1.x)) / Math.pow(10, arg1.x), Math.ceil(this.y * Math.pow(10, arg1.y)) / Math.pow(10, arg1.y));
	}
	else
	{
		return new Vector2(Math.ceil(this.x), Math.ceil(this.y));
	}
}

// Rounds the components of the vector down
// Takes no arguments OR a number OR two numbers OR a Vector2
Vector2.prototype.floor = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(Math.floor(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.floor(this.y * Math.pow(10, arg2)) / Math.pow(10, arg2));
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(Math.floor(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.floor(this.y * Math.pow(10, arg1)) / Math.pow(10, arg1));
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(Math.floor(this.x * Math.pow(10, arg1.x)) / Math.pow(10, arg1.x), Math.floor(this.y * Math.pow(10, arg1.y)) / Math.pow(10, arg1.y));
	}
	else
	{
		return new Vector2(Math.floor(this.x), Math.floor(this.y));
	}
}

// Rounds the components of the vector to the nearest number
// Takes no arguments OR a number OR two numbers OR a Vector2
Vector2.prototype.round = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(Math.round(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.round(this.y * Math.pow(10, arg2)) / Math.pow(10, arg2));
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return new Vector2(Math.round(this.x * Math.pow(10, arg1)) / Math.pow(10, arg1), Math.round(this.y * Math.pow(10, arg1)) / Math.pow(10, arg1));
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(Math.round(this.x * Math.pow(10, arg1.x)) / Math.pow(10, arg1.x), Math.round(this.y * Math.pow(10, arg1.y)) / Math.pow(10, arg1.y));
	}
	else
	{
		return new Vector2(Math.round(this.x), Math.round(this.y));
	}
}

// Gets the modulus of the components of the vector
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.mod = function(arg1, arg2)
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return new Vector2(this.x % arg1, this.y % arg2);
	}
	else if (typeof arg1 === "number" && arg2 !== "number")
	{
		return new Vector2(this.x % arg1, this.y % arg1);
	}
	else if (arg1.constructor == Vector2)
	{
		return new Vector2(this.x % arg1.x, this.y % arg1.y);
	}
	else
	{
		return this;
	}
}

// Gets the distance between two vectors.
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.distance = function(arg1, arg2) 
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return Math.sqrt((this.x - arg1) * (this.x - arg1) + (this.y - arg2) * (this.y - arg2));
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return Math.sqrt((this.x - arg1) * (this.x - arg1) + (this.y - arg1) * (this.y - arg1));
	}
	else if (arg1.constructor == Vector2)
	{
		return Math.sqrt((this.x - arg1.x) * (this.x - arg1.x) + (this.y - arg1.y) * (this.y - arg1.y));
	}
	else
	{
		return 0;
	}
}

// Gets the magnitude (or length) of the vector
Vector2.prototype.magnitude = function()
{
	return this.distance(0);
}

// Same as magnitude, just a different name
Vector2.prototype.length = Vector2.prototype.magnitude;

// Gets the normal of a vector
Vector2.prototype.getNormal = function()
{
	return this.div(this.magnitude());
}

// Gets the dot product of the vector and arguments
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.dot = function(arg1, arg2) 
{
	if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		return this.x * arg1 + this.y * arg2;
	}
	else if (typeof arg1 === "number" && typeof arg2 !== "number")
	{
		return this.x * arg1 + this.y * arg1;
	}
	else if (arg1.constructor == Vector2)
	{
		return this.x * arg1.x + this.y * arg1.y;
	}
	else
	{
		return this;
	}
}

// Returns the vector with the shortest length
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.min = function(arg1, arg2)
{
	var vec2 = new Vector2();

	if(arg1.constructor == Vector2)
	{
		vec2 = arg1;
	}
	else if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		vec2 = new Vector2(arg1, arg2);
	}
	else if(typeof arg2 === "number" && typeof arg2 !== "number")
	{
		vec2 = new Vector2(arg1, arg1);
	}
	else
	{
		return this;
	}

	var length1 = this.magnitude();
	var length2 = vec2.magnitude();

	return length1 > length2 ? length2 : length1;
}

// Returns the vector with the largest length
// Takes a number OR two numbers OR a Vector2
Vector2.prototype.max = function(arg1, arg2)
{
	var vec2 = new Vector2();

	if(arg1.constructor == Vector2)
	{
		vec2 = arg1;
	}
	else if (typeof arg1 === "number" && typeof arg2 === "number")
	{
		vec2 = new Vector2(arg1, arg2);
	}
	else if(typeof arg2 === "number" && typeof arg2 !== "number")
	{
		vec2 = new Vector2(arg1, arg1);
	}
	else
	{
		return this;
	}

	var length1 = this.magnitude();
	var length2 = vec2.magnitude();

	return length1 < length2 ? length2 : length1;
}

// Rotates the vector around a given vector, at a given angle, in radians. Can be clockwise or counterclockwise
// Takes a vector, an angle and, optionally, a bool to determine if it's clockwise or not
Vector2.prototype.rotate = function(vec2, ang)
{
	if (vec2.constructor == Vector2 && typeof ang === "number")
	{
		var curX = this.x - vec2.x;
		var curY = this.y - vec2.y;

		var angCurrent = Math.atan2(curY, curX);

		var angToRotate = angCurrent + ang;

		var x = vec2.x + Math.cos(angToRotate) * this.distance(vec2);
		var y = vec2.y + Math.sin(angToRotate) * this.distance(vec2);

		return new Vector2(x, y);
	}
}
