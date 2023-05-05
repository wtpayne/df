htmx.defineExtension('bowyer', {
onEvent : function(name_evt_src, evt_src) {

    // New logic is either swapped in or sent via SSE.
    is_swap   = (name_evt_src === 'htmx:afterSwap');
    is_sse    = name_evt_src.startsWith('htmx:sse:');
    is_update = (is_swap || is_sse);
    if (!is_update) {
        return;
    }

    // Event handling logic is stored in the window.bowyer global.
    if (!('bowyer' in window)) {
        window.bowyer = {};
    }

    // Ignore events where handling logic already exists.
    if (name_evt_src in window.bowyer) {
        return;
    }

    // Update the callbacks where we have new ones provided.
    elt_target = evt_src.target;
    list_found = htmx.findAll(elt_target, '[bowyer], [data-bowyer]');
    for (var idx = 0; idx < list_found.length; idx++) {

        elt_found    = list_found[idx];
        name_evt_tgt = 'htmx:sse:' + elt_found.id;

        if (!(name_evt_tgt in window.bowyer)) {
            window.bowyer[name_evt_tgt] = {};
        }

        node_new = eval(elt_found.dataset.bowyer);
        node_old = window.bowyer[name_evt_tgt];

        if ('step' in node_old) {
            elt_target.removeEventListener(name_evt_tgt,
                                           node_old.step);
        }
        if ('step' in node_new) {
            elt_target.addEventListener(name_evt_tgt,
                                        node_new.step);
        }

        window.bowyer[name_evt_tgt] = node_new;
        window.bowyer[name_evt_tgt].reset(name_evt_tgt);

    }
}
})
