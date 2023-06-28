$season = '2019'
$sites2019 = @("xuzhou", "nanjing","yinchuan","shenyang","nanchang","shanghai","hongkong","ec-final")
$sites2019 | %{python .\board_downloader.py "../../local/board_data/$season/$_" $season $_ --force}