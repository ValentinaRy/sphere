var shelid = $("#main").data("shel-id");
var sheladmin = $("#main").data("shel-admin");
var petid = $("#main").data("pet-id");
var shelpets = $("#main").data("shel-pets-url");

$(document).ready(function() {
    $('#shel-form').on('submit', function(event) {
        event.preventDefault();
    });
    $('#add-pet-form').on('submit', function(event) {
        event.preventDefault();
    });
    $('#pet-info-form').on('submit', function(event) {
        event.preventDefault();
    });
    $('#pet-owner').on('submit', function(event) {
        event.preventDefault();
    });
    $('#shelbtn').click(function () {
        var fd = new FormData($("#shel-form")[0]);
        fd.append("shel_id", shelid);
        fd.append("ch_shel", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#shel-status").show();
                    $("#shel-status").text("Сохранено успешно");
                    $("#shel-status").removeClass("btn-danger");
                    $("#shel-status").addClass("btn-success");
                    setTimeout(function() {
                        $("#shel-status").hide();
                    }, 3000);
                } else {
                    $("#shel-status").show();
                    $("#shel-status").text(resp.message);
                    $("#shel-status").removeClass("btn-success");
                    $("#shel-status").addClass("btn-danger");
                    setTimeout(function() {
                        $("#shel-status").hide();
                    }, 3000);
                    console.log(resp.errors);
                }
            });
    });
    $('#addpet').click(function () {
        var name = $('#id_pet_name').val();
        var ptype = $('#id_pet_ptype').val();
        var sex = $('#id_pet_sex').val();
        var photo = $('#id_pet_photo').val();
        var in_date = $('#id_pet_in_date').val();
        var fd = new FormData($("#add-pet-form")[0]);
        fd.append("shel_id", shelid);
        fd.append("add_pet", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#pet-status").show();
                    $("#pet-status").text("Сохранено успешно");
                    $("#pet-status").removeClass("btn-danger");
                    $("#pet-status").addClass("btn-success");
                    getPetPage(0);
                    setTimeout(function() {
                        $("#pet-status").hide();
                    }, 3000);
                } else {
                    $("#pet-status").show();
                    $("#pet-status").text(resp.message);
                    $("#pet-status").removeClass("btn-success");
                    $("#pet-status").addClass("btn-danger");
                    setTimeout(function() {
                        $("#pet-status").hide();
                    }, 3000);
                    console.log(resp.errors);
                }
            });
    });
    $('#pet-info-btn').click(function () {
        var fd = new FormData($("#pet-info-form")[0]);
        fd.append("shel_id", shelid);
        fd.append("pet_id", petid);
        fd.append("ch_pet", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#pet-info-lbl").show();
                    $("#pet-info-lbl").text("Сохранено успешно");
                    $("#pet-info-lbl").removeClass("btn-danger");
                    $("#pet-info-lbl").addClass("btn-success");
                    $("img").attr("src",resp.photo_url);
                    setTimeout(function() {
                        $("#pet-info-lbl").hide();
                    }, 3000);
                } else {
                    $("#pet-info-lbl").show();
                    $("#pet-info-lbl").text(resp.message);
                    $("#pet-info-lbl").removeClass("btn-success");
                    $("#pet-info-lbl").addClass("btn-danger");
                    setTimeout(function() {
                        $("#pet-info-lbl").hide();
                    }, 3000);
                    console.log(resp.errors);
                }
            });
    });
    $("#del-pet").click(function () {
        var fd = new FormData($("#pet-info-form")[0]);
        fd.append("shel_id", shelid);
        fd.append("pet_id", petid);
        fd.append("del_pet", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#pet-info-lbl").show();
                    $("#pet-info-lbl").text("Удален успешно");
                    $("#pet-info-lbl").removeClass("btn-danger");
                    $("#pet-info-lbl").addClass("btn-success");
                    setTimeout(function() {
                        $("#pet-info-lbl").hide();
                        window.location.replace(shelpets);
                    }, 3000);
                } else {
                    $("#pet-info-lbl").show();
                    $("#pet-info-lbl").text(resp.message);
                    $("#pet-info-lbl").removeClass("btn-success");
                    $("#pet-info-lbl").addClass("btn-danger");
                    setTimeout(function() {
                        $("#pet-info-lbl").hide();
                    }, 3000);
                    console.log(resp.errors);
                }
            });
    });
    $("#owner-id").bind('keyup mouseup',function () {
        var fd = new FormData($("#pet-owner")[0]);
        fd.append("shel_id", shelid);
        fd.append("pet_id", petid);
        fd.append("get_username", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#owner-name").text(resp.username);
                    $("#set-owner").prop("disabled", false);
                    $("#set-owner").removeClass("disabled");
                } else {
                    $("#owner-name").text("No such user");
                    $("#set-owner").prop("disabled", true);
                    $("#set-owner").addClass("disabled");
                }
            });
    });
    $("#set-owner").prop("disabled", true);
    $("#set-owner").click(function () {
        var fd = new FormData($("#pet-owner")[0]);
        fd.append("shel_id", shelid);
        fd.append("pet_id", petid);
        fd.append("set_owner", 1);
        $.ajax({
            method: "POST",
            url: sheladmin,
            data: fd,
            processData: false,
            contentType: false
            })
            .done(function(resp) {
                console.log(resp);
                if (resp.status == 1) {
                    $("#pet-owner").remove();
                    $("#pet-info").append("<div>Уже взяли домой</div>" +
                        "<div>Хозяин: "+resp.username+"</div>");
                } else {
                    $("#owner-name").text("No such user");
                    $("#set-owner").prop("disabled", true);
                    $("#set-owner").addClass("disabled");
                }
            });
    });
});