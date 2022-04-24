console.log("javascript loading")


function _all(q, e = document) { return e.querySelectorAll(q) }

function _one(q, e = document) { return e.querySelector(q) }



// Toggle modal
function toggleImageUpload() {
    _one("#imageUploadModal").classList.toggle("hidden")
}

// Toggle modal
function toggleModal() {
    console.log('toggle')
    _one("#user-modal").classList.toggle("invisible")
    _one("#arrow-turn").classList.toggle("-scale-y-[1]")
    _one("#background-screen").classList.toggle("hidden")
}




// Resize textarea based on content 
const tx = _all("textarea");
for (let i = 0; i < tx.length; i++) {
    tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
    tx[i].addEventListener("input", OnInput, false);
}

function OnInput(e) {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
}



// Go back to previous page
// onclick="history.go(-1)"