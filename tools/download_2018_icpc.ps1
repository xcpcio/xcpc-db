$season = '2018'
$sites2019 = @("jiaozuo", "xuzhou", "shenyang", "beijing", "nanjing", "qingdao", "hongkong", "ec-final")
$sites2019 | %{python .\board_downloader.py "../../local/board_data/$season/$_" $season $_ --force}