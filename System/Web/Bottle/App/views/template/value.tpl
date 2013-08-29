
      <!-- Feed Entry -->
      <div class="row" id={{value.id}}>
        <div class="small-3 large-2 columns "><img src="http://www.semageek.com/wp-content/uploads/2011/03/ArduinoUNO_Front.jpg" width="80px" height="80px"></div>
        <div class="small-9 large-10 columns">
          <p>
            <strong>Value id:</strong>
            {{value.id}}
          </p>
          <p>
            <strong>Value:</strong>
            {{value.value}}
          </p>
          <ul class="inline-list">
            <li><a href="arduino/index?name=" + >Check arduino</a>
            </li>
          </ul>

          %if value.comments :
            <h6>len(value.comments) Comments</h6>

            %for comment in value.comments:
              <div class="row">
                <div class="small-3 large-2 columns"><img src="http://a5.mzstatic.com/us/r1000/069/Purple/v4/dc/b2/4d/dcb24d22-b0ba-325b-e1fc-cf3f73be0bed/mzl.uubhibka.png" width="50px" height="50px"></div>
                <div class="small-9 large-10 columns">
                  <strong>{{comment.author}}</strong> at {{comment.date}}
                  <p>{{comment.content}}</p>
                </div>
              </div>
            %end
          %end
        </div>
      </div>