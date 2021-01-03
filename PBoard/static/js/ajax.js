function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function sendRequest(method, url, data = null) {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();

        xhr.open(method, url);

        xhr.responseType = 'json';
        xhr.setRequestHeader('Content-Type', 'application/json')
        xhr.setRequestHeader("X-CSRFTOKEN", getCookie("csrftoken"));

        xhr.onload = () => {
            if (xhr.status >= 400) {
                reject(xhr.response);
            } else {
                resolve(xhr.response);
            }
        }

        xhr.onerror = () => {
            reject(xhr.response)
        }

        xhr.send(JSON.stringify(data));
    })
}

document.body.querySelectorAll('.post-main').forEach((post) => {

    let estimation_value_block = post.querySelector('.estimation-value')
    let range_input = post.querySelector('.range_input')
    let range_paragraph = post.querySelector('.range_paragraph')
    let range_delete_btn = post.querySelector('.range_delete_btn')

    let data = {
        post_id: range_input.getAttribute('post_id'),
    }

    sendRequest('GET', '/posts/estimations/?post_id='+data.post_id, data)
    .then(data => {
        if(data['status']){
            range_paragraph.innerHTML = data['user_est'];
            range_input.value = data['user_est'];
            colorNumber(range_paragraph)
        }
    })

    range_input.onchange = function (event) {
        event.preventDefault();

        data['estimation_value'] = event.target.value;

        sendRequest('POST', '/posts/estimations/', data)
            .then(data => {
                console.log(data)
                // Тут дописать заполнения поля
                estimation_value_block.innerHTML = data['post_est']
                colorNumber(estimation_value_block)
            })
            .catch(err => console.log(err))
    }

    range_delete_btn.onclick = function(event){
        event.preventDefault();

        sendRequest('DELETE','/posts/estimations/',data)
            .then(data => {
                console.log(data) 
                if(data['post_est'] == null){
                    estimation_value_block.innerHTML = 'пока нет оценки'
                    estimation_value_block.style.color = 'red'
                } else {
                    estimation_value_block.innerHTML = data['post_est']
                    colorNumber(estimation_value_block)
                }
                range_paragraph.innerHTML = 5;
                range_input.value = 5;
            })
            .catch(err => console.log(err))
    }
})

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