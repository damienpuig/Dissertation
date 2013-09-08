<!-- Header Content -->
        <div class="row">
 
          <div class="large-6 columns">
 
            <img src="http://arduino.cc/en/uploads/Main/ArduinoDiecimilaComponents.jpg"><br>
 
          </div>

          <div class="large-6 columns">
            <div class="panel">
              <h4 class="hide-for-small">{{device.name}}<hr></h4>
            <h5 class="subheader">{{device.description}}</h5>
            </div>
 
          <div class="row">
              <div class="large-6 small-6 columns">
                <div class="panel">
                <h5 class="hide-for-small">Number of values<hr></h5>
                <h6 class="subheader">{{len(device.values)}}</h6>
                </div>
              </div>
 
              <div class="large-6 small-6 columns">
                <div class="panel">
                   <h5 class="hide-for-small">Location<hr></h5>
                  <strong>Longitude: </strong> <p> {{device.location['coordinates'][0]}} </p>
                  <strong>Latitude: </strong><p> {{device.location['coordinates'][1]}} </p>
                </div>
              </div>
          </div>
          </div>
        </div>

<script type="text/javascript">


</script>
%rebase layout/layout message=message, user=user