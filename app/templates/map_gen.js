let layer;

document.addEventListener("DOMContentLoaded", function(){

    Loader.async = true;
    console.log('calling Loader');
    Loader.load(null, null, function () {
        console.log('Loading stuff');

        const center = SMap.Coords.fromWGS84(14.41790, 50.12655);
        const map = JAK.gel("map");
        const m = new SMap(JAK.gel("map"), center, 9);
        m.addDefaultLayer(SMap.DEF_SMART_BASE).enable();
        m.addDefaultControls();

        // Grow map to the size of it's parent element
        const sync = new SMap.Control.Sync();
        m.addControl(sync);

        // create marker layer we will later fill
        layer = new SMap.Layer.Marker();
        m.addLayer(layer);
        layer.enable();

        console.log('pasting coords into map');
        //{% for p in waypoints %}
        let card = addPoint("{{ p.coord_x }}", "{{ p.coord_y }}", "{{ p.name }}", "{{p.description}}");
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