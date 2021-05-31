<!DOCTYPE html>
<html lang="es">
<head>
    <title>Fixatges Empresa</title>
    <meta charset="UTF-8">
    <style>
        #FixatgesEmpresa {
            color: blue;
        }
	#tablaDerecha {
	float: left;
	width: 325px;
	}
    </style>
</head>
<body>
<b id="FixatgesEmpresa">
	<?php
		$connexio = mysqli_connect ("localhost", "sergi", "P@ssw0rd", "fixatges");
		echo "<form method='POST'>";
            	echo "<label for='usuari'>Introdueix l'usuari: </label>";
		echo "<input type='text' id='usuari' name='usuari' required><br><br>";
		echo "<label for='contraseña'>Introdueix la contrasenya: </label>";
		echo "<input type='password' id='contraseña' name='contraseña' required><br><br>";
           	echo "<input type='submit' name='enviar' value='Connectar-se'><br><br>";
	  	echo "</form>";

		$usuari = $_POST["usuari"];
		$contra = $_POST["contraseña"];

		if (isset($_POST["enviar"])) {
			$select1 = "SELECT usuari, contrasenya FROM adminsweb WHERE usuari = '$usuari' AND contrasenya = '$contra'";
			$result1 = mysqli_query($connexio, $select1);
			$rows1 = mysqli_fetch_array($result1, MYSQLI_ASSOC);
			if ($rows1["usuari"] == $usuari AND $rows1["contrasenya"] == $contra) {
				$select2 = "SELECT * FROM treballadors ORDER BY id";
				$result2 = mysqli_query($connexio, $select2);
				$rows2 = mysqli_fetch_array($result2, MYSQLI_ASSOC);
				do {
					$data1[] = $rows2;
				}while($rows2 = mysqli_fetch_array($result2, MYSQLI_ASSOC));
				echo "<div id='tablaDerecha'>";
				$taula1 = "<table border='1'>";
				$taula1 .= "<th>ID</th>";
				$taula1 .= "<th>Nom</th>";
				$taula1 .= "<th>Cognom1</th>";
				$taula1 .= "<th>Cognom2</th>";
				$taula1 .= "<th>DNI</th>";
				foreach ($data1 as $a) {
					$taula1 .= "<tr>";
					foreach ($a as $c) {
						$taula1 .= "<td>".$c."</td>";
					}
					$taula1 .= "</tr>";
				}
				$taula1 .= "</table>";
				echo $taula1;
				$select3 = "SELECT * FROM fixatges ORDER BY datahora";
				$result3 = mysqli_query($connexio, $select3);
				$rows3 = mysqli_fetch_array($result3, MYSQLI_ASSOC);
				do {
					$data2[] = $rows3;
				}while($rows3 = mysqli_fetch_array($result3, MYSQLI_ASSOC));
				$taula2 = "<table border='1'>";
				$taula2 .= "<th>ID</th>";
				$taula2 .= "<th>Data i Hora d'entrada</th>";
				foreach ($data2 as $a) {
					$taula2 .= "<tr>";
					foreach ($a as $c) {
						$taula2 .= "<td>".$c."</td>";
					}
					$taula2 .= "</tr>";
				}
				$taula2 .= "</table>";
				echo "</div>";
				echo $taula2;
			}
			else {
				echo "Usuari o contrasenya incorrecte";
			}
		}
		mysqli_close($connexio);
	?>
</b>
</body>
</html>
