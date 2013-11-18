(function () {

  /** Ajax request to get the status of a document. */
  function progress() {
    alert('progress')
    
//    $.ajax({
//      type: "GER",
//      url: "save_text/",
//      data: text_dict,
//      success: function (payload) {
//        animate_msg("Text saved");
//        $('.docviewer-textView span').text('Text');
//        $('#form-edition').hide();
//        for (var i=0; i<num_page_list.length; i++) {
//          var n = num_page_list[i];
//          var text = viewer.schema.text[n-1];
//          viewer.models.document.originalPageText[n] = text;
//        }
//        end_edition_mode();
//        viewer.schema.loadEdition(payload.edition);
//        viewer.api.redrawEditions();
//      },
//      dataType: 'json',
//      error: function (payload) {
//        animate_msg("ajax error saving text");
//      },
//      complete: function (payload) {
//        viewer.api.setCurrentPage(currentPage);
//        viewer.events.loadText(currentPage-1);
//      }
//    });
//    
//    modified_pages = [];
//    $('.docviewer-textInput').val("");
  }
  
  /** Bind the event to its respective elements. */
  $(document).ready(function () {debugger;
    $("#antonio").live('click', function (ev) {
      progress();
    });
  });

}());
