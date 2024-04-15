document.addEventListener('DOMContentLoaded', function() { 
    shoppingListArray = [];

    let shoppingListCount = document.getElementById("shopping-list-count");
    shoppingListCount.addEventListener("change", shoppingListCount_Change)
    shoppingListCount_Change({target: shoppingListCount});

    let i = 3;
    while (i > 0) {
        addShoppingItem();
        i--;
    }
});

// Events
function shoppingListAmount_Change(e) {
    let index = getIndexFromElement(e.target.parentElement);
    let thisShoppingItem = shoppingListArray[index];
    let originalAmount = thisShoppingItem.amount;
    let amount = Number(e.target.value);

    if (amount < 0) {
        amount = 0;
        e.target.setAttribute("value", amount);
        e.target.value = amount;
    }

    if (amount == NaN) {
        amount = originalAmount;
        e.target.setAttribute("value", amount);
    }

    thisShoppingItem.amount = amount;
}

function shoppingListName_Change(e) {
    let index = getIndexFromElement(e.target.parentElement);
    let name = e.target.value;

    let thisShoppingItem = shoppingListArray[index];
    thisShoppingItem.name = name;
}

function shoppingListCount_Change(e) {
    e.target.disabled = true;
    // A VERY hacky implementation of "data binding"
    // If the user changes the number of subjects we
    // need to create/destroy fields and keep our
    // array up to date

    let originalCount = Number(shoppingListArray.length);
    let newCount = Number(e.target.value);

    //console.log("Original: " + originalCount + ", new: " + newCount);

    if (newCount > originalCount) {
        // Create new subjects if we go from
        // a low number of subjects to a
        // higher amount of subjects
        let n = originalCount;
        while (n < newCount) {
            addShoppingItem();
            n++;
        }
    } else if (newCount < originalCount) {
        // Inversely, pop items from the array if 
        // we go from a high number to a low number
        let n = originalCount;
        while (n > newCount) {
            deleteShoppingItem(shoppingListArray.length-1);
            n--;
        }
    }

    e.target.disabled = false;
}

function addShoppingItem_OnClick(sender) {
    addShoppingItem();
}

function deleteShoppingItem_OnClick(sender) {
    let index = getIndexFromElement(sender.parentElement);
    deleteShoppingItem(index);
}

// Methods
function reconstructListHTML() {
    let innerHTML = "";
    
    let shoppingListCount = document.getElementById("shopping-list-count");
    shoppingListCount.setAttribute("value", shoppingListArray.length);
    shoppingListCount.value = shoppingListArray.length;
    
    for (let i = 0; i < shoppingListArray.length; i++) {
        innerHTML += getSubjectHTML(i);
    }

    let column = document.getElementById("shopping-list-column");
    column.innerHTML = innerHTML;

    // Now we will re-construct the innerHTML of the column
    let shoppingListAmounts = document.getElementsByClassName("shopping-list-amount-input");
    let shoppingListNames = document.getElementsByClassName("shopping-list-name-input");

    // Need to re-apply event handlers after changing HTML
    for (let i = 0; i < shoppingListNames.length; i++) {
        // Maintain the values of the nodes
        shoppingListNames[i].setAttribute("value", shoppingListArray[i].name);
        shoppingListAmounts[i].setAttribute("value", shoppingListArray[i].amount);

        shoppingListAmounts[i].removeEventListener("change", shoppingListAmount_Change);
        shoppingListAmounts[i].addEventListener("change", shoppingListAmount_Change);
        shoppingListNames[i].removeEventListener("change", shoppingListName_Change);
        shoppingListNames[i].addEventListener("change", shoppingListName_Change);
    }
}

function getIndexFromElement(element) {
    // Extract the index from the ID
    // e.g. "result-1" -> 1
    let components = element.id.split("-");
    return Number(components[components.length-1]);
}

function addShoppingItem() {
    let index = shoppingListArray.length;

    shoppingListArray[index] = {
        name: "",
        amount: 0
    };

    reconstructListHTML();
}

function deleteShoppingItem(index) {
    if (index >= 0 && index < shoppingListArray.length) {
        shoppingListArray.splice(index, 1);
    }
    
    reconstructListHTML();
}

function getSubjectHTML(index) {
    let id = "item-" + String(index);
    let innerHTML = "";

    innerHTML += "<div id='" + id + "' class='d-flex justify-content-center align-items-center'>\n";
    innerHTML += "<ul class='ul-shopping-list'><li class='li-shopping-list'></li></ul>";
    innerHTML += "<input class='shopping-list-name-input col-12 col-md-8' type='text'>";
    innerHTML += "\n<input class='shopping-list-amount-input' type='number'>";
    innerHTML += "<button class='button-delete-subject' onclick='deleteShoppingItem_OnClick(this)'>";
    innerHTML += "<img src='../../media/images/emoji-cross-mark-w10.png' class='img-delete-subject'></button>";
    innerHTML += "</div>";
    
    return innerHTML;
}