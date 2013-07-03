<h1>Login</h1>
<form action="/login" method="post">
    <dl>
        <dd>email: <input type="input" name="email"/></dd>
        <dd>pass: <input type="input" name="pass"/></dd>
        <dd><input type="submit" value="Flash"/></dd>
    </dl>
</form>
%rebase layout/layout message=message
