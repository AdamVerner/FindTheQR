let layer;
let m;

document.addEventListener("DOMContentLoaded", function(){

    Loader.async = true;
    Loader.load(null, null, function () {

        m = new SMap(JAK.gel("map"), SMap.Coords.fromWGS84(14.430, 50.084), 13);
        // Grow map to the size of it's parent element
        m.addControl(new SMap.Control.Sync());

        m.addDefaultLayer(SMap.DEF_SMART_BASE).enable();
        m.addDefaultControls();

        var mouse = new SMap.Control.Mouse(SMap.MOUSE_PAN | SMap.MOUSE_WHEEL | SMap.MOUSE_ZOOM); /* Ovládání myší */
        m.addControl(mouse);

        // create marker layer we will later fill
        layer = new SMap.Layer.Marker();
        m.addLayer(layer);
        layer.enable();

        console.log('pasting coords into map');
        //{% for p in waypoints %}
        addPoint("{{ p.coord_x }}", "{{ p.coord_y }}", "{{ p.name }}", "{{p.description}}");
        //{% endfor %}

    });
    console.log('calling Loader finished');

});


function addPoint(x, y, name, description){

         /* Create card with location miniature */
        var card = new SMap.Card();
        card.getHeader().innerText = name;
        card.getBody().innerText = description;


        /* create marker with embedded card */
        var options = { title: name };
        var marker = new SMap.Marker(SMap.Coords.fromWGS84(x, y), "Marker" + x + y, { title: name });
        marker.decorate(SMap.Marker.Feature.Card, card);

        /* add marker to map */
        layer.addMarker(marker);
        console.log("Added " + name);

        return card

}