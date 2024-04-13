document.addEventListener('DOMContentLoaded', function(){ 
    let body = document.getElementById("lab9-column");
    let newLine = "";
    let originalBottles = 99;
    let bottles = originalBottles;

    // We use a "-1" so that when we're all out of bottles we can say "no more..."
    while (bottles > -1) {
        if (bottles > 0) {
            newLine = bottles + " bottle" + (bottles > 1 ? "s" : "") + " beer on the wall, " + bottles + " bottle" + (bottles > 1 ? "s" : "") + " of beer<br>";
            bottles--;
            newLine += "Take one down and pass it around, " + (bottles > 0 ? bottles : "no more") + " bottle" + (bottles == 1 ? "" : "s") + " of beer on the wall<br><br>";
        } else {
            newLine = "No more bottles of beer on the wall, no more bottles of beer<br>";
            newLine += "Go to the store and buy some more, " + originalBottles + " bottles of beer on the wall";
            bottles--;
        }

        body.innerHTML += newLine;
    }
}, false);