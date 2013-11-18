docviewer.model.Editions = function(viewer) {
  this.viewer                   = viewer;
  this.saveCallbacks            = [];
  this.deleteCallbacks          = [];
  this.byId                     = this.viewer.schema.data.editionsById;
  this.byPage                   = this.viewer.schema.data.editionsByPage;
  this.bySortOrder              = this.sortEditions();
};

docviewer.model.Editions.prototype = {

  // Render an edition model to HTML
  render: function(edition){
    var documentModel             = this.viewer.models.document;
    var pageModel                 = this.viewer.models.pages;
    var edata                     = edition;


    edata.author         = edata.author || "";
    edata.modified_pages = edata.modified_pages || [];
    edata.date           = edata.date || '';
    edata.author         = edata.author || 'no-author';
    edata.comment        = edata.comment || 'no-comment';


    edata.orderClass = '';
    edata.options = this.viewer.options;
    if (edata.position == 1) edata.orderClass += ' docviewer-firstEdition';
    if (edata.position == this.bySortOrder.length) edata.orderClass += ' docviewer-lastEdition';

    var template = 'edition';
    return JST[template](edata);
  },

  // Re-sort the list of annotations when its contents change. Annotations
  // are ordered by page primarily, and then their y position on the page.
  sortEditions : function() {
    return this.bySortOrder = _.sortBy(_.values(this.byId), function(edit) {
      return 0; //edit."date";
    });
  },

  // When an edition is successfully saved, fire any registered
  // save callbacks.
  fireSaveCallbacks : function(edit) {
    _.each(this.saveCallbacks, function(c){ c(edit); });
  },

  // When an edition is successfully removed, fire any registered
  // delete callbacks.
  fireDeleteCallbacks : function(edit) {
    _.each(this.deleteCallbacks, function(c){ c(edit); });
  },


  getFirstEdition: function(){
    return _.first(this.bySortOrder);
  },

  getNextEdition: function(currentId) {
    var edit = this.byId[currentId];
    return this.bySortOrder[_.indexOf(this.bySortOrder, edit) + 1];
  },

  getPreviousEdition: function(currentId) {
    var edit = this.byId[currentId];
    return this.bySortOrder[_.indexOf(this.bySortOrder, edit) - 1];
  },

  // Get an edition by id, with backwards compatibility for argument hashes.
  getEdition: function(identifier) {
    if (identifier.id) return this.byId[identifier.id];
    if (identifier.index && !identifier.id) throw new Error('looked up an edition without an id');
    return this.byId[identifier];
  }

};
