function toggleRemove() {
    var removeBtn = $('.remove-btn');
    if (removeBtn.is(":visible"))
        removeBtn.hide();
    else removeBtn.show();
}

function requestDatasets() {
    let i, c = $('.dataset-card'), m = $('.dataset-modal');

    for(i = 0; i < c.length; i++) {
        (function(idx, elem) {$.get({
            'dataType': 'html',
            'url': document.location + 'do_render.cgi',
            'data': {
                'dataset': idx,
                'is_modal': false
            },
            'success': function (xhr) {
                elem.innerHTML = xhr;
            },
            'error': function (xhr) {
                let txt = '';
                if(!(xhr.responseText instanceof String))
                    txt = 'No Info';
                else txt = xhr.responseText;
                elem.innerHTML =
                    "<div class=\"alert alert-danger\" role=\"alert\">\n" +
                    (xhr.status > 0 ? ("ERROR: Got code " + xhr.status.toString() + ": " + txt.slice(0, 50) + "\n")
                        : "Disconnected from server\n") +
                    "</div>"
            }
        })})(c[i].id.split('-')[0], c[i])
    }

    for(i = 0; i < m.length; i++) {
        (function(idx, elem) {$.get({
            'dataType': 'html',
            'url': document.location + 'do_render.cgi',
            'data': {
                'dataset': idx,
                'is_modal': true
            },
            'success': function (xhr) {
                elem.innerHTML = xhr;
            },
            'error': function (xhr) {
                let txt = '';
                if(!(xhr.responseText instanceof String))
                    txt = 'No Info';
                else txt = xhr.responseText;
                elem.innerHTML =
                    "<div class=\"alert alert-danger\" role=\"alert\">\n" +
                    (xhr.status > 0 ? ("ERROR: Got code " + xhr.status.toString() + ": " + txt.slice(0, 50) + "\n")
                        : "Disconnected from server\n") +
                    "</div>"
            }
        })})(m[i].id.split('-')[0], m[i])
    }
}

function requestLastUpdate() {
    let c = $('.last-update-time'), m = $('.last-update-time-modal');

}

function requestAll() {
    requestDatasets();
}

$(requestAll);
setInterval(requestAll, 10 * 60 * 1000);