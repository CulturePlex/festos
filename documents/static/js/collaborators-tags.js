$(document).ready(function(){

    pickers_collabs = $( ".picker_collabs" )
    if ( pickers_collabs.length){
        pickers_collabs.autocomplete({
          source: function(request, response) {
                adata = { }
                adata['term'] = $(this).attr('element').val()
                $.ajax({
                 type: "POST",
                 dataType: 'json',
                 url: $(this).attr('element').data('url'),
                 async: false,
                 data: adata,
                 success: function(data) {
                      response(data)
                   },
               });
             },
          //$('.picker_collabs').data('url'),
          minLength: 1,
          select: function (ev, ui){
            adata = { }
            adata['doc_id'] = $(ev.target).parents(".document-row").data('id')
            adata['username'] = ui.item.value
            $.ajax({
              url: "add_sharer/",
              data: adata,
              dataType: 'json',
              type: 'GET',
              success: function(payload) {
                var user = adata['username']
                $(ev.target).prev().append("<a class=\"nolink\" href=\"#\"><span class=\"sharer\" data-id=\""+ user +"\">@" + user + "</span></a>")
              }})
          }
        });
    }
    
    
    pickers_tags = $( ".picker_tags" )
    if ( pickers_tags.length){
        pickers_tags.autocomplete({
          source: function(request, response) {
                adata = { }
                adata['term'] = $(this).attr('element').val()
                $.ajax({
                 type: "POST",
                 dataType: 'json',
                 url: $(this).attr('element').data('url'),
                 async: false,
                 data: adata,
                 success: function(data) {
                      response(data)
                   },
               });
             },
          //$('.picker_tags').data('url'),
          minLength: 1,
          select: function (ev, ui){
            adata = { }
            adata['doc_id'] = $(ev.target).parents(".document-row").data('id')
            adata['tag'] = ui.item.value
            $.ajax({
              url: "add_taggit_tag/",
              data: adata,
              dataType: 'json',
              type: 'POST',
              success: function(payload){
                //location.reload();
                if (payload.added) {
                    var tag = adata['tag']
                    $(ev.target).prev().append("<a class=\"nolink\" href=\"#\"><span class=\"taggit_tag\" data-id=\""+ tag +"\">" + tag + "</span></a>")
                }
              }})
          }
      });
      
      $("input#id_taggit_tags").bind("enterKey",function(ev){
        if ($(this).val() != "") {
            adata = { }
            adata['doc_id'] = $(ev.target).parents(".document-row").data('id')
            adata['tag'] = $(this).val()
            $.ajax({
              url: "add_taggit_tag/",
              data: adata,
              dataType: 'json',
              type: 'POST',
              success: function(payload){
                //location.reload();
                if (payload.added) {
                    var tag = adata['tag']
                    $(ev.target).prev().append("<a class=\"nolink\" href=\"#\"><span class=\"taggit_tag\" data-id=\""+ tag +"\">" + tag + "</span></a>")
                }
              }})
        }
      });
      
      $("input#id_taggit_tags").keypress(function(e){
          if(e.keyCode == 13)
          {
              $(this).trigger("enterKey");
          }
      });
  }
  
    var pickers_collabs_tags = $("tr.document-row .ui-autocomplete-input")
    if (pickers_collabs_tags.length) {
        pickers_collabs_tags.autocomplete({
            open: function(ev, ui) {
                var thesePickers = $(ev.target).parents('tr.document-row').find('.ui-autocomplete-input')
                thesePickers.addClass("ui-autocomplete-input-shown")
                thesePickers.removeClass("ui-autocomplete-input-hidden")
            },
            close: function(ev, ui) {
                var thesePickers = $(ev.target).parents('tr.document-row').find('.ui-autocomplete-input')
                thesePickers.addClass("ui-autocomplete-input-hidden")
                thesePickers.removeClass("ui-autocomplete-input-shown")
            }
        })
    }
  
  
    var tag_filter = [];
    var collab_filter = [];
    var doc_filter = [];
    
    pickers_filter_docs = $( ".picker_filter_docs" )
    if ( pickers_filter_docs.length){
        pickers_filter_docs.autocomplete({
          source: function(request, response) {
                adata = { }
                adata['term'] = $(this).attr('element').val()
                $.ajax({
                 type: "POST",
                 dataType: 'json',
                 url: $(this).attr('element').data('url'),
                 async: false,
                 data: adata,
                 success: function(data) {
                      response(data)
                   },
               });
             },
          //$('.picker_filter_docs').data('url'),
          minLength: 1,
          select: function (ev, ui){
            var doc = ui.item.value
            if (doc_filter.indexOf(doc) == -1) {
                doc_filter.push(doc)
                $("#filter_docs").append("<a class=\"nolink\" ><span class=\"filter_doc\" data-id=\""+ doc +"\" style=\"margin-left:6px;\">" + doc + "</span></a>")
            }
            filter_docs_by_doc(doc);
          }
      });
  }
    
    pickers_filter_collabs = $( ".picker_filter_collabs" )
    if ( pickers_filter_collabs.length){
        pickers_filter_collabs.autocomplete({
          source: function(request, response) {
                adata = { }
                adata['term'] = $(this).attr('element').val()
                $.ajax({
                 type: "POST",
                 dataType: 'json',
                 url: $(this).attr('element').data('url'),
                 async: false,
                 data: adata,
                 success: function(data) {
                      response(data)
                   },
               });
             },
          //$('.picker_filter_collabs').data('url'),
          minLength: 1,
          select: function (ev, ui){
            var collab = ui.item.value
            if (collab_filter.indexOf(collab) == -1) {
                collab_filter.push("@"+collab)
                $("#filter_collabs").append("<a class=\"nolink\" ><span class=\"filter_collab\" data-id=\""+ collab +"\" style=\"margin-left:6px;\">@" + collab + "</span></a>")
            }
            filter_docs_by_collab(collab);
          }
      });
  }
    
    pickers_filter_tags = $( ".picker_filter_tags" )
    if ( pickers_filter_tags.length){
        pickers_filter_tags.autocomplete({
          source: function(request, response) {
                adata = { }
                adata['term'] = $(this).attr('element').val()
                $.ajax({
                 type: "POST",
                 dataType: 'json',
                 url: $(this).attr('element').data('url'),
                 async: false,
                 data: adata,
                 success: function(data) {
                      response(data)
                   },
               });
             },
          //$('.picker_filter_tags').data('url'),
          minLength: 1,
          select: function (ev, ui){
            var tag = ui.item.value
            if (tag_filter.indexOf(tag) == -1) {
                tag_filter.push(tag)
                $("#filter_tags").append("<a class=\"nolink\" ><span class=\"filter_tag\" data-id=\""+ tag +"\" style=\"margin-left:6px;\">" + tag + "</span></a>")
            }
            filter_docs_by_tag(tag);
          }
      });
  }
  
  $("a.nolink span.sharer").live("click", function(ev) {
//    ev.preventDefault()
//    ev.stopPropagation()
    var collab = ev.target.textContent.slice(1)
    if (collab_filter.indexOf(collab) == -1) {
        collab_filter.push("@"+collab)
        $("#filter_collabs").append("<a class=\"nolink\" ><span class=\"filter_collab\" data-id=\""+ collab +"\" style=\"margin-left:6px;\">@" + collab + "</span></a>")
    }
    filter_docs_by_collab(collab);
    return false
  })
  
  $("a.nolink span.taggit_tag").live("click", function(ev) {
//    ev.preventDefault()
//    ev.stopPropagation()
    var tag = ev.target.textContent
    if (tag_filter.indexOf(tag) == -1) {
        tag_filter.push(tag)
        $("#filter_tags").append("<a class=\"nolink\" ><span class=\"filter_tag\" data-id=\""+ tag +"\" style=\"margin-left:6px;\">" + tag + "</span></a>")
    }
    filter_docs_by_tag(tag);
    return false
  })
  
    var filter_docs_by_doc = function(doc) {
        var tr_docs = $("tr.document-row:visible")
        tr_docs.each(function(index) {
            docs = get_docs($(this))
            if (docs.indexOf(doc) == -1)
                $(this).hide()
        })
    }
  
    var filter_docs_by_collab = function(collab) {
        var tr_docs = $("tr.document-row:visible")
        tr_docs.each(function(index) {
            collabs = get_collabs($(this))
            if (collabs.indexOf("@"+collab) == -1)
                $(this).hide()
        })
    }
  
    var filter_docs_by_tag = function(tag) {
        var tr_docs = $("tr.document-row:visible")
        tr_docs.each(function(index) {
            tags = get_tags($(this))
            if (tags.indexOf(tag) == -1)
                $(this).hide()
        })
    }
  
    var unfilter_docs = function() {
        var tr_docs = $("tr.document-row:hidden")
        if (doc_filter.length == 0 && collab_filter.length == 0 && tag_filter.length == 0) {
            tr_docs.show()
        }
        else {
            tr_docs.each(function(index) {
                docs = get_docs($(this))
                collabs = get_collabs($(this))
                tags = get_tags($(this))
                if (allIn(doc_filter, docs) && allIn(collab_filter, collabs) && allIn(tag_filter, tags))
                    $(this).show()
            })
        }
    }
    
    var allIn = function(l1, l2) {
        return l1.length == 0 && l2.length == 0 || l1.every(function(val) { return l2.indexOf(val) >= 0; })
    }
    
    var get_docs = function(tr) {
        var docs = []
        var span_docs = tr.find("span.document")
        span_docs.each(function(index) {
            docs.push($(this).text())
        })
        return docs
    }
    
    var get_collabs = function(tr) {
        var collabs = []
        var span_collabs = tr.find("span.sharer")
        span_collabs.each(function(index) {
            collabs.push($(this).text())
        })
        return collabs
    }
    
    var get_tags = function(tr) {
        var tags = []
        var span_tags = tr.find("span.taggit_tag")
        span_tags.each(function(index) {
            tags.push($(this).text())
        })
        return tags
    }
    
  
    $("#filter_docs a.nolink").live("click", function (ev) {
        var doc = ev.target.textContent
        var index = doc_filter.indexOf(doc)
        doc_filter.splice(index, 1)
        index += 1
        var children = $(ev.target).parent().parent().children()
        var child = children.filter(":nth-child("+ index +")")
        child.remove()
        
        unfilter_docs();
    });
  
    $("#filter_collabs a.nolink").live("click", function (ev) {
        var collab = ev.target.textContent
        var index = collab_filter.indexOf(collab)
        collab_filter.splice(index, 1)
        index += 1
        var children = $(ev.target).parent().parent().children()
        var child = children.filter(":nth-child("+ index +")")
        child.remove()
        
        unfilter_docs();
    });
  
    $("#filter_tags a.nolink").live("click", function (ev) {
        var tag = ev.target.textContent
        var index = tag_filter.indexOf(tag)
        tag_filter.splice(index, 1)
        index += 1
        var children = $(ev.target).parent().parent().children()
        var child = children.filter(":nth-child("+ index +")")
        child.remove()
        
        unfilter_docs();
    });
    
  
    $("#sharers a.nolink").live("click", function (ev) {
        ev.preventDefault()
        var document_id = $(ev.target).parents("tr").data("id")
        var user1 = ev.target.children[0].textContent.slice(1)
        var adata = {}
        adata["doc_id"] = document_id
        adata["username"] = user1
        $.ajax({
          url: "remove_sharer/",
          data: adata,
          dataType: 'json',
          type: 'POST',
          success: function(payload){
            var user2 = "@"+user1
            var user_list = []
            var collaborators = $(ev.target).parents('#sharers')
            collaborators.find(".sharer").each(function(index, data) {
                user_list.push(data.textContent)
            })
            var index = user_list.indexOf(user2) + 1
            var user3 = collaborators.children().filter(":nth-child("+ index +")")
            user3.remove()
          }})
    });
    
  
    $("#taggit_tags a.nolink").live("click", function (ev) {
        ev.preventDefault()
        var document_id = $(ev.target).parents("tr").data("id")
        var tag1 = ev.target.children[0].textContent
        var adata = {}
        adata["doc_id"] = document_id
        adata["tag"] = tag1
        $.ajax({
          url: "remove_taggit_tag/",
          data: adata,
          dataType: 'json',
          type: 'POST',
          success: function(payload){
            var tag2 = tag1
            var tag_list = []
            var tags = $(ev.target).parents('#taggit_tags')
            tags.find(".taggit_tag").each(function(index, data) {
                tag_list.push(data.textContent)
            })
            var index = tag_list.indexOf(tag2) + 1
            var tag3 = tags.children().filter(":nth-child("+ index +")")
            tag3.remove()
          }})
    });

})
