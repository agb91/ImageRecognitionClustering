<?php

//funzione per elencare le ricerche precedenti presenti nel database
function get_oldSearch(){
	include 'parametri.php';
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
		 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
		}

	//execute the SQL query and return records
	$var = array();
	$sql = 'SELECT `Object`,`numeroImm` FROM `mainTable` WHERE 1 ORDER BY `Object` ASC';
	$result = mysqli_query($con, $sql);

	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	//$temp = json_decode(json_encode($var[0]), true);	

    $num = count($var);	
	for ($i = 0; $i < $num; $i++) {
	  	$temp = json_decode(json_encode($var[$i]), true);
      echo $temp['Object'].' ('.$temp['numeroImm'].' imm)<br>';
    }

    mysqli_close($con);

}

//funzione per prendere la chiave di ricerca dal db
function get_key(){
	include 'parametri.php';
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
		 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
		}

	//execute the SQL query and return records
	$var = array();
	$sql = 'SELECT * FROM `inputTable` WHERE `ID` ="0";';
	$result = mysqli_query($con, $sql);

	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);	
    mysqli_close($con);
	return str_replace(" ", "_", $temp['toSearch']);
}

//funzione per avere il numero massimo di classi dal database
function get_maxClass(){
	include 'parametri.php';
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
		 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
		}

	//execute the SQL query and return records
	$var = array();
	$sql = 'SELECT `numClassi` FROM `inputTable` WHERE `ID` ="0";';
	$result = mysqli_query($con, $sql);

	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);	
    mysqli_close($con);
	return $temp['numClassi'];
}

//controlla il formato delle immagini
function controllaFormato($nomefile){
  if(strripos($nomefile, '.jpg'))  return TRUE;
  return FALSE; //non è stato trovato alcun formato
}

//prende in ingresso il nome dell'immagine
//restituisce un array con rank in posizione 0
//						   classe in posizione 1
function get_rank_class($img){
	include 'parametri.php';
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
		 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
		}

	//execute the SQL query and return records
	$var = array();
	$sql = 'SELECT `Rank`, `Class` FROM `clusttable` WHERE `ImageName`="'.$img.'"';
	$result = mysqli_query($con, $sql);

	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);	
    mysqli_close($con);
	return $temp;

}

function showImage(){
	$toSearch = get_key();
	$maxClass = get_maxClass();
	$dir=opendir('imm/'.$toSearch);
    if(!$dir){
      echo '<h3><strong>Errore!</strong> Impossibile aprire la directory.</h3>';
    }else{
    	while(!(($file=readdir($dir))===false)){
    		if(controllaFormato($file)){	//controlla il formato delle immagini
											//legge solo le immagini .jpg della cartella
    			$r_c= get_rank_class($file);
		      	echo '	<div class="col-xs-6 col-md-3 div_image">
		      				 <center><h4>'.$file.'</h4></center>';
		        if ($r_c['Rank']==="-1") echo '<center><h5>rank: '.$r_c['Rank'].'</h5></center>';
				echo      '<a class="thumbnail">
				               <img class ="imm_show" src="imm/'.$toSearch.'/'.$file.'" alt="'.$file.'">
				             </a>
				             <select class="form-control select rank" name="">';
			   for ($i = 0; $i < $maxClass; $i++) {
			      if($i==$r_c['Class']) echo '<option value='.$r_c['Class'].' selected="true"> classe '.$r_c['Class'].'</option>';
			      else echo '<option value='.$i.'>classe '.$i.'</option>';
			    }
               echo '</select>
		           	</div>';
		    }
    	}
	}
}

//conta quante immagini ci sono in una classe
function get_countClass($c){
	include 'parametri.php';
	$con = mysqli_connect($host, $user, $password, $dbName);
	if (!$con) {
		 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
		}

	//execute the SQL query and return records
	$var = array();
	$sql = 'SELECT COUNT(*) FROM `clustTable` WHERE `Class`="'.$c.'"';
	$result = mysqli_query($con, $sql);

	while($obj = mysqli_fetch_object($result)) {
		$var[] = $obj;
	}
	$temp = json_decode(json_encode($var[0]), true);	
    mysqli_close($con);
    return $temp;
}


function showImageOrderdByClass(){
	$toSearch = get_key();
	$dir=opendir('imm/'.$toSearch);
	$maxClass = get_maxClass();
	$conteggio = array();
	//conto quante immagini ci sono in ogni classe
	for($i=0; $i<$maxClass; $i++){
		$conteggio[$i]=get_countClass($i);
	}

//mostro immagini a partire dalla classe più numerosa
	while(max($conteggio)!=0){
		$i=0;
		$max = max($conteggio);	//numero di elementi nella classe
		while($max!=$conteggio[$i]) $i++;
		$conteggio[$i]=0;
		$c=$i;	//classe corrente

		include 'parametri.php';
		$var = array();

		$con = mysqli_connect($host, $user, $password, $dbName);
		if (!$con) {
			 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
			}

		//execute the SQL query and return records
		$var = array();
		$sql = 'SELECT * FROM `clustTable` WHERE `Class`="'.$c.'"';
		$result = mysqli_query($con, $sql);

		while($obj = mysqli_fetch_object($result)) {
			$var[] = $obj;
		}
		$num = count($var);	

		for ($i = 0; $i < $num; $i++) {
		    $temp = json_decode(json_encode($var[$i]), true);
	      	echo '	<div class="col-xs-6 col-md-3 div_image">
	      				 <center><h4>'.$temp['ImageName'].'</h4></center>';
		        if ($temp['Rank']!="-1") echo '<center><h5>rank: '.$temp['Rank'].'</h5></center>';
				echo      '<a class="thumbnail">
			               <img class ="imm_show" src="imm/'.$temp['Search'].'/'.$temp['ImageName'].'" alt="'.$temp['ImageName'].'">
			             </a>
			             <select class="form-control select rank" name="'.str_replace(".jpg", "", $temp['ImageName']).'">';
		   for ($j = 0; $j < $maxClass; $j++) {
		      if($j==$temp['Class']) echo '<option value='.$temp['Class'].' selected="true"> classe '.$temp['Class'].'</option>';
		      else echo '<option value='.$j.'>classe '.$j.'</option>';
		    }
	       echo '</select>
	           	</div>';
	   }
	}
}


function showImageClust(){
	$toSearch = get_key();
	$dir=opendir('imm/'.$toSearch);
	$maxClass = get_maxClass();
	$conteggio = array();
	//conto quante immagini ci sono in ogni classe
	for($i=0; $i<$maxClass; $i++){
		$conteggio[$i]=get_countClass($i);
	}

//mostro immagini a partire dalla classe più numerosa
	while(max($conteggio)!=0){
		$i=0;
		$max = max($conteggio);	//numero di elementi nella classe
		while($max!=$conteggio[$i]) $i++;
		$conteggio[$i]=0;
		$c=$i;	//classe corrente

		include 'parametri.php';
		$var = array();

		$con = mysqli_connect($host, $user, $password, $dbName);
		if (!$con) {
			 trigger_error('Could not connect to MySQL: ' . mysqli_connect_error());
			}

		//execute the SQL query and return records
		//seleziona le immagini appartententi a una classe
		$var = array();
		$sql = 'SELECT * FROM `clustTable` WHERE `Class`="'.$c.'"';
		$result = mysqli_query($con, $sql);

		while($obj = mysqli_fetch_object($result)) {
			$var[] = $obj;
		}
		$num = count($var);	
		echo '
			<div class="col-xs-12 div_image">';
		//mostra le immagini appartenenti alla classe
		for ($i = 0; $i < $num; $i++) {
		    $temp = json_decode(json_encode($var[$i]), true);
	      	echo '	<div class="col-xs-6 col-md-2">
	      				 <center><h5>'.$temp['ImageName'].'</h5></center>';
		        if ($temp['Rank']!="-1") echo '<center><h6>rank: '.$temp['Rank'].'</h6></center>';
				echo      '<a class="thumbnail">
			               <img class ="imm_show" src="imm/'.$temp['Search'].'/'.$temp['ImageName'].'" alt="'.$temp['ImageName'].'">
			             </a>
					<h4>Classe '.$c.', im'.($i).'</h4>
					<input type="radio" name="c'.$c.($i).'" value="1" id="radio1" />
					<label for="radio1" class="css-label radGroup2">Si</label>				
					<input type="radio" name="c'.$c.($i).'" value="0" id="radio2"  checked/>
					<label for="radio2" class="css-label radGroup2">No</label>	
	           	</div>';
	   }
	   echo '</div>';

	}
}

?>