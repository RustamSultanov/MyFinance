$(document).ready(function () {

    $(document).on("click", '#updateAddress', function () {
        showAddressToChange();
    });

    $(document).on("click", '#updateFN', function () {
        showFirstNameToChange();
    });

    $(document).on("click", '#updateLN', function () {
        showLastNameToChange();
    });

    $(document).on("click", "#cancelAddress", function () {
            showAddress();
    });

    $(document).on("click", "#cancelFN", function () {
            showFirstName();
    });

    $(document).on("click", "#cancelLN", function () {
            showLastName();
    });

    $(document).on("click", '#sendAddressAjax', function () {
        var csrftoken = getCookie('csrftoken');
        var text = $("#contentAddress").val();
        $.ajaxSetup({
            url: "/update/",
            type: "POST",
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            data: {'address': text},
            success: [
                function () {
                    showAddress(text);
                }
            ],
            error: [
                function () {
                    alert("Your session is over.");
                }
            ]
        });
    });

    $(document).on("click", '#sendFirstNameAjax', function () {
        var csrftoken = getCookie('csrftoken');
        var text = $("#contentFN").val();
        $.ajaxSetup({
            url: "/update/",
            type: "POST",
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            data: {'first_name': text},
            success: [
                function () {
                    showFirstName(text);
                }
            ],
            error: [
                function () {
                    alert("Your session is over.");
                }
            ]
        });
    });

    $(document).on("click", '#sendLastNameAjax', function () {
        var csrftoken = getCookie('csrftoken');
        var text = $("#contentLN").val();
        $.ajaxSetup({
            url: "/update/",
            type: "POST",
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        $.ajax({
            data: {'last_name': text},
            success: [
                function () {
                    showLastName(text);
                }
            ],
            error: [
                function () {
                    alert("Your session is over.");
                }
            ]
        });
    });

});

function showAddressToChange() {
    var text = $('#ar').html();
    document.cookie = "address=" + text;
    $("#address")
        .empty()
        .append("" +
            "<div class='form-group'>" +
            "   <input type='text' class='form-control' id='contentAddress' value='" + text + "'/>" +
            "   <a id='sendAddressAjax'>" +
            "       <button class='btn btn-success'>Update</button>" +
            "   </a>" +
            "   <a id='cancelAddress'>" +
            "       <button class='btn btn-warning'>Cancel</button>" +
            "   </a>" +
            "</div>"
        );
    $('#contentAddress').focus();
}

function showAddress(text) {
    var toInsert = null;
    if (text == null) toInsert = getCookie('address');
    else toInsert = text;
    document.cookie = "address=" +toInsert;
    $("#address")
        .empty()
        .append("" +
            "<h4>Your address: <b id='ar'>" + toInsert + "</b> " +
            "   <a id='updateAddress'>" +
            "       <button class='btn btn-success'>" +
            "           <span class='glyphicon glyphicon-pencil' aria-hidden='true'></span>" +
            "       </button>" +
            "   </a>" +
            "</h4>"
        );
}

function showFirstNameToChange() {
    var text = $('#fn').html();
    document.cookie = "firstName=" + text;
    $("#first_name")
        .empty()
        .append("" +
            "<div class='form-group'>" +
            "   <input type='text' class='form-control' id='contentFN' value='" + text + "'/>" +
            "   <a id='sendFirstNameAjax'>" +
            "       <button class='btn btn-success'>Update</button>" +
            "   </a>" +
            "   <a id='cancelFN'>" +
            "       <button class='btn btn-warning'>Cancel</button>" +
            "   </a>" +
            "</div>"
        );
    $('#contentFN').focus();
}

function showFirstName(text) {
    var toInsert = null;
    if (text == null) toInsert = getCookie('firstName');
    else toInsert = text;
    document.cookie = "firstName=" + toInsert;
    $("#first_name")
        .empty()
        .append('' +
            '<h4>Your first name: <b id="fn">' + toInsert + '</b> ' +
            '   <a id="updateFN">' +
            '       <button class="btn btn-success">' +
            '           <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>' +
            '       </button>' +
            '   </a>' +
            '</h4>'
        );
}

function showLastNameToChange() {
    var text = $('#ln').html();
    document.cookie = "lastName=" + text;
    $("#last_name")
        .empty()
        .append("" +
            "<div class='form-group'>" +
            "   <input type='text' class='form-control' id='contentLN' value='" + text + "'/>" +
            "   <a id='sendLastNameAjax'>" +
            "       <button class='btn btn-success'>Update</button>" +
            "   </a>" +
            "   <a id='cancelLN'>" +
            "       <button class='btn btn-warning'>Cancel</button>" +
            "   </a>" +
            "</div>"
        );
    $('#contentLN').focus();
}

function showLastName(text) {
    var toInsert = null;
    if (text == null) toInsert = getCookie('lastName');
    else toInsert = text;
    document.cookie = "lastName=" + toInsert;
    $("#last_name")
        .empty()
        .append("" +
            "<h4>Your last name: <b id='ln'>" + toInsert + "</b> " +
            "   <a id='updateLN'>" +
            "       <button class='btn btn-success'>" +
            "           <span class='glyphicon glyphicon-pencil' aria-hidden='true'></span>" +
            "       </button>" +
            "   </a>" +
            "</h4>"
        );
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
