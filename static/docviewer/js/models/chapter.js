docviewer.model.Chapters = function(viewer) {
  this.viewer = viewer;
  this.loadChapters();
};

docviewer.model.Chapters.prototype = {

  // Load (or reload) the chapter model from the schema's defined sections.
  loadChapters : function() {
    var sections = this.viewer.schema.data.sections;
    var chapters = this.chapters = this.viewer.schema.data.chapters = [];
    _.each(sections, function(sec){ sec.id || (sec.id = _.uniqueId()); });

    var sectionIndex = 0;
    for (var i = 0, l = this.viewer.schema.data.totalPages; i < l; i++) {
      var section = sections[sectionIndex];
      var nextSection = sections[sectionIndex + 1];
      if (nextSection && (i >= (nextSection.page - 1))) {
        sectionIndex += 1;
        section = nextSection;
      }
      if (section && !(section.page > i + 1)) chapters[i] = section.id;
    }
  },

  getChapterId: function(index){
    return this.chapters[index];
  },

  getChapterPosition: function(chapterId){
    for(var i = 0,len=this.chapters.length; i < len; i++){
      if(this.chapters[i] === chapterId){
        return i;
      }
    }
  }
};
