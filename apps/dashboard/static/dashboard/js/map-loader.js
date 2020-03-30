/**
 *  Tracklist section map
 *  Configuration screen
 */

function loadMap(map_scale, map_center_x, map_center_y, draggable)
{
    // Map container and main elements
    var container = document.querySelector('.layout-form-audioset__right').getBoundingClientRect();
    var W = container.width;
    var H = container.height;

    var svg = d3.select('#map')
      .append("svg")
      .attr("width",  W)
      .attr("height", H);
    var g = svg.append("g");

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

}
