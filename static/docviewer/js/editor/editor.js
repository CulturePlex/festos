/*global alert,docviewer,reload_url,$,mydocviewer:true*/
/*global Ext*/
/*global Jed*/
/*global i18n*/
/*global FBL*/
/*global DEBUG*/
/*global yepnope*/
/*global PhoneGap*/
/*global MathJax*/
/*global JSON*/
/*global console*/
/*global printStackTrace*/
/*global head*/
/*global jQuery*/
/*jslint forin:true, noarg:true, noempty:true, eqeqeq:true, bitwise:true, strict:false, undef:true, curly:true, browser:true, indent:2, maxerr:50
*/

var modified_pages = [];
var restore = false;

(function () {
  "use strict";
  var annotation_page = 0,
    docviewer_cover = "";

  /** Utility function to indicate messages */
  function animate_msg(message) {
    $("#fixed-div").html(message);
    $("#fixed-div").fadeIn(1000);
    $("#fixed-div").delay(2000);
    $("#fixed-div").fadeOut(2000);
  }

  /** Returns the coordinates of the current annotation */
  function get_coord_annotation() {
    var anno = $('#annotation-area'),
      zoomfactor = mydocviewer.models.pages.zoomFactor(),
      anno_offsetX = anno.position().left,
      anno_offsetY = anno.position().top,
      y_initial = 5 + Math.round((anno_offsetY) / zoomfactor),
      y_end =   5 + Math.round((anno_offsetY + anno.height()) / zoomfactor),
      x_initial = 7 + Math.round((anno_offsetX) / zoomfactor),
      x_end =   16 + Math.round((anno_offsetX + anno.width()) / zoomfactor);
    return y_initial + "," + x_end + "," + y_end + "," + x_initial;
  }

  /** Binds the events of the mouse for the selection mode */
  function bind_mouse_events() {
    $('.docviewer-cover').css('cursor', 'crosshair');
    var ev_down = 0,
      selection_area = $('#annotation-area');
    if (selection_area.length === 0) {
      selection_area = jQuery('<div/>', {
        id: 'annotation-area',
        html: '<span id="instruction"> Drag and resize me</span>'
      });
    }
    $('.docviewer-cover').live('mousedown', function (ev_down) {
      var docviewer_set = $(ev_down.target).parents('.docviewer-set');
      if (ev_down.target.className === 'docviewer-cover') {
        docviewer_cover = $(ev_down.target);
      } else {
        docviewer_cover = $(ev_down.target).parents('.docviewer-cover');
      }
      selection_area.css('position', 'absolute');
      selection_area.css('top', ev_down.offsetY);
      selection_area.css('left', ev_down.offsetX);
      annotation_page = mydocviewer.api.currentPage();
      docviewer_cover.prepend(selection_area);
      $('.docviewer-cover').live('mousemove', function (ev) {
        var height = Math.max(Math.abs(ev_down.pageY - ev.pageY), 50),
          width = Math.max(Math.abs(ev_down.pageX - ev.pageX), 50);
        if (ev_down.pageY < ev.pageY) {
          selection_area.css('top', ev_down.offsetY);
        } else {
          selection_area.css('top', ev.offsetY);
        }
        if (ev_down.pageX < ev.pageX) {
          selection_area.css('left', ev_down.offsetX);
        } else {
          selection_area.css('left', ev.offsetX);
        }
        selection_area.css('height', height);
        selection_area.css('width', width);
      });
    });
    $('.docviewer-cover').live('mouseup', function (ev) {
      $('.docviewer-cover').die('mousedown');
      $('.docviewer-cover').die('mousemove');
      $('.docviewer-cover').css('cursor', 'default');
      $('#annotation-area').resizable().draggable();
      $('#form-annotation').show();
    });
  }

  /** Enable the events that allows the selection of an annotation. */
  function enable_selection_mode() {
    $('#add-annotation').hide();
    $('#cancel-annotation').show();
    $('.docviewer-annotations').hide();
    mydocviewer.dragReporter.unBind();
    bind_mouse_events();
  }

  /** Disable the events that allows the selection of an annotation. */
  function disable_selection_mode() {
    $('#add-annotation').show();
    $('#cancel-annotation').hide();
    $('.docviewer-annotations').show();
    $('.docviewer-pages').css('overflow', 'auto');
    $('.docviewer-cover').css('cursor', '-webkit-grab');
    $('.docviewer-cover').die('mousedown');
    $('.docviewer-cover').die('drag');
    $('.docviewer-cover').die('mouseup');
    $('#annotation-area').remove();
    $('#form-annotation').hide();
    mydocviewer.dragReporter.setBinding();
  }

  /** Ajax request to add an annotation. */
  function add_annotation(title, content, location) {
    var adata = { };
    adata.title = $('#annotation-title').val();
    adata.content = $('#annotation-content').val();
    adata.location = get_coord_annotation();
    adata.page_id = mydocviewer.api.currentPage();
    $.ajax({
      url: "add_annotation/",
      data: adata,
      success: function (payload) {
        var zoomLevel = mydocviewer.models.pages.zoomLevel;
//        console.log(zoomLevel);
        load_document(function () {
          mydocviewer.pageSet.zoom({zoomLevel: zoomLevel });
          mydocviewer.api.setCurrentPage(adata.page_id);
          disable_selection_mode();
          animate_msg("Annotation saved");
        });
      },
      dataType: 'json',
      error: function (payload) {
        alert("Ajax request error");
      },
      type: 'GET'
    });
  }

  /** Ajax request to update an annotation. */
  function update_annotation(id, field, value) {
    var adata = { };
    adata.id = id;
    adata[field] = value;
    $.ajax({
      type: "GET",
      url: "update_annotation/",
      data: adata,
      success: function (payload) {
        animate_msg("Annotation updated");
        value.trim();
      },
      dataType: 'json',
      error: function (payload) {
        animate_msg("Error en el ajax request");
      }
    });
  }

  /** Ajax request to remove an annotation. */
  function remove_annotation(id) {
    var adata = { };
    adata.id = id;
    $.ajax({
      url: "remove_annotation/",
      data: adata,
      success: function (payload) {
        var current_page = mydocviewer.api.currentPage(),
          zoomLevel = mydocviewer.models.pages.zoomLevel;
        load_document(function () {
          mydocviewer.pageSet.zoom({zoomLevel: zoomLevel });
          mydocviewer.api.setCurrentPage(current_page);
          animate_msg("Annotation removed");
        });
      },
      dataType: 'json',
      type: 'GET'
    });
  }


  /** Bind the events for editing the title of an annotation. */
  function bind_title_events() {
    var title = "";
    $('.docviewer-annotationTitle').live('click', function (ev) {
      title = ev.target.innerText;
      ev.target.contentEditable = 'true';
      $(ev.target).focus();
    });
    $('.docviewer-annotationTitle').live('blur', function (ev) {
      if (title !== ev.target.innerText) {
        // avoid null annotations
        if (ev.target.innerText.trim() !== "") {
          update_annotation(
            $(ev.target).parents(".docviewer-annotation")[0].dataset.id,
            'title',
            ev.target.innerText.trim()
          );
        } else {
          ev.target.innerText = title;
          animate_msg("Cannot have annotations without a title");
        }
      }
      ev.target.contentEditable = 'false';
    });
    $('.docviewer-annotationTitle').live('keypress', function (ev) {
      if (ev.keyCode === 13) {
        ev.target.blur();
      }
    });
  }

  /** Bind the events for editing the content of an annotation. */
  function bind_content_events() {
    var content = "",
      empty = $('<span/>', {
        'class': 'empty',
        text: 'Click here to add a description'
      });
    $('div.docviewer-annotationBody').live('click', function (ev) {
      var body = ev.target;
      if (ev.target.className === "empty") {
        body = ev.target.parentElement;
        $(ev.target).remove();
      }
      content = body.innerText;
      body.contentEditable = 'true';
      $(body).focus();
    });
    $('.docviewer-annotationBody').live('blur', function (ev) {
      if (content !== ev.target.innerText) {
        update_annotation(
          $(ev.target).parents(".docviewer-annotation")[0].dataset.id,
          'content',
          ev.target.innerText.trim()
        );
      }
      if (ev.target.innerText.trim() === "") {
        $(ev.target).empty();
        $(ev.target).append(empty);
      }
      ev.target.contentEditable = 'false';
    });
    $('.docviewer-annotationBody').live('keypress', function (ev) {
      if (ev.keyCode === 13) {
        ev.target.blur();
      }
    });
  }

  /** Hide the annotation area when the page changes */
//  function hide_anno_on_page_change() {
//    mydocviewer.states.events.observerPage = function () {
//      if (mydocviewer.state !== 'ViewDocument') { return; }
//      var anno = $('#annotation-area');
//      if (anno.length === 0) { return; }
//      if (mydocviewer.api.currentPage() >= annotation_page - 1 &
//          mydocviewer.api.currentPage() <= annotation_page + 1) {
//        anno.show();
//      } else {
//        anno.hide();
//      }
//    };
//    mydocviewer.states.helpers.addObserver("observerPage");
//  }

  /** Hide the annotation area when the page changes */
  function hide_anno_edit_his_on_page_change() {
    mydocviewer.states.events.observerPage = function () {
      var state = mydocviewer.state;
      if (state !== 'ViewDocument') {
        $('#annotation-options').hide();
        if (state !== 'ViewText') {
          $('#edition-options').hide();
          $('#history-versions').hide();
        } else {
          if (restore == false)
            $('#edition-options').show();
          $('#history-versions').show();
        }
      } else {
        $('#annotation-options').show();
        $('#edition-options').hide();
        $('#history-versions').hide();
        var anno = $('#annotation-area');
        if (anno.length === 0) { return; }
        if (mydocviewer.api.currentPage() >= annotation_page - 1 &
            mydocviewer.api.currentPage() <= annotation_page + 1) {
          anno.show();
        } else {
          anno.hide();
        }
      }
    };
    mydocviewer.states.helpers.addObserver("observerPage");
  }


  /** Enable restoring. */
  function enable_restoring_mode() {
    restore = true;
    $('#form-restoring').show();
    $('#edition-options').hide();
    $(".plain-text-area").addClass('restore');
  }

  /** Disable restoring. */
  function disable_restoring_mode() {
    restore = false;
    $('#form-restoring').hide();
    $('#edition-options').show();
    $(".plain-text-area").removeClass('restore');
  }


  /** Enable the events that allows the edition of text. */
  function enable_edition_mode() {
    $('#add-edition').hide();
    $('#cancel-edition').show();
//    $('#form-edition').show();
    editText();
  }

  /** Disable the events that allows the edition of text. */
  function disable_edition_mode() {
    $('#add-edition').show();
    $('#cancel-edition').hide();
    $('#form-edition').hide();
    uneditText();
  }

  /** End the events that allows the edition of text. */
  function end_edition_mode() {
    $('#add-edition').show();
    $('#cancel-edition').hide();
    $('#form-edition').hide();
    endEditText();
  }
  
  function editText() {
    var id = window.location.pathname.split('/')[2];
    docviewer.viewers["doc-"+id].api.enterEditPageTextMode();
  }
  
  function uneditText() {
    var id = window.location.pathname.split('/')[2];
    docviewer.viewers["doc-"+id].api.leaveEditPageTextMode();
    $('.docviewer-textView span').text('Text');
    $('#form-edition').hide();
    asterisk();
    modified_pages = [];
    $('.docviewer-textInput').val("");
  }
  
  function endEditText() {
    var id = window.location.pathname.split('/')[2];
    docviewer.viewers["doc-"+id].api.endEditPageTextMode();
    $('.docviewer-textView span').text('Text');
    $('#form-edition').hide();
    asterisk();
  }

  /** Ajax request to save text. */
  function save_text(num_page_list) {
    var id = window.location.pathname.split('/')[2];
    var viewer = docviewer.viewers["doc-"+id];
    var currentPage = viewer.api.currentPage();
    
    var text_dict = {};
    text_dict['comment'] = $('.docviewer-textInput').val();
    var rel_art = viewer.schema.document.resources.related_article;
    var rel_art_len = rel_art.length
    text_dict['textURI'] = viewer.schema.document.resources.page.text.substring(rel_art_len);
    for (var i=0; i<num_page_list.length; i++) {
      var n = num_page_list[i];
      var text = viewer.schema.text[n-1];
      text_dict[n] = text;
    }
    
    $.ajax({
      type: "POST",
      url: "save_text/",
      data: text_dict,
      success: function (payload) {
        animate_msg("Text saved");
        $('.docviewer-textView span').text('Text');
        $('#form-edition').hide();
        for (var i=0; i<num_page_list.length; i++) {
          var n = num_page_list[i];
          var text = viewer.schema.text[n-1];
          viewer.models.document.originalPageText[n] = text;
        }
        end_edition_mode();
        viewer.schema.loadEdition(payload.edition);
        viewer.api.redrawEditions();
      },
      dataType: 'json',
      error: function (payload) {
        animate_msg("ajax error saving text");
      },
      complete: function (payload) {
        viewer.api.setCurrentPage(currentPage);
        viewer.events.loadText(currentPage-1);
      }
    });
    
    modified_pages = [];
    $('.docviewer-textInput').val("");
  }

  /** Bind the events for u pdating the text. */
  function bind_text_events() {
    $('.plain-text-area.docviewer-editing').live('blur', function (ev) {
      var id = window.location.pathname.split('/')[2];
      var viewer = docviewer.viewers["doc-"+id];
      var currentPage = viewer.api.currentPage();
      var text = $('#plain-text-area-'+currentPage).text();
      if (viewer.schema.text[currentPage-1] != text) {
        viewer.schema.text[currentPage-1] = text;
        modified_pages.push(currentPage);
      }
      else {
        if (modified_pages.length == 0) {
          $('.docviewer-textView span').text('Text');
          $('#form-edition').hide();
          asterisk();
        }
      }
    });
    asterisk();
  }

  function asterisk() {
    $('.plain-text-area.docviewer-editing').live('keyup', function (ev) {
      var id = window.location.pathname.split('/')[2];
      var viewer = docviewer.viewers["doc-"+id];
      var currentPage = viewer.api.currentPage();
      var text = $('#plain-text-area-'+currentPage).text();
      if (viewer.schema.text[currentPage-1] != text) {
        $('.docviewer-textView span').text('Text*');
        $('#form-edition').show();
        $('.plain-text-area.docviewer-editing').die('keydown');
      }
    });
  }

  /** Restore a document version. */
  function restoreVersion(ts) {
    var id = window.location.pathname.split('/')[2];
    var viewer = docviewer.viewers["doc-"+id];
    var currentPage = viewer.api.currentPage();
    
    $.ajax({
      type: "POST",
      url: "restore_version/",
      data: {'ts': ts},
      success: function (payload) {
//        animate_msg("Version restored");
        var mod_pags = payload.modified_pages;
        var keys = Object.keys(mod_pags);
        for (var k = 0; k < keys.length; k++) {
          (function(key) {
              var n = keys[key];
              var url = mod_pags[n];//+ "?x="+(new Date()).getTime();
              var nump = parseInt(n);
              $.ajax({
                type: 'GET',
                url: url,
                success: function (data) {
                  viewer.schema.text[nump-1] = data;
                  viewer.models.document.originalPageText[nump] = data;
                  viewer.events.loadText(nump-1);
                },
                error: function (data) {
                    animate_msg("File not found.")
              }})
          })(k);
        }
        modified_pages = _.range(1, viewer.models.document.totalPages+1);
//        for (var i = 0; i < modified_pages.length; i++) {
//            viewer.events.restoreText(i);
//        }
        $('.docviewer-textInput').val("");
      },
      dataType: 'json',
      error: function (payload) {
        animate_msg("ajax error restoring version");
      },
      complete: function (payload) {
        viewer.api.setCurrentPage(currentPage);
        viewer.events.loadText(currentPage-1);
      }
    });
  }

  /** Bind the event to its respectives elements. */
  $(document).ready(function () {
    bind_content_events();
    bind_title_events();
    $("#add-annotation").live('click', function (ev) {
      enable_selection_mode();
    });
    $("#cancel-annotation").live('click', function (ev) {
      disable_selection_mode();
    });
    $('#annotation-button').live('click', function (ev) {
      ev.preventDefault();
      add_annotation();
    });
    $(".docviewer-remove").live('click', function (ev) {
      remove_annotation(
        $(ev.target).parents(".docviewer-annotation")[0].dataset.id
      );
    });
    
    bind_text_events();
    $("#add-edition").live('click', function (ev) {
      enable_edition_mode();
    });
    $("#cancel-edition").live('click', function (ev) {
      disable_edition_mode();
    });
    $('#edition-button').live('click', function (ev) {
      save_text(modified_pages);
    });
    
    hide_anno_edit_his_on_page_change();
    
    $(".docviewer-historyLink").live('click', function (ev) {
      enable_restoring_mode();
      restoreVersion(ev.currentTarget.id);
    });
    $("#restore-button").live('click', function (ev) {
      save_text(modified_pages);
      disable_restoring_mode();
    });
    $("#cancel-restore-button").live('click', function (ev) {
      restoreVersion('99999999999999999999');
      disable_restoring_mode();
    });
  });

}());
