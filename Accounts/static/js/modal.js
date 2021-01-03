let modal = document.getElementById("myModal");
let modalImg = document.getElementById("img01");
let captionText = document.getElementById("caption");
let span = document.querySelector("#close_img");
let hoverImgs = document.querySelectorAll('.hover-img')

for(let h of hoverImgs){
  h.onclick = function() {
    modal.style.display = "block";
    modalImg.src = h.src;
    captionText.innerHTML = h.alt;

    span.onclick = function () {
      modal.style.display = "none";
    };
    modal.onclick = function(){
      modal.style.display = "none";
    }
  }
}
