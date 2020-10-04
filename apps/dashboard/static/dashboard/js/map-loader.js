/**
 *  Tracklist section map
 *  Configuration screen
 */

function loadMap(map_scale, map_center_x, map_center_y, is_map_conf, audioset)
{
    // Map container and main elements
    var container = document.querySelector('.layout-form-audioset__right');
    var W = container.clientWidth;
    var H_target = document.querySelector('.form--simple') || container;
    var H = H_target.clientHeight;
    var scale_factor = W / 6.5;

    var svg = d3.select('#map')
      .append("svg")
      .attr("width",  W)
      .attr("height", H);

    // Create default map projection
    var projection  = d3.geoRobinson()
      .center([ map_center_x, map_center_y ])
      .scale(map_scale * scale_factor)
      .translate([ W/2, H/2 ]);
    var path = d3.geoPath().projection(projection);

    // Load map
    d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', function(error, data)
    {
        if (error) throw error;
        var countries = topojson.feature(
          data,
          data.objects.countries,
        ).features;

        // Create paths for countries in the map
        //
        svg.selectAll('.countries')
          .data(countries)
          .enter()
          .append("path")
          .attr("class", "countries")
          .attr("d", path)
          .attr("class", "countries")
          .style("stroke", "#2c2c2c")
          .style("stroke-width", 0.5)
          .style("fill", "#888888");

        // If in tracklist section
        // load clip markers
        //
        if(!is_map_conf && audioset){
            document.querySelector('.layout-form-audioset').classList.add('saving');
            d3.json('/api/1.0/track/clips/'+audioset, function(error, data)
            {
                svg.selectAll(".clip-marker")
                  .data(data)
                  .enter()
                  .append('circle')
                  .attr('class', 'clip-marker clip-marker--map')
                  .attr('data-id', function(d){ return d.pk })
                  .attr('r', 10)
                  .attr('fill', function(d){ return d.track[0].color })
                  .attr('stroke', 'rgba(0, 0, 0, .15)')
                  .attr('stroke-width', '8')
                  .attr("transform", function(d)
                  {
                      return 'translate('+ projection([d.pos_x, d.pos_y]) + ')'
                  })
                  .on('click', function(d){
                      document.querySelector('.clip-actions__edit[data-id="'+d.pk+'"]').click();
                  })
                  document.querySelector('.layout-form-audioset').classList.remove('saving');
            })
        }
    });

    // If in map configuration section
    // allow to zoom to set desired scale
    //
    var zoom = null;
    if(is_map_conf){
        zoom = d3.behavior.zoom()
          .translate([ W/2, H/2 ])
          .scale(map_scale * scale_factor)
          .scaleExtent([W/6.5, 2000])
          .on("zoom", zoomed);
        svg.call(zoom).call(zoom.event);
    }
    function zoomed()
    {
        var scalation   = zoom.scale();
        projection.scale( scalation );
        svg.selectAll('.countries').attr("d", path);
        document.querySelector('#id_map_scale').value = parseInt(scalation / scale_factor);
    }

    // Map finder behavior
    //
    var map_finder = document.querySelector('.background-field__submit');
    map_finder.addEventListener('click', function(e)
    {
        var place = document.querySelector('.background-field__input').value;
        if(place)
        {
            document.querySelector('.layout-form-audioset').classList.add('saving');
            // makes a lookup in nominatim database
            var url = "https://nominatim.openstreetmap.org/search/" + encodeURIComponent(place) + "?format=json";
            var placeholder =  document.querySelector('.clip-marker--placeholder');
            d3.json(url, function(error, data)
            {
                // If lookup was succesful use first —most relevant— finding
                // else display a warning
                var place = null;
                if(data.length > 0){
                    place = data[0];
                    document.querySelector('.background-field__warning').classList.add('hidden');
                } else {
                    document.querySelector('.background-field__warning').classList.remove('hidden');
                    document.querySelector('.layout-form-audioset').classList.remove('saving');
                    return;
                }
                // TODO: handle rejections and coordinates outside of current projection bounding box
                if(is_map_conf){
                    // If in map configuration section
                    // use data to center the map
                    projection.center([
                        place.lon,
                        place.lat
                    ]).scale( zoom.scale() ).translate( zoom.translate() );
                    // Shift shapes
                    svg.selectAll('.countries').attr("d", path);
                    // Update inputs
                    document.querySelector('#id_map_center_x').value = place.lon;
                    document.querySelector('#id_map_center_y').value = place.lat;
                } else {
                    // If in tracklist section
                    // use data to append a marker and update current clip
                    var coords = projection([
                        place.lon,
                        place.lat
                    ]);
                    if(!placeholder){
                        svg.append("circle")
                          .attr('class','clip-marker clip-marker--placeholder')
                          .attr('r', 10)
                          .attr('fill', 'green')
                          .attr('stroke', '#7ffa07')
                          .attr('stroke-width', '8')
                          .attr("transform", function(d){
                              return 'translate('+ coords + ')'
                          });
                    } else {
                        d3.select('.clip-marker--placeholder')
                        .attr("transform", function(d){
                            return 'translate('+ coords + ')'
                        });
                    }

                    document.querySelector('#id_pos_x').value = place.lon;
                    document.querySelector('#id_pos_y').value = place.lat;
                }
                  document.querySelector('.layout-form-audioset').classList.remove('saving');
            });
        }
    });
}
