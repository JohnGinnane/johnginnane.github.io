function check_grid(_grid, _x, _y, _start) {
	var j = 1;

	if (Number.isInteger(_start)) {
		if (_start > 0) {
			j = _start;
		}
	}

	for (j; j < _grid.length; j++) {
		if (_grid[j].x == _x && _grid[j].y == _y) {
			//console.log("something in " + _x + ", " + _y)
			return j;
		}
	}

	//console.log("nothing in " + _x + ", " + _y)
	return 0;
}

function dist_to_cell(_grid, _num) {
	return Math.abs(_grid[_num].x) + Math.abs(_grid[_num].y);
}

var print_percent = 0

function generate_spiral(_num) {
	var start_time = Date.now();
	var cur_x = 0;
	var cur_y = 0;
	var check_headstart = 1;

	// Move counter clockwise
	var direction = "right";

	grid[1] = {x:0, y:0, num:1};

	for (i = 2; i <= _num; i++) {
		// stupid percent loading thingy
		if (_num > 100 && grid.length > print_percent) {
			var prc = Math.floor(100 / _num * grid.length);

			// Only every 10%
			if (prc % 10 == 0) {
				console.log("Generating spiral... " + prc + "%");

				print_percent = (_num / 100) * (prc + 1);
			}
		}

		switch (direction) {
			case "right":
				cur_x = cur_x+1;
				check_headstart = check_grid(grid, cur_x, cur_y+1, check_headstart);

				if (check_headstart == 0) {
					direction = "up";
					//console.log(i + ": (" + cur_x + ", " + cur_y + ") moving " + direction);
				}

				break;
			case "up":
				cur_y = cur_y+1;
				check_headstart = check_grid(grid, cur_x-1, cur_y, check_headstart);

				if (check_headstart == 0) {
					direction = "left";
					//console.log(i + ": (" + cur_x + ", " + cur_y + ") moving " + direction);
				}

				break;
			case "left":
				cur_x = cur_x-1;
				check_headstart = check_grid(grid, cur_x, cur_y-1, check_headstart);

				if (check_headstart == 0) {
					direction = "down";
					//console.log(i + ": (" + cur_x + ", " + cur_y + ") moving " + direction);
				}

				break;
			case "down":
				cur_y = cur_y-1;
				check_headstart = check_grid(grid, cur_x+1, cur_y, check_headstart);

				if (check_headstart == 0) {
					direction = "right";
					//console.log(i + ": (" + cur_x + ", " + cur_y + ") moving " + direction);
				}

				break;
		}

		//console.log("entered in (" + cur_x + ", " + cur_y + ") = " + i + " now heading " + direction)
		grid[i] = {x:cur_x, y:cur_y, num:i}
	}

	var end_time = Date.now()

	// Idea of how long it took
	console.log((end_time - start_time) / 1000);
}

//generate_spiral(277678);
generate_spiral(300000);