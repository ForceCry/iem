<?php

function printHTML($urls){
global $rooturl;
$frames = sizeof($urls);
?>

<script language="JavaScript1.2" type="text/javascript">

// <!--

//============================================================
//                >> jsImagePlayer 1.0 <<
//            for Netscape3.0+, September 1996
//============================================================
//                  by (c)BASTaRT 1996
//             Praha, Czech Republic, Europe
//
// feel free to copy and use as long as the credits are given
//          by having this header in the code
//
//          contact: xholecko@sgi.felk.cvut.cz
//          http://sgi.felk.cvut.cz/~xholecko

//********* SET UP THESE VARIABLES - MUST BE CORRECT!!!*********************
 

first_image = 0;
last_image = <?php echo $frames-1; ?>;


//=== global variables ====
theImages = new Array();      //holds the images
imageNum = new Array();       //keeps track of which images to omit from loop
//radtimes = new Array();
normal_delay = 300;
delay = normal_delay;         //delay between frames in 1/100 seconds
delay_step = 50;
delay_max = 4000;
delay_min = 50;
dwell_multipler = 3;
dwell_step = 1;
end_dwell_multipler   = dwell_multipler;
start_dwell_multipler = dwell_multipler;
current_image = first_image;     //number of the current image
timeID = null;
status = 0;                      // 0-stopped, 1-playing
play_mode = 0;                   // 0-normal, 1-loop, 2-sweep
size_valid = 0;

//===> Make sure the first image number is not bigger than the last image number
if (first_image > last_image)
{
   var help = last_image;
   last_image = first_image;
   first_image = help;
}


theImages[0] = new Image();
theImages[0].src = "<?php echo $urls[0]; ?>";
imageNum[0] = true;

//==============================================================
//== All previous statements are performed as the page loads. ==
//== The following functions are also defined at this time.   ==
//==============================================================
 
//===> Stop the animation
function stop()
{
   //== cancel animation (timeID holds the expression which calls the fwd or bkwd function) ==
   if (status == 1)
      clearTimeout (timeID);
   status = 0;
}
 
 
//===> Display animation in fwd direction in either loop or sweep mode
function animate_fwd()
{
   current_image++;                      //increment image number
 
   //== check if current image has exceeded loop bound ==
   if (current_image > last_image) {
      if (play_mode == 1) {              //fwd loop mode - skip to first image
         current_image = first_image;
      }
      if (play_mode == 2) {              //sweep mode - change directions (go bkwd)
         current_image = last_image;
         animate_rev();
         return;
      }
   }
 
   //== check to ensure that current image has not been deselected from the loop ==
   //== if it has, then find the next image that hasn't been ==
   while (imageNum[current_image-first_image] == false) {
         current_image++;
         if (current_image > last_image) {
            if (play_mode == 1)
               current_image = first_image;
            if (play_mode == 2) {
               current_image = last_image;
               animate_rev();
               return;
            }
         }
   }
 
   //document.form.radtime.value = radtimes[current_image-first_image];
   document.animation.src = theImages[current_image-first_image].src;   //display image onto screen

   delay_time = delay;
   if ( current_image == first_image) delay_time = start_dwell_multipler*delay;
   if (current_image == last_image)   delay_time = end_dwell_multipler*delay;
 
   //== call "animate_fwd()" again after a set time (delay_time) has elapsed ==
   timeID = setTimeout("animate_fwd()", delay_time);
}
 
 
//===> Display animation in reverse direction
function animate_rev()
{
   current_image--;                      //decrement image number
 
   //== check if image number is before lower loop bound ==
   if (current_image < first_image) {
     if (play_mode == 1) {               //rev loop mode - skip to last image
        current_image = last_image;
     }
     if (play_mode == 2) {
        current_image = first_image;     //sweep mode - change directions (go fwd)
        animate_fwd();
        return;
     }
   }
 
   //== check to ensure that current image has not been deselected from the loop ==
   //== if it has, then find the next image that hasn't been ==
   while (imageNum[current_image-first_image] == false) {
         current_image--;
         if (current_image < first_image) {
            if (play_mode == 1)
               current_image = last_image;
            if (play_mode == 2) {
               current_image = first_image;
               animate_fwd();
               return;
            }
         }
   }
 
  //document.form.radtime.value = radtimes[current_image-first_image];
   document.animation.src = theImages[current_image-first_image].src;   //display image onto screen

   delay_time = delay;
   if ( current_image == first_image) delay_time = start_dwell_multipler*delay;
   if (current_image == last_image)   delay_time = end_dwell_multipler*delay;
 
   //== call "animate_rev()" again after a set amount of time (delay_time) has elapsed ==
   timeID = setTimeout("animate_rev()", delay_time);
}
 
 
//===> Changes playing speed by adding to or substracting from the delay between frames
function change_speed(dv)
{
   delay+=dv;
   //== check to ensure max and min delay constraints have not been crossed ==
   if(delay > delay_max) delay = delay_max;
   if(delay < delay_min) delay = delay_min;
}
 
//===> functions that changed the dwell rates.
function change_end_dwell(dv) {
   end_dwell_multipler+=dv;
   if ( end_dwell_multipler < 1 ) end_dwell_multipler = 0;
   }
 
function change_start_dwell(dv) {
   start_dwell_multipler+=dv;
   if ( start_dwell_multipler < 1 ) start_dwell_multipler = 0;
   }
 
//===> Increment to next image
function incrementImage(number)
{
   stop();
 
   //== if image is last in loop, increment to first image ==
   if (number > last_image) number = first_image;
 
   //== check to ensure that image has not been deselected from loop ==
   while (imageNum[number-first_image] == false) {
         number++;
         if (number > last_image) number = first_image;
   }
 
   current_image = number;
   //document.form.radtime.value = radtimes[current_image-first_image];
   document.animation.src = theImages[current_image-first_image].src;   //display image
}
//===> Decrement to next image
function decrementImage(number)
{
   stop();
 
   //== if image is first in loop, decrement to last image ==
   if (number < first_image) number = last_image;
 
   //== check to ensure that image has not been deselected from loop ==
   while (imageNum[number-first_image] == false) {
         number--;
         if (number < first_image) number = last_image;
   }
 
   current_image = number;
   //document.form.radtime.value = radtimes[current_image-first_image];
   document.animation.src = theImages[current_image-first_image].src;   //display image
}
 
//===> "Play forward"
function fwd()
{
   stop();
   status = 1;
   play_mode = 1;
   animate_fwd();
}
 
//===> "Play reverse"
function rev()
{
   stop();
   status = 1;
   play_mode = 1;
   animate_rev();
}

//===> "play sweep"
function sweep() {
   stop();
   status = 1;
   play_mode = 2;
   animate_fwd();
   }
 
//===> Change play mode (normal, loop, swing)
function change_mode(mode)
{
   play_mode = mode;
}
 
//===> Load and initialize everything once page is downloaded (called from 'onLoad' in <BODY>)
function launch()
{
<?php
for ($q=1;$q<$frames;$q++){
  echo "theImages[$q] = new Image();\n";
  echo "theImages[$q].src = \"". $urls[$q]."\";\n";
  echo "document.animation.src = theImages[$q].src;\n";
} 
?>

   // this needs to be done to set the right mode when the page is manually reloaded
   change_mode (1);
   fwd();
}
 
//===> Check selection status of image in animation loop
function checkImage(status,i)
{
   if (status == true)
      imageNum[i] = false;
   else imageNum[i] = true;
}
 
//==> Empty function - used to deal with image buttons rather than HTML buttons
function func()
{
}
 
//===> Sets up interface - this is the one function called from the HTML body
function animation()
{
  count = first_image;
}
// -->
</SCRIPT>

<body BGCOLOR="#FFFFFF" onLoad="launch()">

<div style="width: 100%; text-align: center;">

<img NAME="animation" BORDER=0 SRC="<?php echo $urls[0]; ?>">
<br />
<a HREF="JavaScript: func()" onClick="change_mode(1);fwd()"><img BORDER=0 WIDTH=29 HEIGHT=24 SRC="<?php echo $rooturl; ?>/images/nrm_button.gif" ALT="Normal"></a>
<a HREF="JavaScript: func()" onClick="sweep()"><img BORDER=0 WIDTH=29 HEIGHT=24
SRC="<?php echo $rooturl; ?>/images/swp_button.gif" ALT="Sweep"></a>

<a HREF="JavaScript: func()" onClick="change_mode(1);rev()"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/rev_button.gif" ALT="REV"></a>
<a HREF="JavaScript: func()" onClick="stop()"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/stp_button.gif" ALT="STOP"></a>
<a HREF="JavaScript: func()" onClick="change_mode(1);fwd()"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/fwd_button.gif" ALT="FWD"></a>

<a HREF="JavaScript: func()" onClick="change_start_dwell(-dwell_step)"><img BORDER=0 WIDTH=29 HEIGHT=24 SRC="<?php echo $rooturl; ?>/images/dw1_minus.gif" ALT="dec"></a>
<a HREF="JavaScript: func()" onClick="change_start_dwell(dwell_step)"><img BORDER=0 WIDTH=29 HEIGHT=24 SRC="<?php echo $rooturl; ?>/images/dw1_plus.gif" ALT="inc"></a>

<a HREF="JavaScript: func()" onClick="change_end_dwell(-dwell_step)"><img BORDER=0 WIDTH=29 HEIGHT=24 SRC="<?php echo $rooturl; ?>/images/dw2_minus.gif" ALT="dec"></a>
<a HREF="JavaScript: func()" onClick="change_end_dwell(dwell_step)"><img BORDER=0 WIDTH=29 HEIGHT=24 SRC="<?php echo $rooturl; ?>/images/dw2_plus.gif" ALT="inc"></a>

<a HREF="JavaScript: func()" onClick="change_speed(delay_step)"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/slw_button.gif" ALT="--"></a>
<a HREF="JavaScript: func()" onClick="change_speed(-delay_step)"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/fst_button.gif" ALT="++"></a>

<a HREF="JavaScript: func()" onClick="decrementImage(--current_image)"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/mns_button.gif" ALT="-1"></a>
<a HREF="JavaScript: func()" onClick="incrementImage(++current_image)"><img BORDER=0 WIDTH=35 HEIGHT=35 SRC="<?php echo $rooturl; ?>/images/pls_button.gif" ALT="+1"></a>

</div>

<?php
} 
?>
