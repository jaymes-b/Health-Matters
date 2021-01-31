// Javascript function
// How to connect to python function and use data there
function getResult() {
  // Uses AJAX to connect to the backend server
  $.ajax({
    // Python Flask url
    url: "/view",
    success: function(result) {
      console.log("received result: " + result);

      // For each item in the list that is returned in the Python function, we add the equivalent table HTML string
      // For each loop
      $.each(JSON.parse(result), function(index, item){
        console.log("added");
        // Appending HTML
        $('#result_table').append('<tr><td>' + item.name + '</td><td>' + item.genre + '</td><td>' + item.time + '</td></tr>');
      });
    }
  });
}
