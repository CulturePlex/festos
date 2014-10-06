$(document).ready(function(){
    var TIME = 10000
    var timer = window.setInterval(getStatus, TIME);
    
    function getStatus() {
      window.clearInterval(timer);
      
      docs = $(".document-status");
      var doc_ids = $.map(docs, function(d) {
        return $(d).attr('data-document-id');
      });
      if(doc_ids.length > 0)
        progress(doc_ids);
    }
    
    function progress(doc_ids) {
      $.ajax({
        type: "GET",
        url: "progress/",
        data: {'ids': doc_ids},
        dataType: 'json',
        success: function (payload) {
          var counter_in_progress_docs = 0;
          for(var i=0; i<doc_ids.length; i++){
            var doc_id = doc_ids[i];
            var dict = payload[doc_id];
            
            var npages = dict["total_pages"]
            var doc_npages = $('.document-row[data-id="'+doc_id+'"]').children().filter('.document-pages');
            doc_npages.children().html(npages);
            
            var doc_st = $('.document-status[data-document-id="'+doc_id+'"]');
            doc_st.attr('data-document-status', dict['status']);
            var div_content = doc_st.children().first();
            div_content.text(dict["status"]);
            div_content.removeClass();
            div_content.addClass("label");
            
            div_content.attr("align", "center");
            
            if(dict["status"] == "failed") {
              var docSt = doc_st.attr("data-actions-state-machine");
              if (!(docSt && docSt.indexOf("CANCEL-") == 0))
                doc_st.attr("data-actions-state-machine", "FAILED");
              div_content.addClass("label-important");
              doc_st.parent().children().last().children().filter("[id='retry']").show();
              var doc_error = $(".document-info#"+doc_id);
              if(dict["error"]) {
                doc_error.attr("data-original-title", dict["error"]);
                doc_error.show();
              }
              hookTooltips(doc_error);
            }
            else if(dict["status"] == "ready"){
              var docSt = doc_st.attr("data-actions-state-machine");
              if (!(docSt && docSt.indexOf("CANCEL-") == 0))
                doc_st.attr("data-actions-state-machine", "READY");
              div_content.addClass("label-success");
              var doc_error = $(".document-info#"+doc_id);
              if(dict["error"]) {
                doc_error.attr("data-original-title", dict["error"]);
                doc_error.show();
              }
              //if(dict["total_time"] > "0") {
                //var title = doc_error.attr("data-original-title");
                //if (title)
                //    title += ". ";
                //title += "Total processing time: " + dict["total_time"];
                //doc_error.attr("data-original-title", title);
                //doc_error.show();
              //}
              hookTooltips(doc_error);
              
              var tr_document = doc_st.parent();
              var doc_ttl = tr_document.children(".document-title");
              var span_ttl = doc_ttl.children().first().children().first();
              if(span_ttl.has('a').length == 0) {
                var ttl = span_ttl.data('title');
                var href = span_ttl.attr('data-href');
                span_ttl.html('<a href="'+href+'" style="">'+ttl+'</a>');
              }
            }
            else if(dict["status"] == "waiting") {
              var docSt = doc_st.attr("data-actions-state-machine");
              if (!(docSt && docSt.indexOf("CANCEL-") == 0))
                doc_st.attr("data-actions-state-machine", "PROCESSING");
              doc_st.html('<div align="center"><img src="../static/img/waiting.gif"> <span id="'+doc_id+'" data-toggle="tooltip" data-placement="right" title="Position in line" class="label label-info document-line-position" align="center">'+dict["position"]+'</span></div> <span title="" align="right" class="document-info" id="'+doc_id+'" data-toggle="tooltip" data-placement="right" style="display:none;"><i class="icon-info-sign"></i></span>');
              var positions = $(".document-line-position#"+doc_id);
              hookTooltips(positions);
              counter_in_progress_docs++;
            }
            else if(dict["status"] == "starting") {
              var docSt = doc_st.attr("data-actions-state-machine");
              if (!(docSt && docSt.indexOf("CANCEL-") == 0))
                doc_st.attr("data-actions-state-machine", "PROCESSING");
              doc_st.html('<div class="progress progress-striped active"> <div class="bar bar-success" role="progressbar" aria-valuenow="" aria-valuemin="0" aria-valuemax="100" style="width: 100%"> <span class="sr-only demo-no" style="font-weight:bold;">starting</span> </div></div> <span title="" align="right" class="document-info" id="'+doc_id+'" data-toggle="tooltip" data-placement="right" style="display:none;"><i class="icon-info-sign"></i></span>');
              counter_in_progress_docs++;
            }
            else { <!-- "processing" -->
              var docSt = doc_st.attr("data-actions-state-machine");
              if (!(docSt && docSt.indexOf("CANCEL-") == 0))
                doc_st.attr("data-actions-state-machine", "PROCESSING");
              var np = dict.num_pages;
              var tp = dict.total_pages;
              var per = parseInt(np*100/tp);
              var progress = np + " / " + tp;
              doc_st.html('<div class="progress"> <div class="bar bar-success" role="progressbar" aria-valuenow="" aria-valuemin="'+np+'" aria-valuemax="'+tp+'" style="width: '+per+'%"> <span class="sr-only" style="font-weight:bold;">'+progress+'</span> </div></div> <span title="" align="right" class="document-info" id="'+doc_id+'" data-toggle="tooltip" data-placement="right" style="display:none;"><i class="icon-info-sign"></i></span>');
              counter_in_progress_docs++;
            }
          }
          if(counter_in_progress_docs > 0)
            timer = window.setInterval(getStatus, TIME);
          else
            window.clearInterval(timer);
          
          showActions(doc_ids);
        },
        error: function (payload) {
        },
        complete: function (payload) {
          showActions(doc_ids);
        }
      });
    }
    
    function showActions(doc_ids) {
      for(var i=0; i<doc_ids.length; i++) {
        var doc_id = doc_ids[i];
        var status = $('.document-status[data-document-id="'+doc_id+'"]');
        var actions = $('.document-actions[data-document-id="'+doc_id+'"] a');
        var state = status.attr("data-actions-state-machine");
        var actions_show = actions.filter("."+state);
        actions.hide();
        actions_show.show();
      }
    }
    
    getStatus();
    
    
    $(".document-actions #remove").live('click', function (ev) {
      var status = $(this).parent().parent().children().filter(".document-status");
      status.attr("data-actions-state-machine", "CANCEL-READY");
      var doc_id = status.parent().attr("data-id");
      showActions([doc_id]);
      
      var div_content = status.children().first();
      div_content.text("remove?");
      div_content.removeClass();
      div_content.addClass("label");
      div_content.addClass("label-warning");
    });
    
    $(".document-actions #cancel-remove").live('click', function (ev) {
      var status = $(this).parent().parent().children().filter(".document-status");
      var actionSt = status.attr("data-actions-state-machine");
      if (actionSt == "CANCEL-PROCESSING")
        status.attr("data-actions-state-machine", "PROCESSING");
      else if (actionSt == "CANCEL-FAILED")
        status.attr("data-actions-state-machine", "FAILED");
      else // actionSt == "CANCEL-READY"
        status.attr("data-actions-state-machine", "READY");
      var doc_id = status.parent().attr("data-id");
      showActions([doc_id]);
      
      progress([doc_id]);
    });
    
    $(".document-actions #cancel").live('click', function (ev) {
      var status = $(this).parent().parent().children().filter(".document-status");
      var actionSt = status.attr("data-actions-state-machine");
      if (actionSt == "PROCESSING")
        status.attr("data-actions-state-machine", "CANCEL-PROCESSING");
      else // actionSt == "FAILED"
        status.attr("data-actions-state-machine", "CANCEL-FAILED");
      var doc_id = status.parent().attr("data-id");
      showActions([doc_id]);
      
      var div_content = status.children().first();
      div_content.text("remove?");
      div_content.removeClass();
      div_content.addClass("label");
      div_content.addClass("label-warning");
    });
    
    
    var titles = $(".document-title span");
    var actions = $.merge($(".document-actions a"), $(".document-actions a#privacy i"));
    var infos = $(".document-info");
    var positions = $(".document-line-position");
    var tooltipElements = $.merge(titles, $.merge(actions, $.merge(infos, positions)))
    hookTooltips(tooltipElements);
    
    function hookTooltips(elems) {
        elems.hover(
          function(){
            $(this).tooltip("show");
          },
          function(){
            $(this).tooltip("hide");
          })
    }

})
