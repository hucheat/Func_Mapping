<?php

$f = get_defined_functions();

$ff = $f['internal'];

$i = 0;
$n = count($ff);
$txt = "";
for($i;$i<$n;$i++){
	$txt .= $ff[$i]."\n";
}
file_put_contents("pif.dat", $txt);

?>