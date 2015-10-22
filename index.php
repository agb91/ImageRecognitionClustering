<?php
include("php/variabili.php");
require('php/funzioni.php');
?>
<!DOCTYPE html>
<html lang="it">
<head>
<title>DIPP</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta charset="utf-8">
<link rel="stylesheet" href="css/bootstrap.css" media="screen">
<link rel="stylesheet" href="css/reset.css" media="screen">
<link rel="stylesheet" href="css/style.css" media="screen">
</head>
<body>
<div class="jumbotron static-navbar">
  <div class="container">
    <h1>DIP_Project</h1>
  </div>
</div>
<?php
if(!isset($_GET['step'])){
?>
<div class="container">
<?php
  if (isset($_GET['up']) && ($_GET['up']=="1")){
    echo '<div class="col-md-6 col-md-offset-3" id="aggiornato">
            <div class="alert alert-success" role="alert">
              <center><h4>Aggiornato</h4></center>
            </div>
          </div>';
  }
?>
  <div class="col-lg-12">
    <h1 id="navbar">Parametri di ricerca</h1>
  </div>
  <div class="bs-docs-section" id="gif_div">
    <div class="row">
      <div class="col-lg-10" >
        <form class="bs-example form-horizontal" data-toggle="validator" method="POST" action="./php/sendSearch.php">
          <div class="form-group">
            <label for="inputkey" class="col-lg-3 control-label">Chiave</label>
            <div class="col-lg-8">
              <input type="text" class="form-control" placeholder="..." aria-describedby="sizing-addon2" name="toSearch" value="" required>
            </div>
          </div>
          <div class="col-lg-12">
            <div class="form-group">
              <div class="col-lg-1"></div>
              <label for="select" class="col-lg-3 control-label">Numero di immagini da scaricare</label>
              <div class="col-lg-3">
                <select class="form-control select" name="numImages">
                  <?php
                  for ($i = 1; $i <= $max_image; $i++) {
                    if($i==$default_image) echo '<option value='.$default_image.' selected="true">'.$default_image.'</option>';
                    else echo '<option value='.$i.'>'.$i.'</option>';
                  }
                  ?>                
                </select>
              </div>

              <label for="select" class="col-lg-3 control-label">Numero di classi</label>
              <div class="col-lg-2">
                <select class="form-control select" name="numClassi">
                  <?php
                  for ($i = 1; $i <= $max_class; $i++) {
                    if($i==$default_class) echo '<option value='.$default_class.' selected="true">'.$default_class.'</option>';
                    else echo '<option value='.$i.'>'.$i.'</option>';
                  }
                  ?>                
                </select>
              </div>
            </div>
          </div>
          <div class="form-group">
            <div class="col-lg-1"></div>
            <label for="select" class="col-lg-3 control-label">Clusterizzazione</label>
            <div class="col-lg-8">
              <div class="btn-group" data-toggle="buttons">               
                <label class="btn btn-default active">
                  <input type="radio" name="selectCluster" value="2" autocomplete="off" checked="checked">Binaria</label>
                <label class="btn btn-default">
                  <input type="radio" name="selectCluster" value="1" autocomplete="off">KMeans</label>
                <label class="btn btn-default">
                  <input type="radio" name="selectCluster" value="0" autocomplete="off">DBScan</label>
              </div>
            </div>
          </div>
          <div class="form-group">
            <div class="col-lg-1"></div>
            <label for="select" class="col-lg-3 control-label">Algoritmi</label>
            <div class="col-lg-8">
            <table>
              <tr>
              <td>
                <input type="checkbox" name="algoritmo1" id="checkboxG1" class="css-checkbox" checked="checked"/>
                <label for="checkboxG1" class="css-label">Algoritmo 1</label>
              </td>
              <td>
                <input type="checkbox" name="algoritmo2" id="checkboxG2" class="css-checkbox" checked="checked"/>
                <label for="checkboxG2" class="css-label">Algoritmo 2</label></td>
              <td>
                <input type="checkbox" name="algoritmo3" id="checkboxG3" class="css-checkbox" checked="checked"/>
                <label for="checkboxG3" class="css-label">Algoritmo 3</label>
              </td>
              </tr>
            </table>
             
            </div>
          </div>
          <div class="form-group">
            <div class="col-lg-1"></div>
            <label for="select" class="col-lg-3 control-label">Cancella</label>
            <div class="col-lg-8">
              <div class="btn-group" data-toggle="buttons">               
                <label class="btn btn-default active">
                  <input type="radio" name="delete" value="no" autocomplete="off" checked="checked">Niente</label>
                <label class="btn btn-default">
                  <input type="radio" name="delete" value="deleteSearch" autocomplete="off">Ultima ricerca con la stessa chiave</label>
                <label class="btn btn-default">
                  <input type="radio" name="delete" value="deleteAll" autocomplete="off">Tutto</label>
              </div>
            </div>
          </div>
          <br>
          <div class="form-group">
            <center>
              <button class="btn btn-default">Cancel</button>
              <button type="submit" class="btn btn-primary">Submit</button>
            </center>
          </div>
        </form>
      </div>
      <div class="col-lg-2">
        <div class="panel panel-primary">
          <div class="panel-heading">
            <h3 class="panel-title"><center>Download precedenti</center></h3>
          </div>
          <div class="panel-body">
            <?php
              get_oldSearch();
            ?>
          </div>
        </div>
      </div>
    </div>
  </div>
<?php
}
ini_set('max_execution_time', 0);
  if(isset($_GET['step']) && ($_GET['step']=="1")){
//echo("ci sono1");
    function run(){
      //echo("ci sono");
      $command = "c:\Python27\python main.py";
       
      $pid = popen( $command,"r");
	  echo("stò elucubrando");
      /*
      while( !feof( $pid ) )
      {
       echo fread($pid, 256);
       flush();
       ob_flush();
       echo "<script>window.scrollTo(0,99999);</script>";
       usleep(100000);
      }
      pclose($pid);
       
      echo "<script>window.scrollTo(0,99999);</script>";
      echo "<br /><br />Script finito<br /><br />";
      header("http://localhost/dipp/index.php?step=2");*/
      }
    run();
    header("Location:http://localhost/dipp/index.php?step=2");
  }
if (isset($_GET['step']) && ($_GET['step']=="2")){
?>
  <div class="container">
    <div class="col-lg-12">

      <h1 id="navbar">Risultati clusterizzazione</h1>
    </div>
    <div class="bs-docs-section">
      <div class="row">
        <div class="col-lg-12">
          <form class="bs-example form-horizontal" data-toggle="validator" method="POST" action="php/updateCluster.php">
          <?php
          //showImage();
          //showImageOrderdByClass();
          showImageClust();
          ?>
           
            <div class="col-lg-12"><br></div>
            <div class="form-group col-lg-12">
              <center>
                <a href="index.php?" class="btn btn-default">Nuova ricerca</a>
                <button type="submit" class="btn btn-primary">Salva</button>
              </center>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div> 
<?php
  
} //end
?>

  <div class="row"></div>
  <footer>
    <div class="row">
      <div class="col-lg-11">
        <p class="pull-right"><a href="#top">Back to top</a></p>
      </div>
      <div class="col-lg-12">
        <p><center>Made by <a href="https://it.linkedin.com/pub/maria-celeste-grandi/b4/421/688" title="linkedin link" target="_blank">LaCele</a> © 2015</center></p>
      </div>
    </div>
  </footer>
</div>
<script src="jquery-1.11.3.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/respond.min.js"></script>
<script src="js/holder.js"></script>
<script src="js/validator.js"></script>
<script src="js/gif_fc.js"></script>
</body>
</html>
