
// Add audio items.

fetch('http://localhost:5000/api/feed/0/0').then(
    resp => resp.json()
).then(function (data) {
    var listElm = document.querySelector('#infinite-list');

    var nextItem = data.id
    var loadMore = function () {
        if (nextItem < 1) {
            return null;
        }
        fetch(`http://localhost:5000/api/feed/${nextItem.toString()}/10`
        ).then(
            resp => resp.json()
        ).then(function (posts) {
            console.log(posts)
            for (var i in posts.posts) {
                var post = posts.posts[i];
                console.log(post)
                var html = `<div class=\"row\">\n` +
                    `        <div class=\"col-md-12 col-xl-8 offset-xl-2\" style=\"text-align: center;\">\n` +
                    `            <h6 style=\"margin: 10px;color: rgb(255,255,255);\">${post.title}</h6>\n` +
                    `            <audio controls=\"\" style=\"margin: 10px;width: 80%;\">\n` +
                    `                <source src=\"static/audio/mp3/${post.audio_file}.mp3\"\n` +
                    `                        type=\"audio/mpeg\">\n` +
                    `            </audio>\n` +
                    `        </div>\n` +
                    `    </div>`
                listElm.insertAdjacentHTML("beforeend", html)
            }
        }).catch(error => console.log(error));
    }


    // Detect when scrolled to bottom.
    listElm.addEventListener('scroll', function () {
        if (listElm.scrollTop + listElm.clientHeight >= listElm.scrollHeight) {
            loadMore();
        }
    });
    // Initially load some items.
    loadMore();
}).catch(error => console.log(error));