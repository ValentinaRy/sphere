function changeTable(resp) {
    table = document.getElementById('shel_list');
    console.log(resp);
    table.innerHTML = "";
    for (i=0; i<resp.names.length; i++) {
        link = "'../" + resp.ids[i] + "'"
        name = "<a href=" + link + ">" + resp.names[i] + "</a>";
        table.innerHTML += "<tr><td>"+name+"</td><td>"+resp.rates[i].toFixed(2)+"</td><td>"+resp.cnts[i]+"</td></tr>";
    }
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
        var link = document.getElementById('ajax_link').value;
        page.innerHTML++;
        param = "?page="+page.innerHTML;
        getPage(link, param);
    };
}

prev = document.getElementsByClassName('prev')

for (var i=0; i<prev.length; i++) {
    prev[i].onclick = function () {
        page = document.getElementById('page');
        if (page.innerHTML == '1') return;
        var link = document.getElementById('ajax_link').value;
        page.innerHTML--;
        param = "?page="+page.innerHTML;
        getPage(link, param);
    };
}
