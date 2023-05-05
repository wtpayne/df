
// ============================================================================
// SSEIMG
// ============================================================================

AFRAME.registerComponent("sseimg", {

    // -----------------------------------------------------------------
    schema: {
        topic:     {type: "string", default: "/sse_topic"},
        resource:  {type: "string", default: "/sse_resource"},
        id_canvas: {type: "string", default: "sse_canvas"}
    },

    // -----------------------------------------------------------------
    init: function () {

        var sseimg         = this;
        sseimg.data.canvas = document.getElementById(sseimg.data.id_canvas);
        sseimg.data.stale  = false;
        sseimg.data.es     = new EventSource(sseimg.data.topic);

        var list_res = this.data.resource.split(",");
        list_res.forEach(function (id_res, idx_res) {
            sseimg.data.es.addEventListener(id_res, function(event) {
                sseimg.data.stale  = true;
                sseimg.data.buffer = event.data;
            });
        });

    },

    // -----------------------------------------------------------------
    tick: function (time, timeDelta) {

        var sseimg = this;
        var color = "red";
        if (sseimg.data.stale) {
            sseimg.data.stale = false;

            var img    = new Image();
            img.src    = "data:image/jpeg;base64," + sseimg.data.buffer.slice(2, -1);
            img.onload = function(){
                var ctx = sseimg.data.canvas.getContext("2d");
                ctx.drawImage(img, 0, 0);
            };

            material = sseimg.el.getObject3D('mesh').material;
            if (material.map) { material.map.needsUpdate = true; }

        } else {
            material = sseimg.el.getObject3D('mesh').material;
            if (material.map) { material.map.needsUpdate = false; }
        }

    }

});  // registerComponent sseimg


// ============================================================================
// BACKGROUND-GRADIENT
// ============================================================================

AFRAME.registerShader('background-gradient', {

  schema: {
    colorTop:    { type: 'color', default: '#37383c', is: 'uniform' },
    colorBottom: { type: 'color', default: '#757575', is: 'uniform' }
  },

  vertexShader: [
    'varying vec3 vWorldPosition;',

    'void main() {',

    'vec4 worldPosition = modelMatrix * vec4( position, 1.0 );',
    'vWorldPosition = worldPosition.xyz;',

    'gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );',

    '}'
  ].join('\n'),

  fragmentShader: [
    'uniform vec3 colorTop;',
    'uniform vec3 colorBottom;',

    'varying vec3 vWorldPosition;',

    'void main()',

    '{',
    'vec3 pointOnSphere = normalize(vWorldPosition.xyz);',
    'float f = 1.0;',

    'f = sin(pointOnSphere.y * 2.2) + 0.4;',

    'gl_FragColor = vec4(mix(colorBottom, colorTop, f), 1.0);',

    '}'
  ].join('\n')

});  // registerShader background-gradient
