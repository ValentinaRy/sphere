var ajaxshellist = $("#main").data("ajax-shel-list");

function changeTable(resp) {
    var table = $('#shel_list tbody');
    var content = "<tbody>";
    resp.data.forEach(function(elem, num) {
        link = "../" + elem.id;
        name = "<a href='" + link + "'>" + elem.name + "</a>";
        content += "<tr><td>"+name+"</td><td>"+elem.aver.toFixed(2)+"</td><td>"+elem.cnt+"</td></tr>";
    });
    content += "</tbody>";
    table.replaceWith(content);
}

function getShelPage(delt) {
    var page = $("#page").text();
    page = page*1 + delt;
    if (page < 1) {
        return;
    }
    $.ajax({
        method: "GET",
        url: ajaxshellist,
        data: {'page': page}
    })
        .done(function(resp) {
            console.log(resp);
            if (resp.data.length > 0) {
                $("#page").text(page);
                changeTable(resp);
            }
        });
}

$(document).ready(function() {
    $(".next").click(function () {
        getShelPage(1);
    });
    $(".prev").click(function() {
        getShelPage(-1);
    });
    getShelPage(0);
});