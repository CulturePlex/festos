docviewer.DocumentViewer = function(options) {
  this.options        = options;
  this.window         = window;
  this.$              = this.jQuery;
  this.schema         = new docviewer.Schema();
  this.api            = new docviewer.Api(this);
  this.history        = new docviewer.History(this);

  // Build the data models
  this.models     = this.schema.models;
  this.events     = _.extend({}, docviewer.Schema.events);
  this.helpers    = _.extend({}, docviewer.Schema.helpers);
  this.states     = _.extend({}, docviewer.Schema.states);

  // state values
  this.isFocus            = true;
  this.openEditor         = null;
  this.confirmStateChange = null;
  this.activeElement      = null;
  this.observers          = [];
  this.windowDimensions   = {};
  this.scrollPosition     = null;
  this.checkTimer         = {};
  this.busy               = false;
  this.annotationToLoadId = null;
  this.dragReporter       = null;
  this.compiled           = {};
  this.tracker            = {};

  this.onStateChangeCallbacks = [];

  this.events     = _.extend(this.events, {
    viewer      : this,
    states      : this.states,
    elements    : this.elements,
    helpers     : this.helpers,
    models      : this.models,
    // this allows us to bind events to call the method corresponding to the current state
    compile     : function(){
      var a           = this.viewer;
      var methodName  = arguments[0];
      return function(){
        if(!a.events[a.state][methodName]){
          a.events[methodName].apply(a.events,arguments);
        }else{
          a.events[a.state][methodName].apply(a.events,arguments);
        }
      };
    }
  });

  this.helpers  = _.extend(this.helpers, {
    viewer      : this,
    states      : this.states,
    elements    : this.elements,
    events      : this.events,
    models      : this.models
  });

  this.states   = _.extend(this.states, {
    viewer      : this,
    helpers     : this.helpers,
    elements    : this.elements,
    events      : this.events,
    models      : this.models
  });
};

docviewer.DocumentViewer.prototype.loadModels = function() {
  this.models.chapters     = new docviewer.model.Chapters(this);
  this.models.document     = new docviewer.model.Document(this);
  this.models.pages        = new docviewer.model.Pages(this);
  this.models.annotations  = new docviewer.model.Annotations(this);
  this.models.removedPages = {};
};

// Transition to a given state ... unless we're already in it.
docviewer.DocumentViewer.prototype.open = function(state) {
  if (this.state == state) return;
  var continuation = _.bind(function() {
    this.state = state;
    this.states[state].apply(this, arguments);
    this.slapIE();
    this.notifyChangedState();
    return true;
  }, this);
  this.confirmStateChange ? this.confirmStateChange(continuation) : continuation();
};

docviewer.DocumentViewer.prototype.slapIE = function() {
  docviewer.jQuery(this.options.container).css({zoom: 0.99}).css({zoom: 1});
};

docviewer.DocumentViewer.prototype.notifyChangedState = function() {
  _.each(this.onStateChangeCallbacks, function(c) { c(); });
};

// Record a hit on this document viewer.
docviewer.DocumentViewer.prototype.recordHit = function(hitUrl) {
  var loc = window.location;
  var url = loc.protocol + '//' + loc.host + loc.pathname;
  if (url.match(/^file:/)) return false;
  url = url.replace(/[\/]+$/, '');
  var id   = parseInt(this.api.getId(), 10);
  var key  = encodeURIComponent('document:' + id + ':' + url);
  docviewer.jQuery(document.body).append('<img alt="" width="1" height="1" src="' + hitUrl + '?key=' + key + '" />');
};

// jQuery object, scoped to this viewer's container.
docviewer.DocumentViewer.prototype.jQuery = function(selector, context) {
  context = context || this.options.container;
  return docviewer.jQuery.call(docviewer.jQuery, selector, context);
};

// The origin function, kicking off the entire documentViewer render.
docviewer.load = function(documentRep, options) {
  options = options || {};
  var id  = documentRep.id || documentRep.match(/([^\/]+)(\.js|\.json)$/)[1];
  if ('showSidebar' in options) options.sidebar = options.showSidebar;
  var defaults = {
    container : document.body,
    zoom      : 'auto',
    sidebar   : true
  };
  options            = _.extend({}, defaults, options);
  options.fixedSize  = !!(options.width || options.height);
  var viewer         = new docviewer.DocumentViewer(options);
  docviewer.viewers[id]     = viewer;
  // Once we have the JSON representation in-hand, finish loading the viewer.
  var continueLoad = docviewer.loadJSON = function(json) {
    var viewer = docviewer.viewers[json.id];
    viewer.schema.importCanonicalDocument(json);
    viewer.loadModels();
    docviewer.jQuery(function() {
      viewer.open('InitialLoad');
      if (options.afterLoad) options.afterLoad(viewer);
      if (docviewer.afterLoad) docviewer.afterLoad(viewer);
      if (docviewer.recordHit) viewer.recordHit(docviewer.recordHit);
    });
  };

  // If we've been passed the JSON directly, we can go ahead,
  // otherwise make a JSONP request to fetch it.
  var jsonLoad = function() {
    if (_.isString(documentRep)) {
      if (documentRep.match(/\.js$/)) {
        docviewer.jQuery.getScript(documentRep);
      } else {
        var crossDomain = viewer.helpers.isCrossDomain(documentRep);
        if (crossDomain) documentRep = documentRep + '?callback=?';
        docviewer.jQuery.getJSON(documentRep, continueLoad);
      }
    } else {
      continueLoad(documentRep);
    }
  };

  // If we're being asked the fetch the templates, load them remotely before
  // continuing.
  if (options.templates) {
    docviewer.jQuery.getScript(options.templates, jsonLoad);
  } else {
    jsonLoad();
  }

  return viewer;
};

// If the document viewer has been loaded dynamically, allow the external
// script to specify the onLoad behavior.
if (docviewer.onload) _.defer(docviewer.onload);

