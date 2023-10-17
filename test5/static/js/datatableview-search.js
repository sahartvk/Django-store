$(document).ready(function () {

    var table = $('#DataTables_Table_0').DataTable();

    // Apply the search
    $('#apply-filter').click(function() {
        $('.search-input').each(function(index) {
          var inputValue = $(this).val();
          table.column(index).search(inputValue);
        });
//        $('.filter-range').each(function() {
//            var column = $(this).data('column');
//            var minVal = parseFloat($(this).eq(0).val());
//            var maxVal = parseFloat($(this).eq(1).val());
//
//            if (!isNaN(minVal) && !isNaN(maxVal)) {
//            table.column(column).search(minVal + '-' + maxVal, true, false);
//            } else if (!isNaN(minVal)) {
//            table.column(column).search('>=' + minVal, true, false);
//            } else if (!isNaN(maxVal)) {
//            table.column(column).search('<=' + maxVal, true, false);
//            } else {
//            table.column(column).search('');
//            }
//        });
        table.draw();
        // Rest of your AJAX code for sending data to the server...
    });

    // Clear the filter inputs
    $('#clear-filter').click(function() {
        $('.search-input').val('');
        $('.filter-range').val('');
        table.columns().search('').draw();
    });

  // Handle the link click to send data to the server
  $('#send-data').click(function (e) {
    e.preventDefault(); // Prevent the default behavior of the link

    // Collect input values from each input box
    var searchData = {};
    $('.search-input').each(function () {
      var columnName = $(this).attr('search_for');
      var inputValue = $(this).val();
      searchData[columnName] = inputValue;
    });
    // Get CSRF token from cookies
    var csrftoken = getCookie('csrftoken');

    // Send data to the server using AJAX
    $.ajax({
      url: exportApi,
      type: 'POST',
      //data: JSON.stringify(searchData),
      data: searchData,
      xhrFields: {
          responseType: 'blob' // to avoid binary data being mangled on charset conversion
      },
      //contentType: 'application/json',

      beforeSend: function (xhr) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set the CSRF token header
      },
      success: function (blob, status, xhr) {
        var filename = "";
        var disposition = xhr.getResponseHeader('Content-Disposition');
        if (disposition && disposition.indexOf('attachment') !== -1) {
            var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            var matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
        }

        if (typeof window.navigator.msSaveBlob !== 'undefined') {
            // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
            window.navigator.msSaveBlob(blob, filename);
        } else {
            var URL = window.URL || window.webkitURL;
            var downloadUrl = URL.createObjectURL(blob);

            if (filename) {
                // use HTML5 a[download] attribute to specify filename
                var a = document.createElement("a");
                // safari doesn't support this yet
                if (typeof a.download === 'undefined') {
                    window.location.href = downloadUrl;
                } else {
                    a.href = downloadUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                }
            } else {
                window.location.href = downloadUrl;
            }

            setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
        }
      },
      error: function (error) {
        console.error('Error:', error);
      }
    });
  });
});
// Function to get CSRF token from cookies
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
