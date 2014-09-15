$(document).ready(function(){

    pickers = $( ".picker" )
    if ( pickers.length){
        $( ".picker" ).autocomplete({
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
          //$('.picker').data('url'),
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
    
    
    pickers2 = $( ".picker2" )
    if ( pickers2.length){
        $( ".picker2" ).autocomplete({
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
          //$('.picker').data('url'),
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
    var filter = [];
    pickers3 = $( ".picker3" )
    if ( pickers3.length){
        $( ".picker3" ).autocomplete({
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
          //$('.picker').data('url'),
          minLength: 1,
          select: function (ev, ui){
            var tag = ui.item.value
            if (filter.indexOf(tag) == -1) {
                filter.push(tag)
                $("#filter_tags").append("<a class=\"nolink\" ><span class=\"filter_tag\" data-id=\""+ tag +"\" style=\"margin-left:6px;\">" + tag + "</span></a>")
            }
            filter_docs(tag);
          }
      });
  }
  
    var pickers12 = $("tr.document-row .ui-autocomplete-input")
    if (pickers12.length) {
        pickers12.autocomplete({
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
    
  
    var filter_docs = function(tag) {
        var tr_docs = $("tr.document-row:visible")
        tr_docs.each(function(index) {
            tags = get_tags($(this))
            if (tags.indexOf(tag) == -1)
                $(this).hide()
        })
    }
  
    var unfilter_docs = function(tag) {
        var tr_docs = $("tr.document-row:hidden")
        if (filter.length == 0) {
            tr_docs.show()
        }
        else {
            tr_docs.each(function(index) {
                tags = get_tags($(this))
                if (allIn(filter, tags))
                    $(this).show()
            })
        }
    }
    
    var get_tags = function(tr) {
        var tags = []
        var span_tags = tr.find("span.taggit_tag")
        span_tags.each(function(index) {
            tags.push($(this).text())
        })
        return tags
    }
    
    var allIn = function(l1, l2) {
        return l1.every(function(val) { return l2.indexOf(val) >= 0; })
    }
    
  
    $("#filter_tags a.nolink").live("click", function (ev) {
        var tag = ev.target.textContent
        var index = filter.indexOf(tag)
        filter.splice(index, 1)
        index += 1
        var children = $(ev.target).parent().parent().children()
        var child = children.filter(":nth-child("+ index +")")
        child.remove()
        
        unfilter_docs(tag);
    });
    
  
    $("#sharers a.nolink").live("click", function (ev) {
        ev.preventDefault()
        var document_id = $(ev.target).parents("tr").data("id")
        var user = ev.target.textContent.slice(1)
        var adata = {}
        adata["doc_id"] = document_id
        adata["username"] = user
        $.ajax({
          url: "remove_sharer/",
          data: adata,
          dataType: 'json',
          type: 'POST',
          success: function(payload){
            var user = ev.target.textContent
            var user_list = []
            var collaborators = $(ev.target).parents('#sharers')
            collaborators.find(".sharer").each(function(index, data) {
                user_list.push(data.textContent)
            })
            var index = user_list.indexOf(user) + 1
            var collaborator = collaborators.children().filter(":nth-child("+ index +")")
            collaborator.remove()
          }})
    });
    
  
    $("#taggit_tags a.nolink").live("click", function (ev) {
        ev.preventDefault()
        var document_id = $(ev.target).parents("tr").data("id")
        var tag = ev.target.textContent
        var adata = {}
        adata["doc_id"] = document_id
        adata["tag"] = tag
        $.ajax({
          url: "remove_taggit_tag/",
          data: adata,
          dataType: 'json',
          type: 'POST',
          success: function(payload){
            var tag = ev.target.textContent
            var tag_list = []
            var tags = $(ev.target).parents('#taggit_tags')
            tags.find(".taggit_tag").each(function(index, data) {
                tag_list.push(data.textContent)
            })
            var index = tag_list.indexOf(tag) + 1
            var tag2 = tags.children().filter(":nth-child("+ index +")")
            tag2.remove()
          }})
    });

})
