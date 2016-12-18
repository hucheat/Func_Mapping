<?php

function t1(){
	system("whoami");
}

function test($a){
	$a .= $a;
	echo $a;
}

function max($x, $y){
	echo $x;
	echo $y;
	return ($x>$y)?$x:$y;
}