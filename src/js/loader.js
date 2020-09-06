/*jslint browser: true*/
/*global $, Handlebars, console*/

$(document).ready(function () {
  var grid = $(".grid");
  var qsRegex;

  // prepare dropdowns
  $('.dropdown-trigger').dropdown({ coverTrigger : false });
  // prepare sidenav for mobile
  $('.sidenav').sidenav();
  // collapsibles
  $('.collapsible').collapsible();

  // prepare isotope filtering with dict and custom filtering function
  var filters = {};
  var isotopeFilters;
  function concatValues( obj ) {
    var value = '';
    for ( var prop in obj ) {
      value += obj[ prop ];
    }
    return value;
  }

  // sidenav: populate collapsibles with same content as dropdowns
  // quick and dirty copy over from the actual dropdowns
  var filtercat = document.getElementById("dropdown-cat").cloneNode(true);
  filtercat.classList.remove("dropdown-content");
  document.getElementById("collapsible-cat").innerHTML = filtercat.outerHTML;

  var filtergeo = document.getElementById("dropdown-geo").cloneNode(true);
  filtergeo.classList.remove("dropdown-content");
  document.getElementById("collapsible-geo").innerHTML = filtergeo.outerHTML;

  // isotope: filter cards, intersect filters with different groups
  $(".slid-filter").on('click', function() {

    // retrieve what group we are filtering, and the filter value
    var filterValue = $(this).attr('filter');
    var filterGroup = $(this).attr('slid-group');

    // update filters dictionary, concatenate values for each group
    filters[filterGroup] = filterValue;
    isotopeFilters = concatValues(filters);

    grid.isotope();

    // uncheck other filters in the group and check the new one
    $(".active", ".slid-" + filterGroup + "-dropdown").removeClass('active');
    $(this).parent().addClass('active');
  });


  // load isotope
  var $grid = grid.isotope({
    itemSelector: ".card",
    layoutMode: "packery",
    filter: function() {
      // var $this = $(this);
      var searchResult = qsRegex ? $(this).text().match( qsRegex ) : true;
      var buttonResult = isotopeFilters ? $(this).is( isotopeFilters ) : true;
      return searchResult && buttonResult;
    },
    getSortData: {
      name: "[data-name]"
    },
    sortBy: "name"
  });

  // Pressing shuffle button randomises sort order
  $(".shuffle-button").on('click', function() {
    grid.isotope('shuffle');
  });

  // use value of search field to filter
  var search = $('#search').keyup(debounce(function() {
    qsRegex = new RegExp(search.val(), "gi");
    grid.isotope();
  }, 200 ));

  // debounce so filtering doesn't happen every millisecond
  function debounce(fn, threshold) {
    var timeout;
    return function debounced() {
      if (timeout) {
        clearTimeout(timeout);
      }
      function delayed() {
        fn();
        timeout = null;
      }
      timeout = setTimeout(delayed, threshold || 100);
    }
  }
});
