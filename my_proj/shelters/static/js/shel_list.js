function changeTable(resp) {
    table = document.getElementById('shel_list');
    console.log(resp);
    table.innerHTML = "";
    resp.data.forEach(function(elem, num) {
        link = "../" + elem.id;
        name = "<a href='" + link + "'>" + elem.name + "</a>";
        table.innerHTML += "<tr><td>"+name+"</td><td>"+elem.aver.toFixed(2)+"</td><td>"+elem.cnt+"</td></tr>";
    });
}

function getPage(link, param) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var resp = JSON.parse(this.responseText);
            changeTable(resp);
        }
    };
    req.open("GET", link+param, false);
    req.send();
}

next = document.getElementsByClassName('next')

for (var i=0; i<next.length; i++) {
    next[i].onclick = function () {
        page = document.getElementById('page');
        page.innerHTML++;
        param = "?page="+page.innerHTML;
        getPage(ajax_link, param);
    };
}

prev = document.getElementsByClassName('prev')

for (var i=0; i<prev.length; i++) {
    prev[i].onclick = function () {
        page = document.getElementById('page');
        if (page.innerHTML == '1') return;
        page.innerHTML--;
        param = "?page="+page.innerHTML;
        getPage(ajax_link, param);
    };
}
