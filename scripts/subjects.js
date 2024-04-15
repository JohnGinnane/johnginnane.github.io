document.addEventListener('DOMContentLoaded', function(){ 
    subjectsArray = [];

    let subjectCount = document.getElementById("subject-count");
    subjectCount.addEventListener("change", subjectCount_Change)
    subjectCount_Change({target: subjectCount});
});

// Events
function subjectResult_Change(e) {
    let index = getIndexFromElement(e.target.parentElement);
    let thisSubject = subjectsArray[index];
    let originalResult = thisSubject.result;
    let result = Number(e.target.value);

    if (result < 0) {
        result = 0;
        e.target.setAttribute("value", result);
        e.target.value = result;
    } else if (result > 100) {
        result = 100;
        e.target.setAttribute("value", result);
        e.target.value = result;
    }

    if (result == NaN) {
        result = originalResult;
        e.target.setAttribute("value", result);
    }

    thisSubject.result = result;

    calculateSummary();
}

function subjectName_Change(e) {
    let index = getIndexFromElement(e.target.parentElement);
    let name = e.target.value;

    let thisSubject = subjectsArray[index];
    thisSubject.name = name;

    calculateSummary();
}

function subjectCount_Change(e) {
    e.target.disabled = true;
    // A VERY hacky implementation of "data binding"
    // If the user changes the number of subjects we
    // need to create/destroy fields and keep our
    // array up to date

    let originalCount = Number(subjectsArray.length);
    let newCount = Number(e.target.value);

    //console.log("Original: " + originalCount + ", new: " + newCount);

    if (newCount > originalCount) {
        // Create new subjects if we go from
        // a low number of subjects to a
        // higher amount of subjects
        let n = originalCount;
        while (n < newCount) {
            addSubject();
            n++;
        }
    } else if (newCount < originalCount) {
        // Inversely, pop items from the array if 
        // we go from a high number to a low number
        let n = originalCount;
        while (n > newCount) {
            deleteSubject(subjectsArray.length-1);
            n--;
        }
    }

    e.target.disabled = false;
}

function addSubject_OnClick(sender) {
    addSubject();
}

function deleteSubject_OnClick(sender) {
    let index = getIndexFromElement(sender.parentElement);
    deleteSubject(index);
}

// Methods
function reconstructListHTML() {
    let innerHTML = "";
    
    let subjectCount = document.getElementById("subject-count");
    subjectCount.setAttribute("value", subjectsArray.length);
    subjectCount.value = subjectsArray.length;
    
    for (let i = 0; i < subjectsArray.length; i++) {
        // subjectNames[i].setAttribute("value", subjectsArray[i].name);
        // subjectResults[i].setAttribute("value", subjectsArray[i].result);

        // innerHTML += "<div id='item-'" + i + "' class='d-flex justify-content-center align-items-center'>\n";
        // innerHTML += subjectNames[i].outerHTML;
        // innerHTML += "\n";
        // innerHTML += subjectResults[i].outerHTML;
        // innerHTML += "% - <span id='result-grade-" + i + "' class='result-grade'></span><br>";
        // innerHTML += "<button id='button-delete-" + i + "' class='button-delete-subject' onclick='deleteSubject(this)'>";
        // innerHTML += "<img src='../../media/images/emoji-cross-mark-w10.png' class='img-delete-subject'></button>";
        // innerHTML += "</div>";

        innerHTML += getSubjectHTML(i);
    }

    let column = document.getElementById("subjects-column");
    column.innerHTML = innerHTML;

    // Now we will re-construct the innerHTML of the column
    let subjectResults = document.getElementsByClassName("subject-result-input");
    let subjectNames = document.getElementsByClassName("subject-name-input");

    // Need to re-apply event handlers after changing HTML
    for (let i = 0; i < subjectNames.length; i++) {
        // Maintain the values of the nodes
        subjectNames[i].setAttribute("value", subjectsArray[i].name);
        subjectResults[i].setAttribute("value", subjectsArray[i].result);

        subjectResults[i].removeEventListener("change", subjectResult_Change);
        subjectResults[i].addEventListener("change", subjectResult_Change);
        subjectNames[i].removeEventListener("change", subjectName_Change);
        subjectNames[i].addEventListener("change", subjectName_Change);
    }

    calculateSummary();    
}

function getIndexFromElement(element) {
    // Extract the index from the ID
    // e.g. "result-1" -> 1
    let components = element.id.split("-");
    return Number(components[components.length-1]);
}

function calculateSummary() {
    let total = 0;

    for (let i = 0; i < subjectsArray.length; i++) {
        let subject = subjectsArray[i];

        if (subject) {
            total += subject.result;

            // Set the appropriate grade for the result
            let itemID = "#item-" + String(i);
            let divSubject = document.querySelector(itemID);
            let spanGrade = divSubject.querySelector(".result-grade");
            spanGrade.innerHTML = getGradeForResult(subject.result);
        }
    }

    let spanSummary = document.getElementById("lab9-total");

    if (subjectsArray.length > 0) {
        total /= subjectsArray.length;
    }
    
    spanSummary.innerHTML = total.toFixed(2) + "%";
}

function getGradeForResult(result) {
    let resultNum = Number(result);
    if (resultNum == NaN) { return ""; }

    if (resultNum >= 85) {
        return "A";
    } else if (resultNum >= 70) {
        return "B";
    } else if (resultNum >= 55) {
        return "C";
    } else if (resultNum >= 40) {
        return "D";
    } else if (resultNum >= 25) {
        return "E";
    } else if (resultNum >= 10) {
        return "F";
    } else {
        return "NG";
    }
}

function addSubject() {
    let index = subjectsArray.length;

    subjectsArray[index] = {
        name: "",
        result: 0};

    reconstructListHTML();
}

function deleteSubject(index) {
    console.log("removing #" + index + " from a list of " + subjectsArray.length);
    if (index >= 0 && index < subjectsArray.length) {
        subjectsArray.splice(index, 1);
    }
    
    reconstructListHTML();
}

function getSubjectHTML(index) {
    // let newHTML = "<input id='name-" + id + "' class='subject-name-input' type='text'>";
    // newHTML += "\n<input id='result-" + id + "' class='subject-result-input' type='number'>";

    // let column = document.getElementById("lab9-column");
    // column.innerHTML += newHTML;

    let id = "item-" + String(index);
    let innerHTML = "";

    innerHTML += "<div id='" + id + "' class='subject-div d-flex justify-content-center align-items-center'>\n";
    innerHTML += "<input class='subject-name-input' type='text'>"
    innerHTML += "\n<input class='subject-result-input' type='number'>";
    innerHTML += "% - <span class='result-grade'>" + getGradeForResult(subjectsArray[index].result) + "</span><br>";
    innerHTML += "<button class='button-delete-subject' onclick='deleteSubject_OnClick(this)'>";
    innerHTML += "<img src='../../media/images/emoji-cross-mark-w10.png' class='img-delete-subject'></button>";
    innerHTML += "</div>";
    
    return innerHTML;
}