<?php
echo "XCPC Rating Project 概念 Demo<br/><br/>";

$servername = "sh-cynosdbmysql-grp-51uynye4.sql.tencentcdb.com";
$username = "root";
$password = "f70v655V9kMv0j2jUz";
$dbname = "xcpc";
$port = 22347;

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname, $port);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$keyword = $_GET['keyword'];
$keyword = trim($keyword);
$keyword = normalizer_normalize($keyword, Normalizer::NFKC);

// 假设关键词可能是名字、队名或者学校
// 其中名字和学校全匹配（做标准化转换），队名可以是部分匹配

// 首先是人名
$sql = "SELECT s.name as school, t.name as team, t.other_names as team_other_name, c.name as competitor, r.rank, r.school_rank, r.prize, r.is_official FROM results r 
LEFT JOIN teams t ON r.team_id = t.id 
LEFT JOIN teams_competitors tc ON t.id = tc.team_id 
LEFT JOIN competitors c ON tc.competitor_id = c.id 
LEFT JOIN schools s ON t.school_id = s.id 
WHERE c.name = \"" . $keyword . "\"";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    var_dump($row);
    echo "<br/><br/>";
  }
} else {
  echo "people 0 results<br/><br/>";
}

// 然后是队名
$sql = "SELECT s.name as school, t.name as team, t.other_names as team_other_name, c.name as competitor, r.rank, r.school_rank, r.prize, r.is_official FROM results r 
LEFT JOIN teams t ON r.team_id = t.id 
LEFT JOIN teams_competitors tc ON t.id = tc.team_id 
LEFT JOIN competitors c ON tc.competitor_id = c.id 
LEFT JOIN schools s ON t.school_id = s.id 
WHERE t.name like \"%" . $keyword . "%\"";

//var_dump($sql);

$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    var_dump($row);
    echo "<br/><br/>";
  }
} else {
  echo "team 0 results<br/><br/>";
}

// 最后是学校
$sql = "SELECT s.name as school, t.name as team, t.other_names as team_other_name, c.name as competitor, r.rank, r.school_rank, r.prize, r.is_official FROM results r 
LEFT JOIN teams t ON r.team_id = t.id 
LEFT JOIN teams_competitors tc ON t.id = tc.team_id 
LEFT JOIN competitors c ON tc.competitor_id = c.id 
LEFT JOIN schools s ON t.school_id = s.id 
WHERE s.name = \"" . $keyword . "\"";

//var_dump($sql);

$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    var_dump($row);
    echo "<br/><br/>";
  }
} else {
  echo "school 0 results<br/><br/>";
}

$conn->close();
?>