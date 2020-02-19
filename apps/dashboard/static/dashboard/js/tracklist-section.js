/**
 *  Dashboard scripts
 *  Tracklist screen
 */

document.addEventListener("DOMContentLoaded", function()
{
    // Modals
    document.querySelectorAll("[data-modal-show]").forEach(function(el){
        var d = el.dataset;
        var modal_name   = d.modalShow + '[data-model=' + d.modalModel + ']';
        var modal_node   = document.querySelector(modal_name);
        var modal_action = d.modalShowId ? 'update' : 'create';
        el.addEventListener("click", function(){
            modal_node.classList.add('visible');
            modal_node.setAttribute('data-action', modal_action)
        })
    });

    // TODO: add a handler to remove the call to querySelectorAll
    //       detecting 'visible' properly (it's not straighf cause
    //       it's added async)
    document.querySelectorAll("[data-modal-close]").forEach(function(el){
        var modal_name = '.form-modal';
        var modal_nodes = document.querySelectorAll(modal_name);
        el.addEventListener("click", function(e){
            modal_nodes.forEach(function(node){
              node.classList.remove('visible');
            })
        })
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
