 //lpc = long polling connection
  //sc = socket connection
function Panel(){

  var self = this
  this.lpaction = null
  this.socketaction = null


  this.init= function(){
  self.panelViewModel = new this.panelViewModel(connection.longPolling, 5)
  ko.applyBindings(self.panelViewModel)
  }

  this.panelViewModel = function (type, time){
  this.last = null
  this.connectionType= ko.observable([type])
  this.seconds= ko.observable(time).extend({ numeric: 0 });
  this.update= function(){

      $('#update').attr('disabled','disabled')


      if(this.connectionType() === connection.longPolling && this.seconds() > 0){
        var timeout= self.panelViewModel.seconds() * 1000
        self.lpaction = setInterval(function() { self.poll(timeout) }, timeout)
      }
      else if(this.connectionType() === connection.socket ){
       self.socketaction = self.socketify()
      }
    }
  this.stop = function(){
    self.clearwork()
    $('#update').removeAttr('disabled','disabled')
  }

  }

  this.clearwork = function(){
    if(self.lpaction != null) clearInterval(self.lpaction)

    if(self.socketaction != null) self.socketaction.close()

    self.lpaction = null
    self.socketaction = null
  }

  this.socketify = function(){

    if (!window.WebSocket) {
                if (window.MozWebSocket) {
                    window.WebSocket = window.MozWebSocket;
                } else {
                    $('#valuecontainer').prepend("<li>Your browser doesn't support WebSockets.</li>")
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

this.poll= function(timeout){

  var el = self.loader()


  var data = {"date": self.panelViewModel.last}

   if(null === self.panelViewModel.last) data = null


    $.ajax({
      url: '/panel/lpupdate',
      dataType: 'json',
      contentType: 'application/json',
      type:'GET',
      data: data,
      timeout: timeout,
      cache:false,
      async: true,
      beforeSend: function () {
               el.show()
            },
      success: function(data)
      {
          el[0].innerHTML= "Success! "

          if(data.hasOwnProperty('data')) 
            self.render(data.data)

          el[0].innerHTML = el[0].innerHTML + data.count + " new value(s)"

          self.panelViewModel.last = data.last
      },
      error: function (xhr, textStatus, errorThrown) {
        setTimeout(function(){ 
        el[0].innerHTML= "Error!"
        }, 1000)
      }
    })
  }

this.render = function(result){
     $('#valuecontainer')
     .prepend(result)
     .css({'opacity':0})
     .animate({'opacity':1})
  }

this.loader = function() {
    var el = $('#load')

     if(el.length <= 0){
     $('#content').prepend("<h2 id=\"load\"></h2>")
     el = $('#load')
   }

   el.html("<center><img src=\"/images/ajax-loader.gif\"></center>")

   return $('#load')
}

}

$(document).ready(function () {

  ko.bindingHandlers.displayTime = {
    init: function(element, valueAccessor) {
        $(element).toggle(ko.utils.unwrapObservable(valueAccessor()()))
    },
    update: function(element, valueAccessor) {
      var value = valueAccessor()()
        connection.longPolling == valueAccessor()() ? $(element).fadeIn() : $(element).fadeOut()
    }
  }

  ko.extenders.numeric = function(target, precision) {
    //create a writeable computed observable to intercept writes to our observable
    var result = ko.computed({
        read: target,  //always return the original observables value
        write: function(newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? 0 : parseFloat(+newValue),
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;
 
            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    });
 
    //initialize with current value to make sure it is rounded appropriately
    result(target());
 
    //return the new computed observable
    return result;
};


  connection = {
  longPolling: "lpc",
  socket: "sc"
 }

  var panel = new Panel()
  panel.init()

})
