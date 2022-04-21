console.log("javascript loading hello")


function _all(q, e=document){return e.querySelectorAll(q)}
function _one(q, e=document){return e.querySelector(q)}


function toggleImageUpload(){
  _one("#imageUploadModal").classList.toggle("hidden")
}



// Resize textarea based on content 
const tx = _all("textarea");
for (let i = 0; i < tx.length; i++) {
  console.log("calami")
  tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
  tx[i].addEventListener("input", OnInput, false);
}

function OnInput(e) {
  console.log("oninput")
  this.style.height = "auto";
  this.style.height = (this.scrollHeight) + "px";
}