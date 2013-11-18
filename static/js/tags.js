(function($) {
    $(document).ready(function($) {
        // General variables
        var prefix = $("#zotero-formset-prefix").val();
        var fields_url = $("#zotero-itemtype-url").val();
        
        
        // Selectors
        var container = "div." + prefix;
        var header = container + " tr.zotero-header";
        var errorList = container + " .errorlist";
        var rowAll = container + " tr:not(:hidden).zotero-tag";
        var rowLast = rowAll + ":last";
        var itemTypeAll = rowAll + " td.field-item_type select";
        var itemTypeFirst = itemTypeAll + ":first";
        var fieldAll = container + " td.field-field select";
        var fieldLast = fieldAll + ":last";
        var idAll = container + " td.field-id";
        
        // Choose applicable fields
        var changeFields = function() {
            var itemTypeValueFirst = $(itemTypeFirst).val();
            if(itemTypeValueFirst == "" || itemTypeValueFirst == undefined)
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
            })
        }
        
        // Set item_type's values
        var setItemTypesValues = function() {
            $(itemTypeAll).val($(itemTypeFirst).val());
        }
        
        // Hide other item_type selectors and id fields
        var hideItemTypeAndId = function() {
            $(itemTypeAll).hide();
            $(itemTypeFirst).show();
            $(idAll).hide();
        }
        
        $(itemTypeAll).change(function(){
            setItemTypesValues();
            changeFields();
        });
        
        
        // Inlines
        var formset = function() {
            var alternatingRows = function(row) {
                $(rows).not(".add-row").not(":hidden").removeClass("row1 row2")
                    .filter(":even").addClass("row1").end()
                    .filter(":odd").addClass("row2");
            }
            
            rows = container + " tbody tr";
            $(rows).formset({
                prefix: prefix,                    // The form prefix for your django formset
                formTemplate: null,                // The jQuery selection cloned to generate new form instances
                addText: "Add a tag",              // Text for the add link
                deleteText: "remove",              // Text for the delete link
                addCssClass: "add-row",            // CSS class applied to the add link
                deleteCssClass: "delete-row",      // CSS class applied to the delete link
                formCssClass: "tag-form",          // CSS class applied to each form in a formset
                extraClasses: [],                  // Additional CSS classes, which will be applied to each form in turn
                emptyCssClass: "empty-form",
                removed: (function(row) {
                    performActions();
                    alternatingRows(row);
                    hideHeader();
                }),                                // Function called each time a form is deleted
                added: (function(row) {
                    checkFirstRow();
                    performActions();
                    alternatingRows(row);
                    resetLastField();
                }),                                // Function called each time a new form is added
            });
        }
        formset();
        
        // Reset last field
        var resetLastField = function() {
            $(fieldLast).val("");
            $(rowLast + " .errorlist").hide();
        }
        
        // Hide header if no rows
        var hideHeader = function() {
            if($(rowAll).length == 0)
                $(header).hide();
                $(errorList).hide();
        }
        
        // Empty first row
        var checkFirstRow = function() {
            if($(rowAll).length == 1) {
                $(header).show();
                $(errorList).hide();
                $(itemTypeFirst).val("");
                $(fieldLast).val("");
            }
        }
        
        
        
        
        
        
        // All actions
        var performActions = function() {
            hideItemTypeAndId();
            setItemTypesValues();
            changeFields();
        }
        performActions();
    });
})(jQuery);
