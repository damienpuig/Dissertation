
 <!-- Nav Sidebar -->
        <!-- Main Feed -->
    <!-- This has been source ordered to come first in the markup (and on small devices) but to be to the right of the nav on larger screens -->
<div class="large-8 columns push-4">

      <!-- Feed Entry -->
      <div class="row">
        <div class="small-3 large-2 columns "><img src="http://www.semageek.com/wp-content/uploads/2011/03/ArduinoUNO_Front.jpg" width="80px" height="80px"></div>
        <div class="small-9 large-10 columns">
          <p><strong>Value at ... :</strong> Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong.</p>
          <ul class="inline-list">
            <li><a href="arduino/index?name=">Check arduino</a>
            </li>
          </ul>


          <h6>1 Comment</h6>
          <div class="row">
            <div class="small-3 large-2 columns"><img src="http://a5.mzstatic.com/us/r1000/069/Purple/v4/dc/b2/4d/dcb24d22-b0ba-325b-e1fc-cf3f73be0bed/mzl.uubhibka.png" width="50px" height="50px"></div>
            <div class="small-9 large-10 columns">
              <strong>{{user.email}}</strong><p>Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit</p></div>
          </div>
        </div>

      </div>
      <!-- End Feed Entry -->

      <hr>


    </div>

    <!-- This is source ordered to be pulled to the left on larger screens -->
    <div class="large-4 columns pull-8">
      <div class="panel">
        <h5><a href="#">{{user.email}}</a></h5>
        
        <div class="section-container vertical-nav" data-section data-options="deep_linking: false; one_up: true">
      <section class="section">
        <h5 class="title"><a href="#">Arduino 1</a></h5>
      </section>
      <section class="section">
        <h5 class="title"><a href="#">Arduino 2</a></h5>
      </section>
      <section class="section">
        <h5 class="title"><a href="#">Arduino 3</a></h5>
      </section>
      <section class="section">
        <h5 class="title"><a href="#">Arduino 4</a></h5>
      </section>
      </div>

      </div>
    </div>

%rebase layout/layout message=message, user = user
