var listElm = document.querySelector('#infinite-list');


var nextItem;
var amount = 10;
fetch('http://localhost:5000/api/feed/0/0').then(
    resp => resp.json()
).then(function (data) {
    nextItem = data.id + amount;

    // Initially load some items.
    loadMore();
}).catch(error => console.log(error));
// Add audio items.
var loadMore = function () {
        nextItem -= amount;
        console.log(nextItem);
        if (nextItem < 1) {
            return null;
        }
        fetch(`http://localhost:5000/api/feed/${nextItem.toString()}/${amount.toString()}`
        ).then(
            resp => resp.json()
        ).then(function (posts) {
            for (var i in posts.posts) {
                var post = posts.posts[i];
                // console.log(post)
                var html = `<div class=\"row\" style="border: 1px solid var(--bs-secondary); background: rgb(50, 57, 60); margin-bottom: 20px;">\n` +
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
var scrollHeight = $(document).height();
var scrollPos = $(window).height() + $(window).scrollTop();
$(window).on("scroll", function() {
  var scrollHeight = $(document).height();
  var scrollPos = $(window).height() + $(window).scrollTop();
  if ((scrollHeight - scrollPos) / scrollHeight == 0) {
    loadMore();
}});