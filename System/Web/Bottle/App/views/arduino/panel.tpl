
 <!-- Nav Sidebar -->
        <!-- Main Feed -->
    <!-- This has been source ordered to come first in the markup (and on small devices) but to be to the right of the nav on larger screens -->
<div class="large-8 columns push-4">

  %for value in values:
    %include template/value value=value
  %end

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

%rebase layout/layout message=message, user=user
