<?php
include_once 'parametri.php';
include_once 'variabili.php';
require('funzioni.php');

mkdir($destination_path);

	//connessione
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
	 	trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
	}

	$sql0 = 'SELECT `Path` FROM `maintable` WHERE `Object` ="'.get_key().'";';
	$result = mysqli_query($con, $sql0);
	$var = array();
	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);
	$path= $temp['Path']."\\";

	$class = get_maxClass()-1;
	$save=0;
	$sql = "SELECT * FROM `clusttable` WHERE";

	while ($class>=0){
		if ($_POST['c'.$class]=="1"){
			//echo 'classe selezionata: '.$class. '<br>' ;
			$save+=1;
			if ($save>1) $sql= $sql." or";
			$sql= $sql. " `Class`=\"" . $class."\"";
		}
		$class -=1;
	}

	//echo $sql;
	$result = mysqli_query($con, $sql);
	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);	
	$num = count($var);	

	//echo 'ok<br>';

	for ($i = 1; $i < $num; $i++) {
		$temp = json_decode(json_encode($var[$i]), true); 
		$insert="INSERT INTO `dbtable`(`classe`, `nome`, `path`) VALUES (\"".$temp['Search']."\",\"".$temp['ImageName']."\",\"./ClustImm/\");";
		if (mysqli_query($con, $insert) ) {
		    //echo "update row ok";
		    } else {
		        echo "Error: " . $insert . "<br>" . mysqli_error($con);
		    }
		    //echo "da copiare: ".$path.$temp['ImageName']."<br>";
		copy($path.$temp['ImageName'], $destination_path."\\".$temp['ImageName']);
	}

header("Location:../index.php?up=1");
//close the connection
mysqli_close($con);

  
?>