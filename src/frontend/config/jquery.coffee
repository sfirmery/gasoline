do ($) ->
  $.fn.toggleWrapper = (obj = {}, cid, init) ->
    methods =
      getWrapperByCid: (cid) ->
        $("[data-wrapper='#{cid}']")

      isTransparent: (bg) ->
        /transparent|rgba/.test bg

      setBackgroundColor: (bg) ->
        if @isTransparent(bg) then "white" else bg

    _.defaults obj,
      className: ""
      backgroundColor: methods.setBackgroundColor @css("backgroundColor")
      zIndex: if @parent().css("zIndex") is "auto" or 0 then 1000 else (Number) @parent().css("zIndex")

    $offset = @offset()
    $width  = @outerWidth(false)
    $height = @outerHeight(false)

    if init
      ## don't add another wrapper if one is already present
      return if methods.getWrapperByCid(cid).length

      ## add the wrapper
      $("<div>")
        .appendTo("body")
          .addClass(obj.className)
            .attr("data-wrapper", cid)
              .css
                width: $width
                height: $height
                top: $offset.top
                left: $offset.left
                position: "absolute"
                zIndex: obj.zIndex + 1
                backgroundColor: obj.backgroundColor
    else
      ## remove the wrapper
      methods.getWrapperByCid(cid).remove()
