function notifySuccess(text) {
    $.notify({ 
        message: text,
        icon: 'glyphicon glyphicon-ok'
    }, { 
        type: 'success', 
        delay: 750 
    });
}

function notifyError(text) {
    $.notify({
        message: text,
        icon: 'glyphicon glyphicon-warning-sign'
    }, {
        type: 'danger',
        delay: 750
    });
}

function notifyISE() {
    notifyError('<strong>Internal Error</strong> Please contact the administrator.');
}

function switchSettings(name) {
    $('.sidebar-page').each(function (idx, name) {
        $(name).hide()
    });
    $('.list-group-item').each(function (idx, name) {
        $(name).removeClass('active')
    });
    console.log('switching to ' + name);
    $('#page-'+name).show(); $('#sidebar-'+name).addClass('active');

}

$(function() {
    $('#descriptionForm').ajaxForm({
        error: function () {
            notifyISE();
        }, success: function () { 
            notifySuccess('User description updated.');
        }
    });
})

$(function () {
    $('#changePWForm').ajaxForm({
        error: function (xhr) {
            if(xhr.status != 403 || xhr.responseText == '')
                notifyISE();
            else notifyError('Passwords don\'t match.');
        },
        success: function () {
            notifySuccess('Password updated.');
        }
    });
})