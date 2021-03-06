<!DOCTYPE html>
<!--[if IE 8]>    <html class="no-js lt-ie9" lang="en"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
  <meta charset="utf-8" />

  <!-- Set the viewport width to device width for mobile -->
  <meta name="viewport" content="width=device-width" />

  <title>Dissertation project | Context-Aware Application</title>

  <!-- Included CSS Files -->
  
  <link rel="stylesheet" href="/css/normalize.css">
  <link rel="stylesheet" href="/css/foundation.min.css">

  <script src="/js/vendor/custom.modernizr.js"></script>

</head>
<body>

  <!-- Header and Nav -->

  <div class="row">
    <div class="large-12 columns">
      <div class="panel">
        <h1><a href="/">context-aware application</a></h1>
      </div>
    % if message is not '':
      <div data-alert class="alert-box secondary">
        {{ message }}
        <a href="#" class="close">&times;</a>
    </div>
    %end

    </div>
  </div>

  <div class="row">
    <div class="large-12 columns">
  %include
    </div>
  </div>
  
  <!-- Footer -->

  <footer class="row">
    <div class="large-12 columns">
      <hr />
      <div class="row">
        <div class="large-5 columns">
          <p>&copy; Copyright Damien PUIG.</p>
        </div>
        <div class="large-7 columns">
          <ul class="inline-list right">
            <li><a href="/me">me</a></li>
          </ul>
        </div>
      </div>
    </div>
  </footer>


  <script type="text/javascript" src="/js/vendor/jquery-2.0.3.min.js"></script>
  <script type='text/javascript' src="/js/vendor/foundation.min.js"></script>
  <script type='text/javascript' src="/js/vendor/knockout-2.3.0.js"></script>
  <script type='text/javascript' src="/js/vendor/zepto.js"></script>
  
  <script>
    $(document).foundation();
  </script>

  %if defined('js'):
    %js()



</body>
</html>