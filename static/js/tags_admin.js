(function($) {
    $(document).ready(function($) {
        // Selectors
        var container = "#" + prefix + "-group";
        var dataRowAll = container + " tr"
        var itemTypeTdField = dataRowAll + " td.field-item_type"
        var itemTypeAll = itemTypeTdField + " select";
        var itemTypeFirst = itemTypeAll + ":first";
        var itemTypeFirstOption = itemTypeFirst + " option[selected]";
        var itemTypeAddAll = itemTypeTdField + " a";
        var itemTypeAddFirst = itemTypeAddAll + ":first";
        var itemTypeSpanClass = "zotero-itemtype-text"
        var itemTypeSpanAll = itemTypeTdField + " span." + itemTypeSpanClass
        var itemTypeSpanFirst = itemTypeSpanAll + ":first"
        var fieldAll = dataRowAll + " td.field-field select";
        var fieldLast = fieldAll + ":last";
        var addLink = dataRowAll + ".add-row a"
        
        
        // Choose applicable fields
        var changeFields = function() {
            var itemTypeValueFirst = $(itemTypeFirst).val();
            if(itemTypeValueFirst == "")
                itemTypeValueFirst = "1";
            $.getJSON(fields_url, {'itemtype': itemTypeValueFirst}, function(data) {
                // Show all fields
                var fields = fieldAll + " option";
                $(fields).show();
                // Get data
                var applicableFields = data;
                
                // Hide non applicable fields
                var numFields = $(fieldLast + " option").size() - 1
                for(var i = 1; i <= numFields; i++)
                {
                    if(applicableFields.indexOf(i) == -1)
                    {
                        var nonApplicableOptions = fields + "[value='" + i + "']";
                        $(nonApplicableOptions).hide();
                    }
                }
                
                //Listen to click events from "Add another Tag"
                $(addLink).click(performActions);
            })
        }
        
        //Add span
        var addSpan = function() {
            var span = "<span class=\"" + itemTypeSpanClass + "\"></span>"
            $(itemTypeTdField).append(span);
        }
        addSpan();
        
        //Set item_type's values
        var setItemTypesValues = function() {
            $(itemTypeAll).val($(itemTypeFirst).val());
            $(itemTypeSpanAll).text($(itemTypeFirstOption).text())
        }
        
        //Hide first span and other item_type selectors
        var hideItemType = function() {
            $(itemTypeAll).hide();
            $(itemTypeFirst).show();
            $(itemTypeSpanAll).show();
            $(itemTypeSpanFirst).hide();
            $(itemTypeAddAll).hide();
            $(itemTypeAddFirst).show();
        }
        
        //All actions
        var performActions = function() {
            hideItemType();
            setItemTypesValues();
            changeFields();
        }
        
        performActions();
        $(itemTypeFirst).change(function(){
            setItemTypesValues();
            changeFields();
        });
    });
})(django.jQuery);
