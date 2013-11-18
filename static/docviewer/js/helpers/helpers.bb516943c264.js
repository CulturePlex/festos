docviewer.Schema.helpers = {

    HOST_EXTRACTOR : (/https?:\/\/([^\/]+)\//),

    annotationClassName: '.docviewer-annotation',

    // Bind all events for the docviewer
    // live/delegate are the preferred methods of event attachment
    bindEvents: function(context){
      var boundZoom = this.events.compile('zoom');
      var doc       = context.models.document;
      var value     = _.indexOf(doc.ZOOM_RANGES, doc.zoomLevel);
      var viewer    = this.viewer;
      viewer.slider = viewer.$('.docviewer-zoomBox').slider({
        step: 1,
        min: 0,
        max: 4,
        value: value,
        slide: function(el,d){
          boundZoom(context.models.document.ZOOM_RANGES[parseInt(d.value, 10)]);
        },
        change: function(el,d){
          boundZoom(context.models.document.ZOOM_RANGES[parseInt(d.value, 10)]);
        }
      });

      // next/previous
      var history         = viewer.history;
      var compiled        = viewer.compiled;
      compiled.next       = this.events.compile('next');
      compiled.previous   = this.events.compile('previous');


      var states = context.states;
      viewer.$('.docviewer-navControls').delegate('span.docviewer-next','click', compiled.next);
      viewer.$('.docviewer-navControls').delegate('span.docviewer-previous','click', compiled.previous);

      viewer.$('.docviewer-annotationView').delegate('.docviewer-trigger','click',function(e){
        e.preventDefault();
        context.open('ViewAnnotation');
      });
      viewer.$('.docviewer-documentView').delegate('.docviewer-trigger','click',function(e){
        // history.save('document/p'+context.models.document.currentPage());
        context.open('ViewDocument');
      });
      viewer.$('.docviewer-thumbnailsView').delegate('.docviewer-trigger','click',function(e){
        context.open('ViewThumbnails');
      });
      viewer.$('.docviewer-textView').delegate('.docviewer-trigger','click',function(e){

        // history.save('text/p'+context.models.document.currentPage());
        context.open('ViewText');
      });
      viewer.$('.docviewer-allAnnotations').delegate('.docviewer-annotationGoto .docviewer-trigger','click', docviewer.jQuery.proxy(this.gotoPage, this));

      viewer.$('form.docviewer-searchDocument').submit(this.events.compile('search'));
      viewer.$('.docviewer-searchBar').delegate('.docviewer-closeSearch','click',function(e){
        e.preventDefault();
        // history.save('text/p'+context.models.document.currentPage());
        context.open('ViewText');
      });
      viewer.$('.docviewer-searchBox').delegate('.docviewer-searchInput-cancel', 'click', docviewer.jQuery.proxy(this.clearSearch, this));

      viewer.$('.docviewer-searchResults').delegate('span.docviewer-resultPrevious','click', docviewer.jQuery.proxy(this.highlightPreviousMatch, this));

      viewer.$('.docviewer-searchResults').delegate('span.docviewer-resultNext','click', docviewer.jQuery.proxy(this.highlightNextMatch, this));

      // Prevent navigation elements from being selectable when clicked.
      viewer.$('.docviewer-trigger').bind('selectstart', function(){ return false; });

      this.elements.viewer.delegate('.docviewer-fullscreen', 'click', _.bind(this.openFullScreen, this));

      var boundToggle  = docviewer.jQuery.proxy(this.annotationBridgeToggle, this);
      var collection   = this.elements.collection;

      collection.delegate('.docviewer-annotationTab','click', boundToggle);
      collection.delegate('.docviewer-annotationRegion','click', docviewer.jQuery.proxy(this.annotationBridgeShow, this));
      collection.delegate('.docviewer-annotationNext','click', docviewer.jQuery.proxy(this.annotationBridgeNext, this));
      collection.delegate('.docviewer-annotationPrevious','click', docviewer.jQuery.proxy(this.annotationBridgePrevious, this));
      collection.delegate('.docviewer-showEdit','click', docviewer.jQuery.proxy(this.showAnnotationEdit, this));
      collection.delegate('.docviewer-cancelEdit','click', docviewer.jQuery.proxy(this.cancelAnnotationEdit, this));
      collection.delegate('.docviewer-saveAnnotation','click', docviewer.jQuery.proxy(this.saveAnnotation, this));
      collection.delegate('.docviewer-saveAnnotationDraft','click', docviewer.jQuery.proxy(this.saveAnnotation, this));
      collection.delegate('.docviewer-deleteAnnotation','click', docviewer.jQuery.proxy(this.deleteAnnotation, this));
      collection.delegate('.docviewer-pageNumber', 'click', _.bind(this.permalinkPage, this, 'document'));
      collection.delegate('.docviewer-textCurrentPage', 'click', _.bind(this.permalinkPage, this, 'text'));
      collection.delegate('.docviewer-annotationTitle', 'click', _.bind(this.permalinkAnnotation, this));
//      collection.delegate('.docviewer-annotationAuthor', 'click', _.bind(this.permalinkAnnotation, this));
      collection.delegate('.docviewer-permalink', 'click', _.bind(this.permalinkAnnotation, this));

      // Thumbnails
      viewer.$('.docviewer-thumbnails').delegate('.docviewer-thumbnail-page', 'click', function(e) {
        var $thumbnail = viewer.$(e.currentTarget);
        if (!viewer.openEditor) {
          var pageIndex = $thumbnail.closest('.docviewer-thumbnail').attr('data-pageNumber') - 1;
          viewer.models.document.setPageIndex(pageIndex);
          viewer.open('ViewDocument');
          // viewer.history.save('document/p'+pageNumber);
        }
      });

      // Handle iPad / iPhone scroll events...
      _.bindAll(this, 'touchStart', 'touchMove', 'touchEnd');
      this.elements.window[0].ontouchstart  = this.touchStart;
      this.elements.window[0].ontouchmove   = this.touchMove;
      this.elements.window[0].ontouchend    = this.touchEnd;
      this.elements.well[0].ontouchstart    = this.touchStart;
      this.elements.well[0].ontouchmove     = this.touchMove;
      this.elements.well[0].ontouchend      = this.touchEnd;

      viewer.$('.docviewer-descriptionToggle').live('click',function(e){
        e.preventDefault();
        e.stopPropagation();

        viewer.$('.docviewer-descriptionText').toggle();
        viewer.$('.docviewer-descriptionToggle').toggleClass('docviewer-showDescription');
      });

      var cleanUp = docviewer.jQuery.proxy(viewer.pageSet.cleanUp, this);

      this.elements.window.live('mousedown',
        function(e){
          var el = viewer.$(e.target);
          if (el.parents().is('.docviewer-annotation') || el.is('.docviewer-annotation')) return true;
          if(context.elements.window.hasClass('docviewer-coverVisible')){
            if((el.width() - parseInt(e.clientX,10)) >= 15){
              cleanUp();
            }
          }
        }
      );

      var docId = viewer.schema.document.id;

      if(docviewer.jQuery.browser.msie == true){
        this.elements.browserDocument.bind('focus.' + docId, docviewer.jQuery.proxy(this.focusWindow,this));
        this.elements.browserDocument.bind('focusout.' + docId, docviewer.jQuery.proxy(this.focusOut,this));
      }else{
        this.elements.browserWindow.bind('focus.' + docId, docviewer.jQuery.proxy(this.focusWindow,this));
        this.elements.browserWindow.bind('blur.' + docId, docviewer.jQuery.proxy(this.blurWindow,this));
      }

      // When the document is scrolled, even in the background, resume polling.
      this.elements.window.bind('scroll.' + docId, docviewer.jQuery.proxy(this.focusWindow, this));

      this.elements.coverPages.live('mousedown', cleanUp);

      viewer.acceptInput = this.elements.currentPage.acceptInput({ changeCallBack: docviewer.jQuery.proxy(this.acceptInputCallBack,this) });

    },

    // Unbind jQuery events that have been bound to objects outside of the viewer.
    unbindEvents: function() {
      var viewer = this.viewer;
      var docId = viewer.schema.document.id;
      if(docviewer.jQuery.browser.msie == true){
        this.elements.browserDocument.unbind('focus.' + docId);
        this.elements.browserDocument.unbind('focusout.' + docId);
      }else{
        viewer.helpers.elements.browserWindow.unbind('focus.' + docId);
        viewer.helpers.elements.browserWindow.unbind('blur.' + docId);
      }
      viewer.helpers.elements.browserWindow.unbind('scroll.' + docId);
      _.each(viewer.observers, function(obs){ viewer.helpers.removeObserver(obs); });
    },

    // We're entering the Notes tab -- make sure that there are no data-src
    // attributes remaining.
    ensureAnnotationImages : function() {
      this.viewer.$(".docviewer-img[data-src]").each(function() {
        var el = docviewer.jQuery(this);
        el.attr('src', el.attr('data-src'));
      });
    },

    startCheckTimer: function(){
      var _t = this.viewer;
      var _check = function(){
        _t.events.check();
      };
      this.viewer.checkTimer = setInterval(_check,100);
    },

    stopCheckTimer: function(){
      clearInterval(this.viewer.checkTimer);
    },

    blurWindow: function(){
      if(this.viewer.isFocus === true){
        this.viewer.isFocus = false;
        // pause draw timer
        this.stopCheckTimer();
      }else{
        return;
      }
    },

    focusOut: function(){
      if(this.viewer.activeElement != document.activeElement){
        this.viewer.activeElement = document.activeElement;
        this.viewer.isFocus = true;
      }else{
        // pause draw timer
        this.viewer.isFocus = false;
        this.viewer.helpers.stopCheckTimer();
        return;
      }
    },

    focusWindow: function(){
      if(this.viewer.isFocus === true){
        return;
      }else{
        this.viewer.isFocus = true;
        // restart draw timer
        this.startCheckTimer();
      }
    },

    touchStart : function(e) {
      e.stopPropagation();
      e.preventDefault();
      var touch = e.changedTouches[0];
      this._moved  = false;
      this._touchX = touch.pageX;
      this._touchY = touch.pageY;
    },

    touchMove : function(e) {
      var el    = e.currentTarget;
      var touch = e.changedTouches[0];
      var xDiff = this._touchX - touch.pageX;
      var yDiff = this._touchY - touch.pageY;
      el.scrollLeft += xDiff;
      el.scrollTop  += yDiff;
      this._touchX  -= xDiff;
      this._touchY  -= yDiff;
      if (yDiff != 0 || xDiff != 0) this._moved = true;
    },

    touchEnd : function(e) {
      if (!this._moved) {
        var touch     = e.changedTouches[0];
        var target    = touch.target;
        var fakeClick = document.createEvent('MouseEvent');
        while (target.nodeType !== 1) target = target.parentNode;
        fakeClick.initMouseEvent('click', true, true, touch.view, 1,
          touch.screenX, touch.screenY, touch.clientX, touch.clientY,
          false, false, false, false, 0, null);
        target.dispatchEvent(fakeClick);
      }
      this._moved = false;
    },

    // Click to open a page's permalink.
    permalinkPage : function(mode, e) {
      if (mode == 'text') {
        var number  = this.viewer.models.document.currentPage();
      } else {
        var pageId  = this.viewer.$(e.target).closest('.docviewer-set').attr('data-id');
        var page    = this.viewer.pageSet.pages[pageId];
        var number  = page.pageNumber;
        this.jump(page.index);
      }
      this.viewer.history.save(mode + '/p' + number);
    },

    // Click to open an annotation's permalink.
    permalinkAnnotation : function(e) {
      var id   = this.viewer.$(e.target).closest('.docviewer-annotation').attr('data-id');
      var anno = this.viewer.models.annotations.getAnnotation(id);
      var sid  = anno.server_id || anno.id;
      if (this.viewer.state == 'ViewDocument') {
        this.viewer.pageSet.showAnnotation(anno);
        this.viewer.history.save('document/p' + anno.pageNumber + '/a' + sid);
      } else {
        this.viewer.history.save('annotation/a' + sid);
      }
    },

    setDocHeight:   function(height,diff) {
      this.elements.bar.css('height', height);
      this.elements.window[0].scrollTop += diff;
    },

    getWindowDimensions: function(){
      var d = {
        height: window.innerHeight ? window.innerHeight : this.elements.browserWindow.height(),
        width: this.elements.browserWindow.width()
      };
      return d;
    },

    // Is the given URL on a remote domain?
    isCrossDomain : function(url) {
    	var match = url.match(this.HOST_EXTRACTOR);
      return docviewer.jQuery.support.cors != true && match && (match[1] != window.location.host);
    },

    resetScrollState: function(){
      this.elements.window.scrollTop(0);
    },

    gotoPage: function(e){
      e.preventDefault();
      var aid           = this.viewer.$(e.target).parents('.docviewer-annotation').attr('rel').replace('aid-','');
      var annotation    = this.models.annotations.getAnnotation(aid);
      var viewer        = this.viewer;

      if(viewer.state !== 'ViewDocument'){
        this.models.document.setPageIndex(annotation.index);
        viewer.open('ViewDocument');
        // this.viewer.history.save('document/p'+(parseInt(annotation.index,10)+1));
      }
    },

    openFullScreen : function() {
      var doc = this.viewer.schema.document;
      var url = doc.canonicalURL.replace(/#\S+$/,"");
      var currentPage = this.models.document.currentPage();

      // construct url fragment based on current viewer state
      switch (this.viewer.state) {
        case 'ViewAnnotation':
          url += '#annotation/a' + this.viewer.activeAnnotationId; // default to the top of the annotations page.
          break;
        case 'ViewDocument':
          url += '#document/p' + currentPage;
          break;
        case 'ViewSearch':
          url += '#search/p' + currentPage + '/' + encodeURIComponent(this.elements.searchInput.val());
          break;
        case 'ViewText':
          url += '#text/p' + currentPage;
          break;
        case 'ViewThumbnails':
          url += '#pages/p' + currentPage; // need to set up a route to catch this.
          break;
      }
      window.open(url, "documentviewer", "toolbar=no,resizable=yes,scrollbars=no,status=no");
    },

    // Determine the correct DOM page ordering for a given page index.
    sortPages : function(pageIndex) {
      if (pageIndex == 0 || pageIndex % 3 == 1) return ['p0', 'p1', 'p2'];
      if (pageIndex % 3 == 2)                   return ['p1', 'p2', 'p0'];
      if (pageIndex % 3 == 0)                   return ['p2', 'p0', 'p1'];
    },

    addObserver: function(observerName){
      this.removeObserver(observerName);
      this.viewer.observers.push(observerName);
    },

    removeObserver: function(observerName){
      var observers = this.viewer.observers;
      for(var i = 0,len=observers.length;i<len;i++){
        if(observerName === observers[i]){
          observers.splice(i,1);
        }
      }
    },

    // TODO: This function is not currently being called. Candidate for removal.

    // setWindowSize: function(windowDimensions){
    //   var viewer          = this.viewer;
    //   var elements        = this.elements;
    //   var headerHeight    = elements.header.outerHeight() + 15;
    //   var offset          = docviewer.jQuery(this.viewer.options.container).offset().top;
    //   var uiHeight        = Math.round((windowDimensions.height) - headerHeight - offset);
    //
    //   // doc window
    //   elements.window.css({ height: uiHeight, width: windowDimensions.width-267 });
    //
    //   // well
    //   elements.well.css( { height: uiHeight });
    //
    //   // store this for later
    //   viewer.windowDimensions = windowDimensions;
    // },

    toggleContent: function(toggleClassName){
      this.elements.viewer.removeClass('docviewer-viewText docviewer-viewSearch docviewer-viewDocument docviewer-viewAnnotations docviewer-viewThumbnails').addClass('docviewer-'+toggleClassName);
    },

    jump: function(pageIndex, modifier, forceRedraw){
      modifier = (modifier) ? parseInt(modifier, 10) : 0;
      var position = this.models.document.getOffset(parseInt(pageIndex, 10)) + modifier;
      this.elements.window[0].scrollTop = position;
      this.models.document.setPageIndex(pageIndex);
      if (forceRedraw) this.viewer.pageSet.redraw(true);
      if (this.viewer.state === 'ViewThumbnails') {
        this.viewer.thumbnails.highlightCurrentPage();
      }
    },

    shift: function(argHash){
      var windowEl        = this.elements.window;
      var scrollTopShift  = windowEl.scrollTop() + argHash.deltaY;
      var scrollLeftShift  = windowEl.scrollLeft() + argHash.deltaX;

      windowEl.scrollTop(scrollTopShift);
      windowEl.scrollLeft(scrollLeftShift);
    },

    getAppState: function(){
      var docModel = this.models.document;
      var currentPage = (docModel.currentIndex() == 0) ? 1 : docModel.currentPage();

      return { page: currentPage, zoom: docModel.zoomLevel, view: this.viewer.state };
    },

    constructPages: function(){
      var pages = [];
      var totalPagesToCreate = (this.viewer.schema.data.totalPages < 3) ? this.viewer.schema.data.totalPages : 3;

      var height = this.models.pages.height;
      for (var i = 0; i < totalPagesToCreate; i++) {
        pages.push(JST.pages({ pageNumber: i+1, pageIndex: i , pageImageSource: null, baseHeight: height }));
      }

      return pages.join('');
    },

    // Position the viewer on the page. For a full screen viewer, this means
    // absolute from the current y offset to the bottom of the viewport.
    positionViewer : function() {
      var offset = this.elements.viewer.position();
      this.elements.viewer.css({position: 'absolute', top: offset.top, bottom: 0, left: offset.left, right: offset.left});
    },

    unsupportedBrowser : function() {
      if (!(docviewer.jQuery.browser.msie && docviewer.jQuery.browser.version <= "6.0")) return false;
      docviewer.jQuery(this.viewer.options.container).html(JST.unsupported({viewer : this.viewer}));
      return true;
    },

    registerHashChangeEvents: function(){
      var events  = this.events;
      var history = this.viewer.history;

      // Default route
      history.defaultCallback = _.bind(events.handleHashChangeDefault,this.events);

      // Handle page loading
      history.register(/document\/p(\d*)$/, _.bind(events.handleHashChangeViewDocumentPage,this.events));
      // Legacy NYT stuff
      history.register(/p(\d*)$/, _.bind(events.handleHashChangeLegacyViewDocumentPage,this.events));
      history.register(/p=(\d*)$/, _.bind(events.handleHashChangeLegacyViewDocumentPage,this.events));

      // Handle annotation loading in document view
      history.register(/document\/p(\d*)\/a(\d*)$/, _.bind(events.handleHashChangeViewDocumentAnnotation,this.events));

      // Handle annotation loading in annotation view
      history.register(/annotation\/a(\d*)$/, _.bind(events.handleHashChangeViewAnnotationAnnotation,this.events));

      // Handle loading of the pages view
      history.register(/pages$/, _.bind(events.handleHashChangeViewPages, events));

      // Handle page loading in text view
      history.register(/text\/p(\d*)$/, _.bind(events.handleHashChangeViewText,this.events));

      // Handle entity display requests.
      history.register(/entity\/p(\d*)\/(.*)\/(\d+):(\d+)$/, _.bind(events.handleHashChangeViewEntity,this.events));

      // Handle search requests
      history.register(/search\/p(\d*)\/(.*)$/, _.bind(events.handleHashChangeViewSearchRequest,this.events));
    },

    // Sets up the zoom slider to match the appropriate for the specified
    // initial zoom level, and real document page sizes.
    autoZoomPage: function() {
      var windowWidth = this.elements.window.outerWidth(true);
      var zoom;
      if (this.viewer.options.zoom == 'auto') {
        zoom = Math.min(
          700,
          windowWidth - (this.viewer.models.pages.REDUCED_PADDING * 2)
        );
      } else {
        zoom = this.viewer.options.zoom;
      }

      // Setup ranges for auto-width zooming
      var ranges = [];
      if (zoom <= 500) {
        var zoom2 = (zoom + 700) / 2;
        ranges = [zoom, zoom2, 700, 850, 1000];
      } else if (zoom <= 750) {
        var zoom2 = ((1000 - 700) / 3) + zoom;
        var zoom3 = ((1000 - 700) / 3)*2 + zoom;
        ranges = [.66*zoom, zoom, zoom2, zoom3, 1000];
      } else if (750 < zoom && zoom <= 850){
        var zoom2 = ((1000 - zoom) / 2) + zoom;
        ranges = [.66*zoom, 700, zoom, zoom2, 1000];
      } else if (850 < zoom && zoom < 1000){
        var zoom2 = ((zoom - 700) / 2) + 700;
        ranges = [.66*zoom, 700, zoom2, zoom, 1000];
      } else if (zoom >= 1000) {
        zoom = 1000;
        ranges = this.viewer.models.document.ZOOM_RANGES;
      }
      this.viewer.models.document.ZOOM_RANGES = ranges;
      this.viewer.slider.slider({'value': parseInt(_.indexOf(ranges, zoom), 10)});
      this.events.zoom(zoom);
    },

    handleInitialState: function(){
      var initialRouteMatch = this.viewer.history.loadURL(true);
      if(!initialRouteMatch) {
        var opts = this.viewer.options;
        this.viewer.open('ViewDocument');
        if (opts.note) {
          this.viewer.pageSet.showAnnotation(this.viewer.models.annotations.byId[opts.note]);
        } else if (opts.page) {
          this.jump(opts.page - 1);
        }
      }
    }

};
