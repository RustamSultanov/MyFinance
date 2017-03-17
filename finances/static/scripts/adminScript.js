$(document).ready(function () {

    $('.alert').fadeOut(4000);

    $(document).on("click", '.edit', {}, function() {
        const rawId = $(this).attr('id');
        const id = rawId.substring(4);
        editUser(id);
    });

    $(document).on("click", '.delete', {}, function() {
        const rawId = $(this).attr('id');
        const id = rawId.substring(6);
        deleteUser(id);
    });

    $(document).on("click", "#sendEdit", function() {
        $("#editForm").submit();
    });

    $(document).on("click", "#sendDelete", function () {
        $("#deleteForm").submit();
    });

});

const dictionary = {
    'username': null,
    'email': null,
    'first_name': null,
    'last_name': null,
    'phone': null,
    'address': null,
    'last_login': null
};

function deleteUser(data) {
    document.getElementById('deleteForm')
        .getElementsByTagName('input')
        .item(0).attributes
        .getNamedItem('value').nodeValue = data;
    $("#deleteUser").modal('show');
}

function editUser(data) {
    const tr = $("#" + data);
    for (let key in dictionary) dictionary[key] = tr.children().filter(function (j, elem) {
        return elem.className == key;
    })[0].innerText;
    for (let key in dictionary) {
        if (key != "phone") {
            $("#id_" + key).val(dictionary[key]);
        } else {
            const gap = dictionary["phone"].indexOf(' ');
            const firstPhone = dictionary['phone'].substring(0, gap);
            const secondPhone = dictionary['phone'].substring(gap + 1);
            $("#id_phone_0").val(firstPhone);
            $("#id_phone_1").val(secondPhone);
        }
    }
    $("#username").text(dictionary["username"]);
    $("#editUser").modal('show');
}
