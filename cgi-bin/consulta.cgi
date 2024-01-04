#!C:\xampp\perl\bin\perl.exe
use strict;
use warnings;
use CGI;

my $q = CGI->new;

print $q->header('text/html');
print <<HTML;
<!DOCTYPE html>
<html>
<head>
  <title>Consulta</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" type="text/css" href="../styles.css">
  <style>
    .not-found {
      text-align: center;
      font-size: 15px;
      color: red;
    }
    .found {
      text-align: center;
      margin: 15px;
      font-size: 13px;
      color: black;
    }
    .return {
      background-color: #4285f4;
      color: #ffffff;
      border: none;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      cursor: pointer;
      border-radius: 24px;
      margin-top: 15px;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      font-size: 10px;
    }

    th, td {
      border: 1px solid #dddddd;
      text-align: center;
      padding: 8px;
    }

    th {
      background-color: #f2f2f2;
    }
    .c {
      max-height: auto;
      max-width: 80%;
      margin: 50px auto;
      text-align: center;
      background-color: white;
      padding: 20px;
      border-radius: 40px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
  </style>
</head>

<body>
HTML

my $nu = $q->param("name_university");
my $lp = $q->param("licensing_period");
my $ld = $q->param("local_department");
my $pn = $q->param("program_name");
my @results;

my $flag;

if (!($nu eq "") && !($lp eq "") && !($ld eq "") && !($pn eq "")) {
  open(IN, "../data/data.csv") or die "<h1>ERROR: No se pudo abrir el archivo data.csv: $!</h1>\n";
  while (my $line = <IN>) {
    chomp $line;
    my %dict = analyze($line);
    if (keys %dict) {
      my $nu1 = $dict{"NOMBRE"};
      my $lp1 = $dict{"PERIODO_LICENCIAMIENTO"};
      my $ld1 = $dict{"DEPARTAMENTO_LOCAL"};
      my $pn1 = $dict{"DENOMINACION_PROGRAMA"};
      if (defined($nu1) && $nu1 eq $nu && 
          defined($lp1) && $lp1 eq $lp && 
          defined($ld1) && $ld1 eq $ld && 
          defined($pn1) && $pn1 eq $pn) {
        push @results, $line;
        $flag = 1;
      }
    }
  }
  close(IN) or die "<h1>ERROR: No se pudo cerrar el archivo data.csv: $!</h1>\n";
}
print <<HTML;
  <div class="c">
    <h1>Resultado de su consulta</h1>
HTML

if (!defined($flag)) { #NO ENCONTRÓ
  print <<HTML;
    <h1 class="not-found">No encontrado</h1>
      
    <form action="../index.html">
      <input type="submit" class="return" value="Volver a buscar">
    </form>
  </div>
HTML
} else { #ENCONTRÓ
  foreach my $line2 (@results){
    my %u = analyze($line2);
    my $a0 = %u{"CODIGO_ENTIDAD"};
    my $a1 = %u{"NOMBRE"};
    my $a2 = %u{"TIPO_GESTION"};
    my $a3 = %u{"ESTADO_LICENCIAMIENTO"};
    my $a4 = %u{"PERIODO_LICENCIAMIENTO"};
    my $a5 = %u{"DEPARTAMENTO_LOCAL"};
    my $a6 = %u{"PROVINCIA_LOCAL"};
    my $a7 = %u{"DISTRITO_LOCAL"};
    my $a8 = %u{"DENOMINACION_PROGRAMA"};
    my $a9 = %u{"TIPO_NIVEL_ACADEMICO"};
    print <<HTML;
      <h1 class="found">Encontrado:</h1>
      <table class="responsive-table">
        <thead>
          <tr>
            <th style="width: 1px">CODIGO</th>
            <th style="width: 200px">NOMBRE</th>
            <th style="width: 50px">GESTION</th>
            <th style="width: 60px">ESTADO LIC.</th>
            <th style="width: 1px">PERIODO LIC.</th>
            <th style="width: 50px">DEPARTAMENTO</th>
            <th style="width: 50px">PROVINCIA</th>
            <th style="width: 100px">DISTRITO</th>
            <th style="width: 500px">PROGRAMA</th>
            <th style="width: 60px">NIVEL ACADEMICO</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="width: 1px"> $a0 </td>
            <td style="width: 200px"> $a1 </td>
            <td style="width: 50px"> $a2 </td>
            <td style="width: 60px"> $a3 </td>
            <td style="width: 1px"> $a4 </td>
            <td style="width: 50px"> $a5 </td>
            <td style="width: 50px"> $a6 </td>
            <td style="width: 100px"> $a7 </td>
            <td style="width: 500px"> $a8 </td>
            <td style="width: 60px"> $a9 </td>
          </tr>
        </tbody>

      </table>
HTML
  }
  
  print <<HTML;  
    <form action="../index.html">
      <input type="submit" class="return" value="Volver a buscar">
    </form>
HTML
}

print <<HTML;
  </body>
  </html>
HTML

exit;

sub analyze{
  my %dict = ();
  my $line = $_[0];
  if ($line =~ /^(\d{3})\|([^|]+)\|\b(PÚBLICO|PRIVADO)\b\|\b(LICENCIA OTORGADA)\|(\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|([-+]?\d+\.\d+)\|([-+]?\d+\.\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|(\d+)\|([^|]+)\|([^|]+)\|([^|]+)$/) {
    $dict{"CODIGO_ENTIDAD"} = $1;
    $dict{"NOMBRE"} = $2;
    $dict{"TIPO_GESTION"} = $3;
    $dict{"ESTADO_LICENCIAMIENTO"} = $4;
    $dict{"PERIODO_LICENCIAMIENTO"} = $5;
    $dict{"DEPARTAMENTO_LOCAL"} = $11;
    $dict{"PROVINCIA_LOCAL"} = $12;
    $dict{"DISTRITO_LOCAL"} = $13;
    $dict{"DENOMINACION_PROGRAMA"} = $17;
    $dict{"TIPO_NIVEL_ACADEMICO"} = $18;
  } else {
    return ();
  }
  return %dict;
}