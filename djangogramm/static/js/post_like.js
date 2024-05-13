document.addEventListener("DOMContentLoaded", function(){
    const likeButton = document.getElementById('like-button');
    if (likeButton){
        handleButtonClick(likeButton);
    }

    function handleButtonClick(button){
        button.addEventListener('click', function (event){
            const url = this.getAttribute('data-url');
            let postId = this.value;
            const csrftoken = getCookie('csrftoken');
            const xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE){
                    if (xhr.status === 200){
                        const response = JSON.parse(xhr.responseText);
                        const likeCountSpan = document.getElementById('like-count');
                        let likes = parseInt(likeCountSpan.textContent);
                        if (response.created) {
                            likeCountSpan.textContent = likes + 1;
                            likeButton.textContent = 'Unlike';
                            likeButton.classList.add('btn-secondary');
                            likeButton.classList.remove('btn-primary');
                        } else {
                            likeCountSpan.textContent = likes - 1;
                            likeButton.textContent = 'Like';
                            likeButton.classList.remove('btn-secondary');
                            likeButton.classList.add('btn-primary');
                        }
                    } else {
                        console.error('Error while liking a post!', xhr.status);
                    }
                }
            };

            xhr.send(JSON.stringify({postId: postId}));
            event.preventDefault();
        });
    }

    function getCookie(name) {
        const cookieRegex = new RegExp(`(?:(?:^|.*;\\s*)${name}\\s*\\=\\s*([^;]*).*$)|^.*$`);
        const cookieMatch = document.cookie.match(cookieRegex);
        return cookieMatch? cookieMatch.pop(): '';
    }
    
});
