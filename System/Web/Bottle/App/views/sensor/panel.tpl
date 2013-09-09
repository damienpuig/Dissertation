
 <!-- Nav Sidebar -->
        <!-- Main Feed -->
    <!-- This has been source ordered to come first in the markup (and on small devices) but to be to the right of the nav on larger screens -->
<div id="content" class="large-8 columns push-4">


      <!-- End Feed Entry -->
      <hr>

<div id="valuecontainer">

  %for value in values:
    %include template/value value=value
  %end

</div>



    </div>

    <!-- This is source ordered to be pulled to the left on larger screens -->
    <div class="large-4 columns pull-8">
      <div class="panel">
         <h5 class="hide-for-small">{{user.email}}<hr></h5>

      <h5 class="subheader">Connected to:</h5>
        <ul class="inline-list">
          <li><a href="#">Arduino1</a></li>
          <li><a href="#">Arduino2</a></li>
          <li><a href="#">Arduino3</a></li>
          <li><a href="#">Arduino4</a></li>
          <li><a href="#">Arduino5</a></li>
        </ul>
      <hr>
     <h5 class="subheader">Connection type</h5>
      <div class="small-6 switch round">

          <input id="d1" name="switch-d" type="radio" value="sc" data-bind="checked: connectionType">
          <label for="d1">True Socket</label>

          <input id="d" name="switch-d" type="radio" value="lpc" data-bind="checked: connectionType">
          <label for="d">Long Polling</label>

          <span></span>
      </div>
      <hr>
      <div id="timecontainer" data-bind='displayTime: connectionType'>
      <h5 class="subheader">Time allocated for LP</h5>
      <div class="row collapse">
                  <div class="small-8 columns">
                    <input type="text" placeholder="in seconds" data-bind="value: seconds">
                  </div>
                  <div class="small-4 columns">
                    <span class="postfix">second(s)</span>
        </div>
      </div>
    </div>
      <a href="#" id="update" data-bind='click: update' class="small button">Update</a>
      <a href="#" id="stop" data-bind='click: stop' class="small button">Cancel</a>
    </div>

%def js():
<script type="text/javascript" src="/js/custom/panel.js"></script>
%end



%rebase layout/layout message=message, user=user, js=js



