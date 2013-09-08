 //lpc = long polling connection
  //sc = socket connection
function Panel(){

  var self = this

  this.init= function(){
  ko.applyBindings(new this.panelViewModel(connection.longPolling, 5))
  }

  this.panelViewModel = function (type, time){
  this.last = null
  this.connectionType= ko.observable([type])
  this.seconds= ko.observable(time)
  this.update= function(){
      if(this.connectionType() === connection.longPolling && this.seconds() > 0){ setTimeout(self.ajaxify, this.seconds()) }
      else if(this.connectionType() === connection.socket ){ self.socketify() }
    }
  }

  this.socketify = function(){

    if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#valuecontainer').prepend("<li>Your browser doesn't support WebSockets.</li>");
                }
            }

            ws = new WebSocket('ws://127.0.0.1:8000/websocket')

            ws.onopen = function(evt) {
              alert("connection opened")
            }

            ws.onmessage = function(evt) {
                this.render(evt.data)
            }

            ws.onclose = function(evt) {
                 alert("connection closed")
            }

        }

  this.ajaxify= function(){
     var el = $('#load')

     if(el.length <= 0){
     $('#content').prepend("<h2 id=\"load\"></h2>")
     el = $('#load')
   }

   el.hide()
   el.innerHTML="Loading values..."

   data = {"date": self.panelViewModel.last}

    $.ajax({
      url: '/panel/lpupdate',
      dataType: 'json',
      contentType: 'application/json',
      type:'GET',
      data: data,
      beforeSend: function () {
               el.show()
            },
      success: function(data)
      {
        setTimeout(function(){
          el[0].innerHTML= "Success!"
          if(data.success && data.data.length > 0){
            self.render(data)
          }
        }, 1000)
      },
      error: function (xhr, textStatus, errorThrown) {
        setTimeout(function(){
          el[0].innerHTML= "Loading values... Error!"
        }, 1000)
      }
    })
  }

  this.render = function(result){
     $('#valuecontainer')
     .prepend(result.data)
     .css({'opacity':0})
     .animate({'opacity':1})


     self.panelViewModel.last = result.last

  }
}

$(document).ready(function () {

  ko.bindingHandlers.displayTime = {
    init: function(element, valueAccessor) {
        $(element).toggle(ko.utils.unwrapObservable(valueAccessor()()))
    },
    update: function(element, valueAccessor) {
        connection.longPolling == valueAccessor()() ? $(element).fadeIn() : $(element).fadeOut()
    }
  }

  connection = {
  longPolling: "lpc",
  socket: "sc"
 }

  var panel = new Panel()

  panel.init()

})
