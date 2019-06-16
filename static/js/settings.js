// basic notification

function notifySuccess(text, delay=750) {
    $.notify({ 
        message: text,
        icon: 'fa fa-ok'
    }, { 
        type: 'success', 
        delay: delay
    });
}

function notifyError(text, delay=750) {
    $.notify({
        message: text,
        icon: 'fa fa-exclamation-circle'
    }, {
        type: 'danger',
        delay: delay
    });
}

function notifyISE() {
    notifyError('<b>Internal Error</b> Please contact the administrator.');
}

function notifyPermissionDenied() {
    notifyError('<b>Permission Denied</b> You don\'t have the permission for this action.')
}

function notifyUserNotFound() {
    notifyError('<b>User not found</b> Please check the username again.')
}

function notifyCodeNotFound() {
    notifyError('<b>Invite code not found</b> Please check the invite code again.')
}

function switchSettings(name) {
    $('.sidebar-page').each(function (idx, name) {
        $(name).hide()
    });
    $('.list-group-item').each(function (idx, name) {
        $(name).removeClass('active');
    });
    $('#page-'+name).show(); $('#sidebar-'+name).addClass('active');
    
}

// general

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
            if(xhr.status < 500) {
                if(xhr.responseText == 'WRONG_OLD_PASSWORD') notifyError('Wrong old password.');
                else if(xhr.responseText == 'PASSWORD_NO_MATCH') notifyError('Passwords don\'t match');
                else notifyISE();
            } else notifyISE();
        },
        success: function () {
            notifySuccess('Password updated.');
        }
    });
})

// stat

// accounts

function recheckIsAdminState(name) {
    var flag = $('#'+name+'-is-admin').prop('checked')
    $.ajax({
        url: '/site_management/set_admin',
        method: 'POST',
        data: {
            username: name
        },
        error: function(xhr) {
            if(xhr.status < 500) {
                if(xhr.responseText == 'PERMISSION_DENIED') notifyPermissionDenied();
                else if(xhr.responseText == 'USER_NOT_FOUND') notifyUserNotFound();
                else notifyISE();
            } else notifyISE();
        },
        success: function(xhr) { notifySuccess('Successfully changed the role of ' + name + '.') }
    })
}

function resetPassword(name) {
    bootbox.confirm({
        title: "Reset Password",
        message: "Are you sure to reset the password of \"" + name + "\"?",
        callback: function (result) {
            if (!result) return;
            $.ajax({
                url: '/site_management/reset_password',
                method: 'POST',
                dataType: 'json',
                data: {
                    username: name
                },
                error: function (result) {
                    if (result.text != null) {
                        if (result.text == 'PERMISSION_DENIED') notifyPermissionDenied();
                        else if (result.text == 'USER_NOT_FOUND') notifyUserNotFound();
                        else notifyISE();
                    } else notifyISE();
                },
                success: function (result) {
                    var msg = ''
                    msg += '<div class=\"input-group\">'
                    msg += '<input class=\"form-control\" id=\"userNewPass\" readonly autofocus value=\"' + result.password + '\">';
                    msg += '<button class=\"btn input-group-append btn-light\" data-clipboard-text=\"' + result.password + '\"><span class=\"fa fa-clipboard\"></span></button>'
                    msg += '</div>'
                    var alt = bootbox.alert({
                        title: "New password for \"" + name + "\"",
                        message: msg
                    });
                    alt.on('shown.bs.modal', function() {
                        new ClipboardJS('.btn', {
                            container: $('.bootbox.modal').get(0)
                        });
                    })
                }
            })
        }
    })
}

function removeUser(name) {
    bootbox.confirm({ 
        size: "small",
        title: "Remove a user",
        message: "Are you sure to remove \"" + name + "\" from the users?",
        callback: function(result) {
            if(!result) return;
            $('#' + name).hide()
            $.ajax({
                url: '/site_management/remove_user',
                method: 'POST',
                data: {
                    username: name
                },
                error: function (xhr) {
                    if (xhr.status < 500) {
                        if (xhr.responseText == 'PERMISSION_DENIED') notifyPermissionDenied();
                        else if (xhr.responseText == 'USER_NOT_FOUND') notifyUserNotFound();
                        else notifyISE();
                    } else notifyISE();
                },
                success: function (xhr) {
                    notifySuccess('Successfully removed user \"' + name + '\".')
                }
            })
        }})
}

function removeInvCode(code) {
    bootbox.confirm({
        title: "Remove an invite code",
        message: "Are you sure to remove the invite code \"" + code + "\"?",
        callback: function (result) {
            if (!result) return;
            $('#' + code).hide()
            $.ajax({
                url: '/site_management/remove_invite_code',
                method: 'POST',
                data: {
                    code: code
                },
                error: function (xhr) {
                    if (xhr.status < 500) {
                        if (xhr.responseText == 'PERMISSION_DENIED') notifyPermissionDenied();
                        else if (xhr.responseText == 'CODE_NOT_FOUND') notifyCodeNotFound();
                        else notifyISE();
                    } else notifyISE();
                },
                success: function () {
                    notifySuccess('Successfully removed invite code \"' + code + '\".')
                }
            })
        }
    })
}

function appendInviteCode() {
    $.ajax({
        url: '/site_management/append_invite_code',
        method: 'POST',
        dataType: 'json',
        data: {},
        error: function (result) {
            if (result.text != null) {
                if (result.text == 'PERMISSION_DENIED') notifyPermissionDenied();
                else notifyISE();
            } else notifyISE();
        },
        success: function (result) { 
            const TEMPLATE = [
                '<tr id=\'' + result.invcode.code + '\'>',
                                '<td>' + result.invcode.id + '</td>',
                                '<td>' + result.invcode.code + '</td>',
                                '<td>',
                                    '<button type="button" class="close removeBtn"',
                                    'onclick="removeInvCode(\'' + result.invcode.code + '\');">×</button>',
                                '</td>',
                            '</tr>'
            ];
            var h = '';
            for(i in TEMPLATE) h += TEMPLATE[i];
            $('#invcode-list').append(h);
        }
    })
}