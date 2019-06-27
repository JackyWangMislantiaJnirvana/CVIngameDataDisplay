function toggleRemove() {
    let removeBtn = $('.remove-btn');
    if (removeBtn.is(":visible"))
        removeBtn.hide();
    else removeBtn.show();
}

function requestDatasets() {
    let i, c = $('.dataset-card'), m = $('.dataset-modal');
    let baseURL = "/users/" + $('#page-username').attr('value') + "/dashboard/";

    for(i = 0; i < c.length; i++) {
        (function(idx, elem) {$.get({
            'dataType': 'html',
            'url': baseURL + 'do_render.cgi',
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
            'url': baseURL + 'do_render.cgi',
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
    let i, c = $('.last-update-time');
    let baseURL = "/users/" + $('#page-username').attr('value') + "/dashboard/";

    for(i = 0; i < c.length; i++) {
        let idx = c[i].id.split('-')[0];
        (function(idx, elem) {
            $.get({
                'url': baseURL + 'query_last_update.cgi',
                'data': {
                    'dataset': idx
                },
                'success': function (xhr) {
                    console.log(xhr);
                    elem.setAttribute('datetime', (new Date(parseInt(xhr) * 1000)).toISOString())
                    timeago().render(elem)
                }
            })
        })(idx, c[i]);
    }
}

function requestAll() {
    requestDatasets();
    requestLastUpdate();
}

$(requestAll);
setInterval(requestAll, 10 * 60 * 1000);
setInterval(function() {timeago().render($('.last-update-time'))}, 10 * 1000)