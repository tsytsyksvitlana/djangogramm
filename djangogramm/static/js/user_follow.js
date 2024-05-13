document.addEventListener("DOMContentLoaded", function(){
    const followButton = document.getElementById('follow-button');
    if (followButton){
        handleButtonClick(followButton);
    }

    function handleButtonClick(button){
        button.addEventListener('click', function (event){
            const url = this.getAttribute('data-url');
            let userId = this.value;
            const csrftoken = getCookie('csrftoken');
            const xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);

            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE){
                    if (xhr.status === 200){
                        const response = JSON.parse(xhr.responseText);
                        const FollowerCountSpan = document.getElementById('follower-count');
                        let followers = parseInt(FollowerCountSpan.textContent);
                        if (response.created){
                            FollowerCountSpan.textContent = followers + 1;
                            followButton.textContent = 'Unfollow';
                            followButton.classList.add('btn-secondary');
                            followButton.classList.remove('btn-primary');
                        } else{
                            FollowerCountSpan.textContent = followers -1;
                            followButton.textContent = 'Follow';
                            followButton.classList.remove('btn-secondary');
                            followButton.classList.add('btn-primary');
                        }
                    } else {
                        console.error('Error while following a user!', xhr.status);
                    }
                }
            };

            xhr.send(JSON.stringify({userId: userId}));
            event.preventDefault();
        });
    }

    function getCookie(name) {
        const cookieRegex = new RegExp(`(?:(?:^|.*;\\s*)${name}\\s*\\=\\s*([^;]*).*$)|^.*$`);
        const cookieMatch = document.cookie.match(cookieRegex);
        return cookieMatch? cookieMatch.pop(): '';
    }
    
});
