/**
 *  Tracklist section map
 *  Configuration screen
 */

function loadMap(map_scale, map_center_x, map_center_y, draggable, audioset)
{
    // Map container and main elements
    var container = document.querySelector('.layout-form-audioset__right').getBoundingClientRect();
    var W = container.width;
    var H = container.height;

    var svg = d3.select('#map')
      .append("svg")
      .attr("width",  W)
      .attr("height", H);

    // Map projection
    var projection  = d3.geoRobinson().translate([
        W/2 + map_center_x,
        H/2 + map_center_y
    ]).scale(map_scale);
    var path = d3.geoPath().projection(projection);

    // Load map
    d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', function(error, data)
    {
        if (error) throw error;
        var countries = topojson.feature(
          data,
          data.objects.countries,
        ).features;

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

        if(audioset){
            d3.json('/api/1.0/track/clips/'+audioset, function(error, data)
            {
                svg.selectAll(".map__clip-marker")
                  .data(data)
                  .enter()
                  .append('circle')
                  .attr('class', 'map__clip-marker')
                  .attr('data-id', function(d){ return d.pk })
                  .attr('r', 10)
                  .attr('fill', function(d){ return d.track[0].color })
                  .attr('stroke', 'rgba(0, 0, 0, .15)')
                  .attr('stroke-width', '8')
                  .attr("transform", function(d){
                      return 'translate('+ (W/2 - d.pos_x) + ',' + (H/2 - d.pos_y) + ')'
                  })
                  .on('click', function(d){
                      document.querySelector('.clip-actions__edit[data-id="'+d.pk+'"]').click();
                  })
            })
        }
    });

    // Map drag options
    var zoom = null;
    if(draggable){
        zoom = d3.behavior.zoom()
          .translate([ W/2 + map_center_x, H/2 + map_center_y ])
          .scale(map_scale)
          .scaleExtent([250, 2000])
          .on("zoom", zoomed);
        svg.call(zoom).call(zoom.event);
    }
    function zoomed()
    {
        var translation = zoom.translate();
        var scalation   = zoom.scale();
        projection.translate( translation ).scale( scalation );
        svg.selectAll('.countries').attr("d", path)
        document.querySelector('#id_map_scale').value = scalation;
        document.querySelector('#id_map_center_x').value = translation[0] - W/2;
        document.querySelector('#id_map_center_y').value = translation[1] - H/2;
    }

    // Populate map with clips

    // Map finder
    document.querySelector('.map__finder').addEventListener('submit', function(e){
        e.preventDefault();
        var place = document.querySelector('.map__finder input[type=text]').value;
        if(place){
            var url = "https://nominatim.openstreetmap.org/search/" + encodeURIComponent(place) + "?format=json";
            jQuery.ajax({
                type : 'GET',
                url  : url,
                success : function(response)
                {
                    // TODO: handle rejections and coordinates outside of current projection bounding box
                    var projection_coords = projection([ response[0].lon, response[0].lat ]);
                    svg.append("circle")
                      .attr('class','marker')
                      .attr('r', 10)
                      .attr('fill', 'green')
                      .attr('stroke', '#7ffa07')
                      .attr('stroke-width', '8')
                      .attr("transform", function(d){
                          return 'translate('+ projection_coords + ')'
                      });
                    document.querySelector('#id_pos_y').value = parseInt( H/2 - projection_coords[1] );
                    document.querySelector('#id_pos_x').value = parseInt( W/2 - projection_coords[0] );

                    // var data = JSON.parse(response)[0];
                },
                error : function(req){
                    console.log('Error: ', req);
                },
            });
        }
    });
}
