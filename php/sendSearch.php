<?php
include_once 'parametri.php';

if (isset($_POST['algoritmo1'])) $a1=1;
else $a1=0;
if (isset($_POST['algoritmo2'])) $a2=1;
else $a2=0;
if (isset($_POST['algoritmo3'])) $a3=1;
else $a3=0;
$deleteSearch=0;
$deleteAll=0;
if($_POST['delete']=="deleteAll") $deleteAll=1;
elseif ($_POST['delete']=="deleteSearch") $deleteSearch=1;

$con = mysqli_connect($host, $user, $password, $dbName);
if (!$con) {
 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
}

$query = "UPDATE `inputTable` SET `toSearch`=\"".$_POST['toSearch']."\",`numImages`=\"".$_POST['numImages']."\",`deleteSearch`=\"".$deleteSearch."\",`deleteAll`=\"".$deleteAll."\",`selectCluster`=\"".$_POST['selectCluster']."\",`algoritmo1`=\"".$a1."\",`algoritmo2`=\"".$a2."\",`algoritmo3`=\"".$a3."\",`numClassi`=\"".$_POST['numClassi']."\" WHERE`ID` =\"0\";";

if (mysqli_query($con, $query)){
  //echo "New record created successfully";
    echo "fatto!<br>"; 
  }else {
    echo "Error: " . $query . "<br>" . mysqli_error($con);
}

header("Location:http://localhost/dipp/index.php?step=1");

//close the connection
mysqli_close($con);

//exec('python ../py/prova.py', $output);
//$var = array();
//$var = var_dump($output);
//echo("<br>sono qui");
//echo("<br>output: ".$var);
?>
