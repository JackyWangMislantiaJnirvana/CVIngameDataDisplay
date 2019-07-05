function notifySuccess(text, delay=750) {
    $.notify({
        message: text,
        icon: 'fa fa-check'
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

function notifyISE(s) {
    notifyError('<b>Internal Error</b><br/>' + s);
}

function initCM() {
    CodeMirror.fromTextArea($('#layout-json')[0], {
        lineNumbers: true,
        mode: {
            name: 'javascript',
            json: true
        },
        indentUnit: 4,
        autofocus: true,
        matchBrackets: true,
        autoCloseBrackets: true,
        lineWrapping: true
    })
}

function initAjaxForm() {
    $('#layout-form').ajaxForm({
        dataType: 'json',
        success: function (e) {
            console.log(e);
            if(e.status === 'success')
                notifySuccess('Layout changed.');
            else if(e.status === 'json_error')
                notifyError("<b>Error at line " + e.exception.lineno
                    + " col " + e.exception.colno + "</b><br/>" + e.exception.msg, 1048576);
            else if(e.status === 'renderer_error')
                notifyError('Renderer not found');
            else if(e.status === 'py_syntax_error')
                notifyError('Syntax error found in placeholders', 1048576);
            else if(e.status === 'key_error')
                notifyError('Required variable not found.')
            else notifyISE();
        },
        error: function (e) {
            notifyISE(e);
        }
    })
}

function initVarTreeView() {
    $('#vars').jstree({})
}

function init() {
    initCM();
    initAjaxForm();
    initVarTreeView();
}

$(init);