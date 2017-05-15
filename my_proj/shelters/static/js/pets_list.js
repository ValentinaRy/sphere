var ajaxpetlist = $("#main").data("ajax-pet-list");
var petlist = $("#main").data("pet-list");
var mediaurl = $("#main").data("media-url");
var shelid = $("#main").data("shel-id");

function changeList(resp) {
    list = $('#main-div');
    content = '<div id="main-div" class="flex-container">';
    resp.data.forEach(function(elem, num) {
        content += '<div>'
        + '<div class="pet-elem bord-block">' + "<a href='" + petlist + "../" + elem.id + "'>"
        + '<img height=200 width=200 src="'+mediaurl+elem.photo+'"/>'
        + '<p>'+elem.name.substring(0,22)+'</p>' + '</a></div></div>';
    });
    content += "</div>";
    list.replaceWith(content);
}

function getPetPage(delt) {
    var page = $("#page").text();
    page = page*1 + delt;
    if (page < 1) {
        return;
    }
    ptype = $("#id_ptype").val();
    sex = $("#id_sex").val();
    avail = $("#id_avail").val();
    $.ajax({
        method: "GET",
        url: ajaxpetlist,
        data: {'page': page, 'ptype': ptype, 'sex': sex,
                'avail': avail, 'shel_id': shelid},
        })
        .done(function(resp) {
            console.log(resp);
            if (resp.data.length > 0) {
                $("#page").text(page);
                changeList(resp);
            }
        });
}

$(document).ready(function() {
    $(".next").click(function () {
        getPetPage(1);
    });
    $(".prev").click(function() {
        getPetPage(-1);
    });
    $('#filter-form').on('submit', function(event) {
        event.preventDefault();
        var page = $("#page").text()*1;
        getPetPage(1-page);
    });
    getPetPage(0);
});