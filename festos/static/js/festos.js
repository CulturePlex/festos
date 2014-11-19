/** Another hack to send a functions with parameters **/
function partial(func /*, 0..n args */) {
  var args = Array.prototype.slice.call(arguments, 1);
  return function() {
    var allArguments = args.concat(Array.prototype.slice.call(arguments));
    return func.apply(this, allArguments);
  };
}

/** A simple hack function to apply bootstrap style to the docviewer **/
var set_boostrap_header = function(url, title, author, owner){
  jQuery('<h4/>', {
    class: 'media-heading'
  }).append(
  jQuery('<a/>', {
    href: url,
//    text: title + ', ' + author,
    text: title,
  })).append(
  jQuery('<small/>', {
    text: ' @' + owner,
    href: '/accounts/' + owner
  })).appendTo($('.docviewer-title').empty());
  if (typeof afterLoad !== "undefined" && afterLoad){
    afterLoad();
  }
}
