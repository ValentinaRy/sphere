var shel_id = $("#main").data("shel-id");
var ajax_comment = $("#main").data("ajax-comment");

function get_comments() {
    var fd = new FormData($("#comment-form")[0]);
    fd.append("shel_id", shelid);
    $.ajax({
        method: "GET",
        url: ajax_comment,
        data: {'shel_id': shel_id}
        })
        .done(function(resp) {
            console.log(resp);
            if (resp.status == 1) {
                content = '<div id="comments-div" class="flex-container">'
                resp.comments.forEach(function(elem, num) {
                    content += '<div class="bord-block comment-elem"> \
                            <div>Оценка: '+elem.rating+'</div> \
                            <div>Комментарий: '+elem.comment+'</div> \
                            <div>Пользователь: '+resp.authors[num]+'</div> \
                        </div>';
                });
                content += '</div>';
                $("#comments-div").replaceWith(content);
                $("#aver-rate").replaceWith('<div id="aver-rate">Средний рейтинг: '+resp.aver+'</div>');
                $("#cnt-rate").replaceWith('<div id="cnt-rate">Количество оценок: '+resp.cnt+'</div>');
            } else {
                console.log(resp.message);
                console.log(resp.errors);
            }
        });
}

$(document).ready(function() {
    $('#comment-form').on('submit', function (event) {
        event.preventDefault();
    });
    $('#comment').click(function () {
        var fd = new FormData($("#comment-form")[0]);
        fd.append("shel_id", shelid);
        $.ajax({
            method: "POST",
            url: ajax_comment,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#comment-form")[0].reset();
                    get_comments();
                } else {
                    console.log(resp.message);
                    console.log(resp.errors);
                }
            });
    });
    get_comments();
});