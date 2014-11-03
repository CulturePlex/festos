$(document).ready(function() {
    var items = $("tr.document-row")
    var perPage = 2
    items.slice(perPage).addClass("hidden-by-pagination")
    $(function() {
        $("#pagination").pagination({
            items: items.length,
            itemsOnPage: perPage,
            cssStyle: 'light-theme',
            onPageClick: function(pageNumber) {
                items.removeClass("hidden-by-pagination")
                var showFrom = perPage * (pageNumber - 1)
                var showTo = showFrom + perPage
                items.addClass("hidden-by-pagination").slice(showFrom, showTo).removeClass("hidden-by-pagination")
            },
            displayedPages: 3,
            edges: 1,
            prevText: "<",
            nextText: ">"
        });
    });
    
    $("#document-list-all").live("click", function(ev) {
        $(this).addClass("hide")
        $("#document-list-latest").removeClass("hide")
        
        var items = $("tr.document-row")
        items.removeClass("hidden-by-pagination")
        $("div#pagination").hide()
    })
    $("#document-list-latest").live("click", function(ev) {
        $(this).addClass("hide")
        $("#document-list-all").removeClass("hide")
        
        var items = $("tr.document-row")
        items = items.not(".hidden-by-filter-doc").not(".hidden-by-filter-collab").not(".hidden-by-filter-tag")
        var perPage = 2
        items.slice(perPage).addClass("hidden-by-pagination")
        $(function() {
            $("#pagination").pagination({
                items: items.length,
                itemsOnPage: perPage,
                cssStyle: 'light-theme',
                onPageClick: function(pageNumber) {
                    items.removeClass("hidden-by-pagination")
                    var showFrom = perPage * (pageNumber - 1)
                    var showTo = showFrom + perPage
                    items.addClass("hidden-by-pagination").slice(showFrom, showTo).removeClass("hidden-by-pagination")
                },
                displayedPages: 3,
                edges: 1,
                prevText: "<",
                nextText: ">"
            });
        });
        $("div#pagination").show()
    })
})




