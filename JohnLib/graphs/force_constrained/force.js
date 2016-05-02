
var w = 1000,
    h = 800,
    fill = d3.scale.category20();  // from example

var vis = d3.select("#chart")
  .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("force.json", function(json) {
  var force = d3.layout.force()
      .charge(-120)
      .nodes(json.nodes)
      .links(json.links)
      .size([w, h]);


  var marker = vis.append("svg:defs").selectAll("marker")
        .data(["end"])      // Different link/path types can be defined here
        .enter().append("svg:marker")    // This section adds in the arrows
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 21)  // how far away from the end of the line (approx 2x radius)
        .attr("refY", 0)   // offset from center of the line
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0,-5L10,0L0,5");

  var link = vis.selectAll("line.link")
      .data(json.links)
      .enter().append("svg:line")
      .attr("class", "link")
      .style("stroke-width", 1.5)   // side effect: controls arrow size
      //.style("stroke-width", function(d) { return Math.sqrt(d.value); })
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; })
      .attr("linkDistance", function(d) { return d.linkDistance; })
      .attr("marker-end", "url(#end)");  // adds the arrows

    force.linkDistance(function(link){
       return link.linkDistance;
       });
      // http://bl.ocks.org/sathomas/83515b77c2764837aac2
    force.start();

  var node = vis.selectAll("circle.node")
      .data(json.nodes)
    .enter().append("svg:circle")
      .attr("class", "node")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("depth", function(d) { return d.depth; })
      .attr("r", 10)
      .style("fill", function(d) { return d.fill; })
      .call(force.drag);

  node.append("svg:title")
      .text(function(d) { return d.name; });

  vis.style("opacity", 1e-6)
    .transition()
      .duration(1000)
      .style("opacity", 1);

  force.on("tick", function(e) {
    // Add extra forces

    var kx = 1.2 * e.alpha;

    node.forEach(function(d, i) {
      d.x += (d.depth - d.x) * kx;
    });
    /*
    link.forEach(function(d, i) {
      d.target.x += (d.target.depth * 120 - d.target.x) * kx;
    });
    */

    node.attr("cx", function(d) {
        d.x += (d.depth - d.x) * kx;
      return d.x; })
        .attr("cy", function(d) { return d.y; });

    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });


  });
});
