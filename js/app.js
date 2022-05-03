console.log("javascript loading")


function _all(q, e = document) { return e.querySelectorAll(q) }

function _one(q, e = document) { return e.querySelector(q) }



// Toggle modal
function toggleImageUpload() {
    _one("#imageUploadModal").classList.toggle("hidden")
}

// Toggle user modal
function toggleUserModal() {
    console.log('toggle')
    _one("#user-modal").classList.toggle("invisible")
    _one("#arrow-turn").classList.toggle("scale-y-mirror")
    _one("#background-screen").classList.toggle("hidden")
}

// Toggle modal
function toggleTweetModal() {
    console.log('toggletweetmodal')
    _one("#tweet-modal").classList.toggle("hidden")
    _one("#background-tweet-screen").classList.toggle("hidden")
}

// Toggle user any modal
function toggleUserAnyModal() {
    console.log('toggle')
    _one("#user-any-modal").classList.toggle("hidden")
    _one("#background-user-any-screen").classList.toggle("hidden")
}


// Resize textarea based on content 
const tx = _all("textarea");
console.log(tx)
for (let i = 0; i < tx.length; i++) {
    tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
    tx[i].addEventListener("input", OnInput, false);
}

function OnInput(e) {
    console.log(this)
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
}



// Go back to previous page
// onclick="history.go(-1)"