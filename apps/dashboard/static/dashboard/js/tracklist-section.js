/**
 *  Dashboard scripts
 *  Tracklist screen
 */

 // Endpoints for Ajax calls
 var endpoints =
 {
     'track' : {
         'get'    : '/api/1.0/track/',
         'create' : '/api/1.0/track/crea',
         'update' : '/api/1.0/track/edita',
         'delete' : '/api/1.0/track/borra',
     },
     'clip' : {
         'get'    : '/api/1.0/clip/',
         'create' : '/api/1.0/clip/crea',
         'update' : '/api/1.0/clip/edita',
         'delete' : '/api/1.0/clip/borra',
     }
 }

// Container node to hold forms in the view
var form_container  = document.querySelector('#form-tracklist-container');

function clean(){
    while(form_container.firstChild)
        form_container.removeChild(form_container.firstChild);
}


jQuery(document).ready( function()
{
    // Forms
    document.querySelectorAll("[data-show-template]").forEach( function(button)
    {
        // Add action to build related template
        button.addEventListener("click", function(e)
        {
            // Prevent 'bubbling'
            e.stopPropagation();

            // Get dataset attributes from the 'builder'
            var d           = button.dataset;
            var template_id = '#' + d.showTemplate;
            var model       = d.model;
            var action      = d.action;
            var track       = d.track;
            var id          = d.id;

            // Build template
            var template_markup = document.querySelector(template_id);
            var form_node       = template_markup.content.cloneNode(true);
            var form            = form_node.querySelector('form');
            if(track)
                form.querySelector('[name="track"]').value = track;
            if(id)
                form.querySelector('[name="pk"]').value = id;
            if(action)
                form.setAttribute('data-action', action);

            // Populate form with proper data
            switch(action)
            {
                case 'update':
                    jQuery.ajax({
                        type : 'GET',
                        url  : endpoints[model]['get'] + '?pk=' + id,
                        success : function(response)
                        {
                            var data = JSON.parse(response)[0];
                            Object.keys(data.fields).forEach(function(field){
                                var widget = form.querySelector('[name='+field+']');
                                console.log(field, data.fields[field]);
                                // Image and color field values cannot be set directly
                                if(field != 'image' && field != 'color'){
                                    widget.value = data.fields[field];
                                }
                                if(field=='color'){
                                  widget.style.backgroundColor = data[field];
                                }
                                form.querySelector('[name=pk]').value = data.pk;
                            });
                        },
                        error : function(req){
                            console.log('Error: ', req);
                        },
                    });
                break;
            }

            // Update submit
            form.addEventListener('submit', function(e){
                e.preventDefault();
                var endpoint = endpoints[model][action];
                // Serialize form data but delete pks to
                // avoid breaking creation forms
                var data = jQuery(form).serialize();
                if(action=='create')
                    delete data['pk']
                jQuery.ajax({
                    type : 'POST',
                    url  : endpoint,
                    data : data,
                    success : function(req)
                    {
                        // TODO: catch form errors here
                        location.reload();
                    },
                    error : function(req)
                    {
                        console.log('Error: ', req);
                    },
                });
            });

            // Remove previous content and add new one
            clean();
            form_container.appendChild(form_node);
        });
    });


    // Fieldsets
    document.querySelectorAll(".collapsible .fieldset__name").forEach(function(el){
        el.addEventListener("click", function(e){
            e.target.parentNode.classList.toggle("collapsed");
        })
    });

    // Map
    // Map
    var geomap_url = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-10m.json";
    var geomap_data = {};
    fetch(geomap_url).then(response=>{
      return response.json();
    }).then(data => {
      var geodata = topojson.feature(
        data,
        data.objects.countries,
      );
      var countries = geodata.features;
      var container = document.querySelector('.layout-form-audioset__right');
      var W = container.offsetWidth;
      var H = container.offsetHeight;
      var svg = d3.select('#map')
        .append("svg")
        .attr("width",  W)
        .attr("height", H);
      var projection = d3.geoRobinson().translate([
          W/2,
          H/2
      ]).scale(200);
      var path = d3.geoPath().projection(projection);

      svg.selectAll(".countries")
        .data(countries)
        .enter()
        .append("path")
        .attr("class", "countries")
        .attr("d", path)
        .style("stroke", "#2c2c2c")
        .style("stroke-width", 0.5)
        .style("fill", "#888888");
    });
});
