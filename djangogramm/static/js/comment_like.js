document.addEventListener("DOMContentLoaded", function(){
    let likeButtons = document.querySelectorAll('[id^="like-button-"]');
    likeButtons.forEach(function(button) {
        handleButtonClick(button);
    });

    function handleButtonClick(button){
        button.addEventListener('click', function (event){
            const url = this.getAttribute('data-url');
            let commentId = this.value;
            const csrftoken = getCookie('csrftoken');
            const xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE){
                    if (xhr.status === 200){
                        const response = JSON.parse(xhr.responseText);
                        const likeCountSpan = document.getElementById('like-count-'+commentId);
                        let likes = parseInt(likeCountSpan.textContent);
                        if (response.created) {
                            likeCountSpan.textContent = likes + 1;
                            button.textContent = 'Unlike';
                            button.classList.add('btn-secondary');
                            button.classList.remove('btn-primary');
                        } else {
                            likeCountSpan.textContent = likes - 1;
                            button.textContent = 'Like';
                            button.classList.remove('btn-secondary');
                            button.classList.add('btn-primary');
                        }
                    } else {
                        console.error('Error while liking a comment!', xhr.status);
                    }
                }
            };

            xhr.send(JSON.stringify({commentId: commentId}));
            event.preventDefault();
        });
    }

    function getCookie(name) {
        const cookieRegex = new RegExp(`(?:(?:^|.*;\\s*)${name}\\s*\\=\\s*([^;]*).*$)|^.*$`);
        const cookieMatch = document.cookie.match(cookieRegex);
        return cookieMatch? cookieMatch.pop(): '';
    }
});
