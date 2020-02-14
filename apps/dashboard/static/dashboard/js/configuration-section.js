/**
 *  Dashboard scripts
 *  Configuration screen
 */

document.addEventListener("DOMContentLoaded", function(){

    // Add listeners
    var mode_selector = document.querySelector('.mode-selector');
    document.querySelectorAll("[name='mode_display']").forEach(function(selector){
        selector.addEventListener('change', function(e){
            var value = e.target.value;
            mode_selector.dataset.currentState = value;
        });
    });

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
      var container = document.querySelector('.mode-selector');
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
