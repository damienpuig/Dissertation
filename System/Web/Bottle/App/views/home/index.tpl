
<ul>
    <p>
    	%if isauth :
    	<a href="/logout" class="large button expand">Logout</a>
    	%else:
    	<a href="/login" class="large button expand">Login</a>
    	%end

        <a href="/new" class="large button expand">Create user</a>
    </p>
</ul>




%rebase layout/layout message=message