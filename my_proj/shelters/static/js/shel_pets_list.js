function changeTable(resp) {
    table = document.getElementById('main-div');
    console.log(resp);
    table.innerHTML = "";
    for (i=0; i<resp.names.length; i++) {
        table.innerHTML += '<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">'
        + '<div class="pet_elem ">' + "<a href='../" + resp.ids[i] + "'>"
        + '<img height=200 width=200 src="'+resp.photos[i]+'" class="img-rounded"/>'
        + '<p>'+resp.names[i]+'</p>' + '</a></div></div>';
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
        ptype = document.getElementById('id_ptype').value;
        sex = document.getElementById('id_sex').value;
        avail = document.getElementById('id_avail').value;
        params = "?page="+page.innerHTML+"&ptype="+ptype+"&sex="+sex+"&avail="+avail;
        getPage(link, params);
    };
}

prev = document.getElementsByClassName('prev')

for (var i=0; i<prev.length; i++) {
    prev[i].onclick = function () {
        page = document.getElementById('page');
        if (page.innerHTML == '1') return;
        var link = document.getElementById('ajax_link').value;
        page.innerHTML--;
        ptype = document.getElementById('id_ptype').value;
        sex = document.getElementById('id_sex').value;
        avail = document.getElementById('id_avail').value;
        params = "?page="+page.innerHTML+"&ptype="+ptype+"&sex="+sex+"&avail="+avail;
        getPage(link, params);
    };
}
