
// ============================================================================
// SSESCENE
// ============================================================================

AFRAME.registerComponent("sse", {

    // -----------------------------------------------------------------
    schema: {
        topic:     {type: "string", default: "/id_res_sse_topic"},
        resource:  {type: "string", default: "id_res_sse_event"},
        data:      {type: "string", default: "{}"},
    },

    // -----------------------------------------------------------------
    init: function () {

        var sse             = this;
        sse.data.es         = new EventSource(sse.data.topic);
        sse.data.has_update = false;
        sse.data.event_data = "";

        var list_res = this.data.resource.split(",");
        list_res.forEach(function (id_res, idx_res) {
            sse.data.es.addEventListener(id_res, function(event) {
                sse.data.has_update = true;
                sse.data.event_data = event.data;
            });
        });
    },

    // -----------------------------------------------------------------
    tick: function (time, timeDelta) {

        var sse = this;
        if (sse.data.has_update) {

            console.log('###### UPDATE SEEN IN TICK FUNCTION ######')
            const cfg = JSON.parse(sse.data.event_data)

            for (const [id_node, cfg_node] of Object.entries(cfg['node'])) {
                el_node = sse.scene.querySelector('.' + id_node);
            }


            // el_node = sse.scene.querySelector('.id_node')
            // var sceneEl = document.querySelector('a-scene');
            // var entityEl = document.createElement('a-entity');
            // // Do `.setAttribute()`s to initialize the entity.
            // sceneEl.appendChild(entityEl);

            sse.data.has_update = false;

        }

    }

});  // registerComponent sse

// ============================================================================
// NODE
// ============================================================================

// ----------------------------------------------------------------------------
AFRAME.registerComponent("node", {

    schema: {
        id_path:   {type: "string", default: "undefined"},
        id_system: {type: "string", default: "undefined"},
        id_node:   {type: "string", default: "undefined"}
    },

    // ------------------------------------------------------------------------
    init: function () {

        var   el        = this.el;
        const id_path   = this.data.id_path;
        const id_system = this.data.id_system;
        const id_node   = this.data.id_node;

        el.addEventListener('click', function (evt) {

            const id_event      = window.crypto.randomUUID().substring(1, 8);
            const str_id_event  = "id_event="  + id_event;
            const str_id_path   = "id_path="   + id_path;
            const str_id_system = "id_system=" + id_system;
            const str_id_node   = "id_node="   + id_node;
            const str_query     = str_id_event  + "&" +
                                  str_id_path   + "&" +
                                  str_id_system + "&" +
                                  str_id_node;
            const str_uri       = "/click?" + str_query
            const Http          = new XMLHttpRequest();
            Http.open("GET", str_uri);
            Http.send();
            // Http.onreadystatechange = (e) => {  /* do something */ };

        });  // click event listener

    }  // init function

});  // registerComponent node
