<?php

/* asd */
echo 1;
/*
sa
 */

function t1(){
	system("whoami");
}

// test
function test($a){
	$a .= $a;
	echo $a;
}

function mmax($x, $y){
	echo $x;
	echo $y;
	return ($x>$y)?$x:$y;
}


function mmm(){
	function in(){
		test('in');
	}
	in();
}

mmm();

function vvv($a){
    test();
	$a .= "vvv";
	echo $a;
}

?>