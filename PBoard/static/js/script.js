function colorNumber(e){
  let value = parseFloat(e.innerHTML);
  e.style.color = "red";
  if (value >= 2.5) {
    e.style.color = "#EE5B1C";
  }
  if (value == 5) {
    e.style.color = "yellow";
  }
  if (value > 5) {
    e.style.color = "#ADD34F";
  }
  if (value >= 7.5) {
    e.style.color = "#70D32E";
  }
  if (value == 10) {
    e.style.color = "green";
  }

}

document.querySelectorAll(".range_input_block").forEach((ib) => {
  let i = ib.querySelector(".range_input");
  let p = ib.querySelector(".range_paragraph");
  i.oninput = function (event) {

    p.innerHTML = event.target.value;
    colorNumber(p);
  }
})

document.querySelectorAll(".estimation-value").forEach((e) => {
  colorNumber(e);
})

let modal = document.getElementById("myModal");
let modalImg = document.getElementById("img01");
let captionText = document.getElementById("caption");
let span = document.querySelector("#close_img");
let hoverImgs = document.querySelectorAll('.hover-img')

for (let h of hoverImgs) {
  h.onclick = function () {
    modal.style.display = "block";
    modalImg.src = h.src;
    captionText.innerHTML = h.alt;

    span.onclick = function () {
      modal.style.display = "none";
    };
    modal.onclick = function () {
      modal.style.display = "none";
    }
  }
}
let sb = document.getElementById("showbutton");
let domain = 'http://localhost:8000/';
let rubrics = [];
try {
  sb.onclick = function () {
    let modal = document.getElementById("RubricModal");
    let span = document.getElementById("close_rubrics");
    let content = modal.querySelector('.modal-content');
    // тут пишем аякс запрос
    if(rubrics.length == 0){
      let rubricListLoader = new XMLHttpRequest();
      rubricListLoader.onreadystatechange = function () {
          if (rubricListLoader.readyState == 4) {
              if (rubricListLoader.status == 200) {
                  rubrics = JSON.parse(rubricListLoader.responseText);
                  for(let r of rubrics){
                    content.innerHTML += '<a href="/posts/'+r.name + '/"><div class="modal-block">'+r.name+'</div></a>';

                  }
              }
          }
      }
    
      function rubricListLoad() {
          rubricListLoader.open('GET', domain + 'posts/api/rubrics/', true);
          rubricListLoader.send();
      }
      rubricListLoad();

    }
    // setTimeout(() => {
    //   for(let r of rubrics){
    //     alert(r["id"]);
    //     alert(r["name"]);
    //     alert(r["post_count"]);
    //   }
    // },2000)

    modal.style.display = "block";

    span.onclick = function () {
      modal.style.display = "none";
    };
    modal.onclick = function () {
      modal.style.display = "none";
    }
  };
} catch{
  console.log('На этой странице нет showbutton.')
}
