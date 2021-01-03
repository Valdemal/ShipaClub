function searchByName(){
    let input = document.querySelector('#search-input'),
        filter = input.value.toUpperCase(),
        posts = document.querySelectorAll('.post'),
        p, name
    ;

    for(p of posts){
        name = p.querySelector('.post-estimation').querySelector('h3');
        if(name.innerHTML.toUpperCase().indexOf(filter) > -1){
            p.style.display = "";
        } else {
            p.style.display = "none";
        }
    }
}
